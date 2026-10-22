# Argo CD GitOps

1. Install Argo CD in your cluster and ensure it can access your Git repository.
2. Edit `argocd/application.yaml`: replace `YOUR_GITHUB_OWNER` and repository URL.
3. Ensure the `k8s/` Deployment manifests refer to the exact SHA-tagged images published by Stage 7.5.
4. Apply the Argo CD Application:
   ```bash
   kubectl apply -f gitops/argocd/application.yaml
   ```
5. Inspect sync and health:
   ```bash
   kubectl -n argocd get applications
   argocd app get retailops
   argocd app sync retailops
   ```

The application uses automated sync and self-heal for the training environment. For a controlled production workflow, disable automatic production sync or use a separate protected GitOps branch and approval process. Do not store registry credentials or application secrets in Git.
