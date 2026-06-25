# ImageTag Cloud Run

Build and deploy the service to Cloud Run with Artifact Registry:

```bash
gcloud config set project cloud-computing-ss26
./build_and_deploy.sh
```

Optional environment variables:

```bash
PROJECT_ID=cloud-computing-ss26 REGION=europe-west3 REPOSITORY=cloud-run-images ./build_and_deploy.sh
```
