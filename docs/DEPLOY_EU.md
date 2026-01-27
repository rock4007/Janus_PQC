# Regional Deployment (UK, Ireland, EU)

Janus_PQC is a Python-based verification tool and containerizable app. This guide shows how to deploy and run it in UK, Ireland, and EU regions across AWS, Azure, and GCP.

Important: For government/regulatory use, operate only with FIPS 140-3 validated crypto modules and approved algorithms in FIPS mode. See COMPLIANCE.md.

## AWS (ECR + ECS/Fargate or Lambda)

### Choose a Region
- UK (London): `eu-west-2`
- Ireland (Dublin): `eu-west-1`
- EU (Frankfurt): `eu-central-1`

### Build and Push Image to ECR
```bash
# Set region
AWS_REGION=eu-west-1  # change to eu-west-2 or eu-central-1 as needed
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_NAME=janus-pqc

# Create repo (idempotent)
aws ecr describe-repositories --repository-names "$REPO_NAME" --region $AWS_REGION >/dev/null 2>&1 || \
  aws ecr create-repository --repository-name "$REPO_NAME" --image-scanning-configuration scanOnPush=true --region $AWS_REGION

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push
docker build -t $REPO_NAME .
docker tag $REPO_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest
```

### Run on ECS Fargate (task example)
Use a minimal task definition referencing the ECR image and run it in the selected region and VPC/subnets.

### Run on Lambda (container)
- Create Lambda with container image from ECR in the chosen region.
- Handler: wrap the Python entry in a simple CLI triggered by an event (e.g., verify a payload).

## Azure (ACR + Container Apps)
```bash
# Region examples: westeurope, northeurope, uksouth
AZ_REGION=westeurope
AZ_RG=janus-pqc-rg
AZ_ACR=januspqcacr

az group create -n $AZ_RG -l $AZ_REGION
az acr create -n $AZ_ACR -g $AZ_RG --sku Basic -l $AZ_REGION
az acr login -n $AZ_ACR

docker build -t $AZ_ACR.azurecr.io/janus-pqc:latest .
docker push $AZ_ACR.azurecr.io/janus-pqc:latest

az containerapp env create -n janus-env -g $AZ_RG -l $AZ_REGION
az containerapp create -n janus-pqc -g $AZ_RG --environment janus-env \
  --image $AZ_ACR.azurecr.io/janus-pqc:latest --target-port 8080 --ingress 'internal'
```

## GCP (Artifact Registry + Cloud Run)
```bash
# Region examples: europe-west1 (Belgium), europe-west2 (London), europe-west4 (Netherlands), europe-central2 (Warsaw)
GCP_REGION=europe-west2
PROJECT_ID=$(gcloud config get-value project)
REPO=janus-pqc

gcloud artifacts repositories create $REPO --repository-format=docker --location=$GCP_REGION --description="Janus_PQC"

gcloud auth configure-docker $GCP_REGION-docker.pkg.dev

docker build -t $GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO/janus-pqc:latest .
docker push $GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO/janus-pqc:latest

gcloud run deploy janus-pqc --image=$GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO/janus-pqc:latest --region=$GCP_REGION --platform=managed --ingress=internal
```

## Data Residency & Compliance
- Select UK/Ireland/EU regions per policy.
- Store keys in regional KMS/HSM (AWS KMS, Azure Key Vault, GCP KMS).
- Ensure FIPS mode and validated modules where required.

## Runtime Notes
- The `Dockerfile` runs the script; adjust CMD/entrypoint to integrate with your service.
- For non-container runs, install `requirements.txt` in region-local hosts.

## Validation
- After deploy, run a health check job to execute Janus_PQC and capture logs:
  - Expect: "[SUCCESS] Data Integrity Verified: System is Quantum-Safe and Uncompromisable."
