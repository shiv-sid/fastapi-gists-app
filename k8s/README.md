# Kubernetes deployment — FastAPI Gists App

## Folder structure
```yaml
k8s/
│── deployment.yml   → FastAPI Deployment
│── service.yml      → ClusterIP service
│── ingress.yml      → exposes app at http://fastapi.gists.local/<username>
│── argocd-app.yml   → ArgoCD GitOps automation
```
---

## Deploy

minikube start --driver=docker
minikube addons enable ingress
minikube tunnel   # keep running

kubectl apply -f k8s/

---

## Access API

http://fastapi.gists.local/octocat

---

## Enable GitOps (optional)

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl apply -f k8s/argocd-app.yml
