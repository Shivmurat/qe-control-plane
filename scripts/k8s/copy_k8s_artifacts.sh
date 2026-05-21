#!/bin/bash

set -e


POD_NAME=$(kubectl get pods \
  --selector=job-name=qe-control-plane-job \
  --output=jsonpath="{.items[0].metadata.name}")


echo "Found pod: ${POD_NAME}"


RUN_ID=$(kubectl exec ${POD_NAME} -- \
  ls /app/artifacts/runs | tail -n 1)


echo "Found run id: ${RUN_ID}"


mkdir -p artifacts/runs


kubectl cp \
  ${POD_NAME}:/app/artifacts/runs/${RUN_ID} \
  artifacts/runs/${RUN_ID}


echo "Kubernetes artifacts copied successfully"