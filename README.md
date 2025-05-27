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
- **Infrastructure**: Docker, Kubernetes, Helm, Kustomize, Terraform, GKE Autopilot
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
├── deployments/        # Deployment configuration
│   ├── helm/           # Helm charts for Kubernetes deployment
│   │   └── bookfinder/ # Main chart directory
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
│   │           └── secret.yaml
│   └── kustomize/      # Kustomize-ready Kubernetes manifests
│       ├── kustomization.yaml
│       ├── frontend-deployment.yaml
│       ├── frontend-service.yaml
│       ├── backend-deployment.yaml
│       ├── backend-service.yaml
│       ├── configmap.yaml
│       ├── ingress.yaml
│       └── secret.yaml
├── iac/                # Terraform files for GCP Autopilot
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars
├── scripts/            # Utility scripts for dataset preparation and model training
│   └── generate_embeddings.py
└── README.md
```

---

## 🔧 Local Kubernetes Deployment

### Prerequisites

- Kubernetes (e.g. Minikube or Docker Desktop)
- `kubectl` with either `kustomize` or `helm` (v3+)
- Docker (if building images locally)
- A Google Books API key

### Option 1: Kustomize Deployment

Follow these steps to deploy BookFinder using Kustomize:

```bash
# 1. Clone the repository
git clone https://github.com/bennymestel/BookFinder.git
cd BookFinder

# 2. Add a local DNS entry
# For macOS/Linux:
echo "127.0.0.1 bookfinder.local" | sudo tee -a /etc/hosts
# For Windows (run PowerShell as Administrator):
Add-Content -Path "$env:windir\System32\drivers\etc\hosts" -Value "`n127.0.0.1 bookfinder.local" -Force

# 3. Apply manifests using Kustomize
kubectl apply -k deployments/kustomize/

# 4. Start a tunnel for ingress access (keep this terminal open)
minikube tunnel
```

Once deployed, BookFinder will be available at: http://bookfinder.local

> **Note:** The frontend application may take a few minutes to become fully operational on initial startup. This delay is primarily due to downloading and initializing the ML models (T5 and Sentence-Transformers).

### Option 2: Helm Deployment

Follow these steps to deploy BookFinder using Helm:

```bash
# 1. Clone the repository
git clone https://github.com/bennymestel/BookFinder.git
cd BookFinder

# 2. Add a local DNS entry
# For macOS/Linux:
echo "127.0.0.1 bookfinder.local" | sudo tee -a /etc/hosts
# For Windows (run PowerShell as Administrator):
Add-Content -Path "$env:windir\System32\drivers\etc\hosts" -Value "`n127.0.0.1 bookfinder.local" -Force

# 3. Install using the Helm chart
helm install bookfinder ./deployments/helm/bookfinder
```

Once deployed, BookFinder will be available at: http://bookfinder.local

> **Note:** The frontend application may take a few minutes to become fully operational on initial startup. This delay is primarily due to downloading and initializing the ML models (T5 and Sentence-Transformers).

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

# Deploy using Kustomize
kubectl apply -k ../deployments/kustomize/

# OR deploy using Helm
helm install bookfinder ../deployments/helm/bookfinder

# Get external IP
kubectl get svc book-finder-frontend
```

Access your deployed app at:

```
http://<EXTERNAL-IP>
```

> **Note:** The frontend application may take a few minutes to become fully operational on initial startup. This delay is primarily due to downloading and initializing the ML models (T5 and Sentence-Transformers).
---

## 🛞 Helm Chart Configuration

The Helm chart provides basic deployment configuration for the BookFinder application:

```bash
# View available configuration options
helm show values ./deployments/helm/bookfinder

# Install with custom values file (if needed)
helm install bookfinder ./deployments/helm/bookfinder -f my-values.yaml

# Uninstall the application
helm uninstall bookfinder
```

---

## 🔐 Secrets and API Keys

Store your Google Books API key securely:

- In `deployments/kustomize/secret.yaml` or `deployments/helm/bookfinder/templates/secret.yaml`
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

- Frontend: [`bennymestel/book-finder-frontend`](https://hub.docker.com/r/bennymestel/book-finder-frontend)
- Backend: [`bennymestel/book-finder-backend`](https://hub.docker.com/r/bennymestel/book-finder-backend)

---

## ✅ Status

- App runs locally and in the cloud
- Fully containerized and K8s-deployable
- Multiple deployment options: Kustomize and Helm
- Infrastructure as Code with Terraform
- Public GCP-compatible deployment path
- Kubernetes Ingress for unified access
