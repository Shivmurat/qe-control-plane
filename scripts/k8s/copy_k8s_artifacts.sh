#!/bin/bash

NAMESPACE=$1
POD_NAME=$2

set -e


if [ -z "$NAMESPACE" ] || [ -z "$POD_NAME" ]; then

    echo "Namespace or pod name missing"

    exit 1
fi


echo "Using namespace: ${NAMESPACE}"

echo "Using pod: ${POD_NAME}"


RUN_ID=$(kubectl exec \
  -n ${NAMESPACE} \
  ${POD_NAME} \
  -- \
  sh -c "ls /app/artifacts/runs | tail -n 1")


echo "Found run id: ${RUN_ID}"


mkdir -p artifacts/runs


kubectl cp \
  ${NAMESPACE}/${POD_NAME}:/app/artifacts/runs/${RUN_ID} \
  artifacts/runs/${RUN_ID}


echo "Kubernetes artifacts copied successfully"