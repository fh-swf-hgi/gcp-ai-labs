#!/bin/bash

username=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | cut -d '@' -f1)

echo "Using username: ${username}"

if [ ! -z "$username" ]
then

    gcloud builds submit --region=europe-west1 --gcs-source-staging-dir=gs://image_build_storage/source --project cloud-computing-ss23 --tag eu.gcr.io/cloud-computing-ss23/${username}-imagetag

    gcloud run deploy ${username}-imagetag-service --project cloud-computing-ss23 --image eu.gcr.io/cloud-computing-ss23/${username}-imagetag
fi