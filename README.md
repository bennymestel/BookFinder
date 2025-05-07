# BookFinder

**BookFinder** is a web application that helps users discover books similar to their favorites by analyzing book descriptions and genres. It leverages natural language processing to compare descriptions and generate personalized recommendations from a custom dataset.

---

## Features

- 🔍 **Search by title & author** using the Google Books API
- ✂️ **Summarize descriptions** with a pretrained `t5-small` model
- 📚 **Find similar books** using sentence embeddings
- 🔗 **Clickable Libgen links** for quick access to recommended titles

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Flask API + precomputed embeddings
- **ML Models**: Transformers (T5), Sentence-Transformers
- **Data Handling**: Pandas, NumPy
- **Deployment**: Docker, Kubernetes, Helm
- **Infrastructure**: Docker, Kubernetes, Terraform, GKE Autopilot
- **APIs**: Google Books API

---

## Architecture Overview

- **Frontend (Streamlit)** runs on port `8501`, calls backend API
- **Backend (Flask)** runs on port `5000`, loads a CSV with 500+ books and precomputed embeddings
- **Deployment**: Dockerized, deployed via Kubernetes
- **Cloud Option**: Full deployment via Terraform to GCP using GKE Autopilot

---

## Repository Structure

```
BookFinder/
├── app/                # Frontend (Streamlit)
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── backend/            # Backend (Flask)
│   ├── app.py
│   ├── book_embeddings.csv
│   ├── Dockerfile
│   └── requirements.txt
├── deployments/        # Deployment configurations
│   ├── helm/           # Helm chart for Kubernetes deployment
│   │   └── bookfinder/ # Helm chart files
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       └── templates/
│   │           ├── _helpers.tpl
│   │           ├── backend-deployment.yaml
│   │           ├── backend-service.yaml
│   │           ├── configmap.yaml
│   │           ├── frontend-deployment.yaml
│   │           ├── frontend-service.yaml 
│   │           ├── ingress.yaml
│   │           ├── NOTES.txt
│   │           └── secret.yaml
│   └── kustomize/      # Kustomize-based deployment
│       ├── kustomization.yaml
│       ├── frontend-deployment.yaml
│       ├── frontend-service.yaml
│       ├── backend-deployment.yaml
│       ├── backend-service.yaml
│       ├── configmap.yaml
│       └── secret.yaml
├── iac/                # Terraform files for GCP deployment
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars
├── scripts/              # Utility scripts for dataset preperation and model training
│   └── generate_embeddings.py
└── README.md
```

---

## 🔧 Local Kubernetes Deployment

### Prerequisites

- Kubernetes (e.g. Minikube or Docker Desktop)
- `kubectl` and `kustomize`
- Docker (if building images locally)
- A Google Books API key

### Steps

```bash
# Clone the repository
git clone https://github.com/bennymestel/BookFinder.git
cd BookFinder

# Apply manifests using Kustomize
kubectl apply -k k8s/

# Streamlit will be available at:
http://localhost
```

---

## ☁️ Cloud Deployment (GCP Autopilot via Terraform)

### Prerequisites

- Google Cloud SDK
- Terraform
- A GCP account with billing enabled
- Docker images published on DockerHub:
  - `bennymestel/book-finder-frontend`
  - `bennymestel/book-finder-backend`

### Steps

```bash
# Clone and enter the Terraform directory
cd BookFinder/iac

# Set up variables
# Edit terraform.tfvars with your GCP project ID and region

# Authenticate with GCP
gcloud auth login
gcloud auth application-default login

# Deploy the infrastructure
terraform init
terraform apply

# Connect to GKE (replace REGION with the region you specified in terraform.tfvars)
gcloud container clusters get-credentials book-finder-cluster --region=REGION

# Deploy the app using Kustomize
kubectl apply -k ../deployments/kustomize/

# Or deploy using Helm
helm install bookfinder ../deployments/helm/bookfinder

# Get external IP
kubectl get svc book-finder-frontend
```

Access your deployed app at:

```
http://<EXTERNAL-IP>
```
---

## 🔱 Helm Deployment

The Helm chart provides a simple way to deploy the entire application to any Kubernetes cluster.

### Prerequisites

- Kubernetes cluster (local or cloud)
- Helm 3.0+
- Docker images published on DockerHub:
  - `bennymestel/book-finder-frontend`
  - `bennymestel/book-finder-backend`

### Steps

```bash
# From the project root
cd deployments/helm

# Install the chart
helm install bookfinder ./bookfinder

# Get the service address
kubectl get svc book-finder-frontend
```

### Accessing the Application

Once deployed, you can access the application through the frontend LoadBalancer service. For local development with minikube, you may need to use `minikube service book-finder-frontend` instead.

```bash
# For cloud providers with LoadBalancer support
export SERVICE_IP=$(kubectl get svc book-finder-frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "BookFinder is available at: http://$SERVICE_IP"
```

Access your deployed app at:

```
http://<EXTERNAL-IP>
```

The Helm chart uses a ConfigMap to provide book embedding data to the backend service. For larger datasets, you might want to:

1. Build a custom backend Docker image that includes your full dataset
2. Update the backend Dockerfile to copy your dataset into the image
3. Push this image to your registry and update the values file

---

## Helm Chart Configuration

The Helm chart (`deployments/helm/bookfinder`) provides a complete Kubernetes deployment of the BookFinder application. The chart includes both frontend and backend components, along with their configurations, services, and resources.

### Installing the Chart

```bash
# From the project root
cd deployments/helm
helm install bookfinder ./bookfinder
```

### Uninstalling the Chart

```bash
helm delete bookfinder
```

### Key Configuration Parameters

#### Frontend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `bennymestel/book-finder-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.service.type` | Frontend service type | `LoadBalancer` |
| `frontend.service.port` | Frontend service port | `80` |
| `frontend.service.targetPort` | Frontend container port | `8501` |

#### Backend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.image.repository` | Backend image repository | `bennymestel/book-finder-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.service.type` | Backend service type | `ClusterIP` |
| `backend.service.port` | Backend service port | `5000` |

#### Other Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `googleBooksApiKey` | Google Books API Key | `""` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | IngressClass to use | `""` |
| `ingress.annotations` | Ingress annotations | `{}` |

### Data Management

The BookFinder application requires book embedding data to function properly. This chart uses a ConfigMap to provide sample book data to the backend service. For larger datasets, you might want to build a custom Docker image that includes your full dataset.

For full configuration options, see `deployments/helm/bookfinder/values.yaml`.

---

## 🔐 Secrets and API Keys

Store your Google Books API key securely:

- In `k8s/secret.yaml`
- Or as an environment variable

Streamlit config and secrets can be set via mounted `secrets.toml`.

---

## 🔁 Updating Embeddings

To regenerate `book_embeddings.csv`:

```bash
python scripts/generate_embeddings.py
```

Replace the CSV in `backend/`, rebuild the image, and redeploy.

---

## 📦 Docker Images

Prebuilt images are hosted on DockerHub:

- Frontend: `bennymestel/book-finder-frontend`
- Backend: `bennymestel/book-finder-backend`

---

## ✅ Status

- App runs locally and in the cloud
- Fully containerized and K8s-deployable
- Infrastructure as Code with Terraform
- Public GCP-compatible deployment path
