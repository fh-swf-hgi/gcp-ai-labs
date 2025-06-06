#!/bin/bash

username=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | cut -d '@' -f1)

echo "Using username: ${username}"

if [ ! -z "$username" ]
then
    tar cfz source.tgz Dockerfile main.py  requirements.txt
    gcloud builds submit source.tgz  --region=europe-west1 --project cloud-computing-ss25 --tag=gcr.io/cloud-computing-ss25/${username}-imagetag
    rm source.tgz
    gcloud run deploy ${username}-imagetag-service --project cloud-computing-ss25 --image gcr.io/cloud-computing-ss25/${username}-imagetag --allow-unauthenticated
fi
