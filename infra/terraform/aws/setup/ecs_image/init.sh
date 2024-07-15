#!/bin/bash

ACCOUNT_ID=$(aws sts get-caller-identity --output json | grep -o '"Account": "[^"]*' | cut -d'"' -f4)
echo "Caller identity accofunt: $ACCOUNT_ID"
terraform init \
    -backend-config="bucket=tf-state-py-order-system-catalogue-${ACCOUNT_ID}" \
    -backend-config="key=streamlit_ecs_image_state/terraform.tfstate" \
    -backend-config="region=us-east-1" \
    -backend-config="dynamodb_table=tf-state-py-order-system-catalogue-${ACCOUNT_ID}" \
    -backend-config="encrypt=false" \
