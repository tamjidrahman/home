#!/bin/bash
set -e

# Deploy script for Home API to AWS App Runner
# Usage: ./deploy.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Check for required tools
command -v aws >/dev/null 2>&1 || { echo "AWS CLI required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker required but not installed."; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "Terraform required but not installed."; exit 1; }

# Get ECR repository URL from Terraform output
cd "$SCRIPT_DIR"
ECR_URL=$(terraform output -raw ecr_repository_url 2>/dev/null || echo "")

if [ -z "$ECR_URL" ]; then
    echo "ECR repository not found. Running terraform apply first..."
    terraform init
    terraform apply -target=aws_ecr_repository.home_api -auto-approve
    ECR_URL=$(terraform output -raw ecr_repository_url)
fi

AWS_REGION=$(terraform output -raw ecr_repository_url | cut -d. -f4)
AWS_ACCOUNT=$(terraform output -raw ecr_repository_url | cut -d. -f1)

echo "Building Docker image..."
cd "$ROOT_DIR"
docker build -t home-api:latest .

echo "Logging into ECR..."
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com"

echo "Tagging and pushing image..."
docker tag home-api:latest "$ECR_URL:latest"
docker push "$ECR_URL:latest"

echo "Applying full Terraform configuration..."
cd "$SCRIPT_DIR"
terraform apply

echo ""
echo "Deployment complete!"
terraform output apprunner_service_url
