# v14-singularity

Production-ready scaffold for the v14 Singularity service.

## Included scaffold pieces

- FastAPI starter service (`api/app.py`)
- Helm chart (`infra/helm`)
- ArgoCD application manifest (`infra/argocd/app.yaml`)

## Quickstart

1. Build and push image

```bash
docker build -t <your-registry>/v14:latest .
docker push <your-registry>/v14:latest
```

2. Deploy with Helm

```bash
helm install v14 v14-singularity/infra/helm
```

3. Connect ArgoCD (GitOps)

```bash
kubectl apply -f v14-singularity/infra/argocd/app.yaml
```
