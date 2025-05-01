provider "google" {
    project = var.project_id
    region  = var.region
}

resource "google_container_cluster" "book-finder" {
    name  = "book-finder-cluster"
    location = var.region
    enable_autopilot = true
    networking_mode = "VPC_NATIVE"
}
