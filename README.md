# BookFinder - Final Project

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
BookFinder_FinalProject/
├── app/                # Frontend (Streamlit)
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── backend/            # Backend (Flask)
│   ├── app.py
│   ├── book_embeddings.csv
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/                # Kubernetes manifests (Kustomize-ready)
│   ├── kustomization.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── iac/              # Terraform files for GCP Autopilot
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfvars.example
│   └── README.md (optional)
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
git clone https://github.com/bennymestel/BookFinder_FinalProject.git
cd BookFinder_FinalProject

# Apply manifests using Kustomize
kubectl apply -k k8s/

# Streamlit will be available at:
http://localhost:8501
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
cd BookFinder_FinalProject/iac

# Set up variables
# Edit terraform.tfvars with your GCP project ID and region

# Authenticate with GCP
gcloud auth login
gcloud auth application-default login

# Deploy the infrastructure
terraform init
terraform apply

# Connect to GKE (replace REGION with the region you specified in terraform.tfvars)
gcloud container clusters get-credentials bookfinder-cluster --region=REGION

# Deploy the app
kubectl apply -k ../k8s/

# Get external IP
kubectl get svc book-finder-frontend
```

Access your deployed app at:

```
http://<EXTERNAL-IP>
```

⚠️ Note: The frontend service is exposed on port 80 by default for GCP compatibility.

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
