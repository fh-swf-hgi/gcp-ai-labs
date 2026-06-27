$ErrorActionPreference = "Stop"

$projectId = if ($env:PROJECT_ID) {
    $env:PROJECT_ID
} else {
    (gcloud config get-value project 2>$null).Trim()
}

$region = if ($env:REGION) { $env:REGION } else { "europe-west3" }
$repository = if ($env:REPOSITORY) { $env:REPOSITORY } else { "cloud-run-images" }

# Aktiven Account holen
$rawAccount = (gcloud auth list --filter="status:ACTIVE" --format="value(account)").Trim()

if ($rawAccount -like "*workforcePools*") {
    # Bei Workforce-Pools: letzten Pfadbestandteil verwenden
    $username = ($rawAccount -split "/")[-1]
} else {
    # Normale Mailadresse: Teil vor @, Punkte/@ ersetzen
    $username = ($rawAccount -split "@")[0] -replace "[.@]", "-"
}

$image = "$region-docker.pkg.dev/$projectId/$repository/$username-imagetag"
$service = "$username-imagetag-service"
$bucketName = "${projectId}_cloudbuild"

Write-Host "Using project: $projectId"
Write-Host "Using username: $username"
Write-Host "Using region: $region"

if ([string]::IsNullOrWhiteSpace($projectId) -or $projectId -eq "(unset)") {
    Write-Error "No GCP project configured. Run: gcloud config set project cloud-computing-ss26"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($username)) {
    Write-Error "No active gcloud account found. Run: gcloud auth login"
    exit 1
}

# Artifact Registry Repository ggf. anlegen
$repoExists = $true
try {
    gcloud artifacts repositories describe $repository `
        --location $region `
        --project $projectId `
        *> $null
} catch {
    $repoExists = $false
}

if (-not $repoExists) {
    gcloud artifacts repositories create $repository `
        --repository-format=docker `
        --location=$region `
        --description="Container images for Cloud Run labs" `
        --project $projectId
}

# Cloud Build direkt aus aktuellem Verzeichnis.
# .gcloudignore verwenden, um unnötige Dateien auszuschließen.
gcloud builds submit . `
    --region=$region `
    --project=$projectId `
    --tag=$image `
    --gcs-source-staging-dir="gs://$bucketName/source/"

gcloud run deploy $service `
    --project=$projectId `
    --region=$region `
    --image=$image `
    --allow-unauthenticated
