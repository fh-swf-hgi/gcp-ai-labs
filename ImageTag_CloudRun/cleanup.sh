#!/bin/bash
set -euo pipefail

# Ressourcen-Bezeichnungen – dieselbe Logik wie in build_and_deploy.sh
project_id="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"
region="${REGION:-europe-west3}"
repository="${REPOSITORY:-cloud-run-images}"
raw_account=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
if [[ "$raw_account" == *"workforcePools"* ]]; then
    username=$(echo "$raw_account" | awk -F'/' '{print $NF}')
else
    username=$(echo "$raw_account" | cut -d '@' -f1 | tr '.@' '--')
fi
image="${region}-docker.pkg.dev/${project_id}/${repository}/${username}-imagetag"
service="${username}-imagetag-service"
bucket_name="${project_id}_cloudbuild"

echo "Using project:    ${project_id}"
echo "Using username:   ${username}"
echo "Using region:     ${region}"
echo ""

if [ -z "$project_id" ] || [ "$project_id" = "(unset)" ]; then
    echo "No GCP project configured. Run: gcloud config set project cloud-computing-ss26"
    exit 1
fi

# 1. Cloud Run Service löschen
echo "==> Deleting Cloud Run service: ${service}"
if gcloud run services describe "$service" \
        --project "$project_id" --region "$region" >/dev/null 2>&1; then
    gcloud run services delete "$service" \
        --project "$project_id" \
        --region "$region" \
        --quiet
    echo "    Deleted."
else
    echo "    Service not found – skipping."
fi

# 2. Artifact Registry: Docker-Image löschen
echo "==> Deleting Docker image: ${image}"
if gcloud artifacts docker images list "${region}-docker.pkg.dev/${project_id}/${repository}" \
        --project "$project_id" 2>/dev/null | grep -q "${username}-imagetag"; then
    gcloud artifacts docker images delete "${image}" \
        --project "$project_id" \
        --delete-tags \
        --quiet
    echo "    Deleted."
else
    echo "    Image not found – skipping."
fi

# 3. Artifact Registry: Repository löschen (nur wenn leer oder per Flag erzwungen)
echo "==> Checking Artifact Registry repository: ${repository}"
remaining=$(gcloud artifacts docker images list \
    "${region}-docker.pkg.dev/${project_id}/${repository}" \
    --project "$project_id" 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
if [ "$remaining" -eq 0 ]; then
    echo "    Repository is empty – deleting."
    gcloud artifacts repositories delete "$repository" \
        --location "$region" \
        --project "$project_id" \
        --quiet
    echo "    Deleted."
else
    echo "    Repository still contains ${remaining} image(s) – NOT deleted."
    echo "    To force deletion run:"
    echo "    gcloud artifacts repositories delete ${repository} --location ${region} --project ${project_id}"
fi

# Hinweis: Das Cloud Build Staging-Bucket (gs://${bucket_name}) wird
# projektübergreifend von allen Nutzern gemeinsam verwendet und wird
# daher hier NICHT gelöscht.

echo ""
echo "Cleanup done."
