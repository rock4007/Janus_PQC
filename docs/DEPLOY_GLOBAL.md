# Global Deployment Guide

This guide covers building, pushing, and running Janus_PQC worldwide across AWS, Azure, and GCP. Use FIPS-validated crypto modules for government-regulated environments.

## Prerequisites
- Docker installed and logged in to your cloud registry.
- Cloud CLIs installed and authenticated: AWS CLI, Azure CLI, Google Cloud SDK.
- A container registry in each cloud (ECR/ACR/GCR) and a resource group/project.

## Build Container
```bash
# From repo root
docker build -t janus-pqc:latest .
```

## AWS (ECR) — US, Canada, APAC, EU
Example regions: us-east-1, us-west-2, ca-central-1, ap-northeast-1, ap-southeast-1/2/3, ap-south-1/2, eu-west-1, eu-central-1.
```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1
REPO=janus-pqc

aws ecr create-repository --repository-name $REPO --region $REGION || true
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker tag janus-pqc:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest

# Run on EC2 or ECS (Fargate) — example EC2 command
ssh ec2-user@<EC2_PUBLIC_IP> "docker pull $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest && docker run --rm $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:latest"
```
Repeat for other regions by changing `REGION`.

## Azure (ACR) — US, Canada, APAC, EU
Example regions: eastus, westus2, canadacentral, southeastasia, australiaeast, japaneast, westeurope, northeurope, uksouth.
```bash
ACR_NAME=<your_acr_name>
RESOURCE_GROUP=<your_rg>
REGION=eastus

az acr create --name $ACR_NAME --resource-group $RESOURCE_GROUP --sku Basic --location $REGION || true
az acr login --name $ACR_NAME

docker tag janus-pqc:latest $ACR_NAME.azurecr.io/janus-pqc:latest
docker push $ACR_NAME.azurecr.io/janus-pqc:latest

# Run on Azure Container Instances (ACI)
az container create \
  --name janus-pqc \
  --resource-group $RESOURCE_GROUP \
  --image $ACR_NAME.azurecr.io/janus-pqc:latest \
  --registry-login-server $ACR_NAME.azurecr.io \
  --restart-policy OnFailure
```

## GCP (GCR/Artifact Registry) — US, Canada, APAC, EU
Example multi-regions: us, eu, asia. Example regions: us-central1, us-east1, northamerica-northeast1, asia-southeast1, asia-northeast1, australia-southeast1, europe-west1/2/3, europe-central2.
```bash
PROJECT_ID=$(gcloud config get-value project)
REGION=us-central1
REPO=janus-pqc

# Artifact Registry recommended
gcloud artifacts repositories create $REPO --repository-format=docker --location=$REGION --description="Janus_PQC" || true

gcloud auth configure-docker $REGION-docker.pkg.dev

docker tag janus-pqc:latest $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/janus-pqc:latest
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/janus-pqc:latest

# Run on GCE VM
gcloud compute ssh <instance-name> --zone=$REGION --command "sudo docker pull $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/janus-pqc:latest && sudo docker run --rm $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/janus-pqc:latest"
```

## Kubernetes (Optional)
Use any global region cluster; set the image to your registry path.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: janus-pqc
spec:
  replicas: 1
  selector:
    matchLabels: { app: janus-pqc }
  template:
    metadata:
      labels: { app: janus-pqc }
    spec:
      containers:
        - name: janus-pqc
          image: <REGISTRY_PATH>/janus-pqc:latest
          imagePullPolicy: Always
```
Apply with your cloud’s Kubernetes tooling.

## FIPS & Compliance Notes
- Use FIPS 140-3 validated crypto modules and enable FIPS mode where applicable.
- Store keys in HSM/KMS; enforce RBAC, logging, and audit trails.
- Track SBOM and run dependency audits (pip-audit) continuously.

## Troubleshooting
- Container pull auth errors: re-login to registry and ensure role permissions.
- Region not supported: pick nearest supported region per cloud.
- oqs/liboqs not present: adapter uses Ed448 fallback; for ML-DSA use Linux/WSL with liboqs.
