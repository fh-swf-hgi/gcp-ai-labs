gcloud builds submit --region=europe-west1 --gcs-source-staging-dir=gs://image_build_storage/source --project cloud-computing-ss23 --tag eu.gcr.io/cloud-computing-ss23/hgi-imgtag

gcloud run deploy hgi-imgtag-service --project cloud-computing-ss23 --image eu.gcr.io/cloud-computing-ss23/hgi-imgtag