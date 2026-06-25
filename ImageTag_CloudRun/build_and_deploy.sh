#!/bin/bash
set -euo pipefail

project_id="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"
region="${REGION:-europe-west3}"
repository="${REPOSITORY:-cloud-run-images}"
username=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | cut -d '@' -f1 | tr '.@' '--')
image="${region}-docker.pkg.dev/${project_id}/${repository}/${username}-imagetag"
service="${username}-imagetag-service"

echo "Using project: ${project_id}"
echo "Using username: ${username}"
echo "Using region: ${region}"

if [ -z "$project_id" ] || [ "$project_id" = "(unset)" ]; then
    echo "No GCP project configured. Run: gcloud config set project cloud-computing-ss26"
    exit 1
fi

if [ -z "$username" ]; then
    echo "No active gcloud account found. Run: gcloud auth login"
    exit 1
fi

if ! gcloud artifacts repositories describe "$repository" --location "$region" --project "$project_id" >/dev/null 2>&1; then
    gcloud artifacts repositories create "$repository" \
        --repository-format=docker \
        --location="$region" \
        --description="Container images for Cloud Run labs" \
        --project "$project_id"
fi

tar cfz source.tgz Dockerfile main.py requirements.txt
gcloud builds submit source.tgz \
    --region="$region" \
    --project "$project_id" \
    --tag="$image"
rm source.tgz

gcloud run deploy "$service" \
    --project "$project_id" \
    --region="$region" \
    --image "$image" \
    --allow-unauthenticated
