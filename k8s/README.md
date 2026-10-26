# Kubernetes deployment

## Before applying
1. Push the repository to GitHub and run Stage 7.5 successfully.
2. Replace `YOUR_GITHUB_OWNER` and `REPLACE_WITH_GIT_SHA` in both Deployment manifests with the actual owner and the exact SHA reported by the workflow.
3. Create a namespace and secrets. For training only, create the secret in your shell without committing it:
   ```bash
   kubectl create namespace retailops
   kubectl -n retailops create secret generic retailops-secrets \
     --from-literal=DATABASE_URL='postgresql+psycopg://USER:PASSWORD@YOUR_DB_HOST:5432/retailops' \
     --from-literal=JWT_SECRET_KEY='REPLACE_WITH_RANDOM_SECRET_AT_LEAST_32_CHARS' \
     --from-literal=ADMIN_PASSWORD='REPLACE_ME_ADMIN' \
     --from-literal=WAREHOUSE_PASSWORD='REPLACE_ME_WAREHOUSE' \
     --from-literal=CUSTOMER_PASSWORD='REPLACE_ME_CUSTOMER'
   ```
   The Kubernetes example expects an externally reachable PostgreSQL database. For a disposable lab cluster, you can add a PostgreSQL StatefulSet and persistent volume, but use managed PostgreSQL for a cloud-ready setup.
4. Apply:
   ```bash
   kubectl apply -f namespace.yaml
   kubectl apply -f configmap.yaml
   kubectl apply -f api-deployment.yaml
   kubectl apply -f web-deployment.yaml
   kubectl get pods,svc -n retailops
   ```
5. For ingress, install an ingress controller, configure DNS and TLS, update `ingress.yaml`, then apply it. Do not expose the plain HTTP lab configuration to the public internet.

## Local cluster quick check
```bash
kubectl -n retailops port-forward svc/retailops-web 8080:80
kubectl -n retailops port-forward svc/retailops-api 8000:8000
```
Run port-forwards in separate terminals. For production, configure API CORS for the actual web origin and use a single TLS ingress/reverse proxy.
