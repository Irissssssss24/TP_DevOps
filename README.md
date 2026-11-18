<div align="center">

# Application 3-Tiers Conteneurisée
### Déploiement Dev · Val · Prod avec Docker, Kubernetes et GitHub Actions

Projet académique de groupe réalisé dans le cadre du module **DevOps**.


### Dev — Docker Compose

À la racine du dépôt :

```bash
docker compose up -d --build
```

Pour arrêter les conteneurs :

```bash
docker compose down
```

```bash
minikube status || minikube start
kubectl create namespace val
kubectl create namespace prod
```

```bash
docker build -t killian2470/tp_devops:backend-val ./backend
docker build -t killian2470/tp_devops:frontend-val ./frontend
docker build -t killian2470/tp_devops:backend-prod ./backend
docker build -t killian2470/tp_devops:frontend-prod ./frontend
minikube image load killian2470/tp_devops:backend-val
minikube image load killian2470/tp_devops:frontend-val
minikube image load killian2470/tp_devops:backend-prod
minikube image load killian2470/tp_devops:frontend-prod
```


```bash
kubectl apply -f k8s/val/ -n val
kubectl apply -f k8s/prod/ -n prod
```

```bash
kubectl get pods -n val
kubectl get pods -n prod
```

```bash
minikube service frontend-service -n val --url
minikube service frontend-service -n prod --url
```




