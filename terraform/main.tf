provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_service_account" "cloud_run_deployer" {
  account_id   = "cloud-run-deployer"
  display_name = "Cloud Run Deployer Service Account"
}

resource "google_project_iam_member" "run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.cloud_run_deployer.email}"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.cloud_run_deployer.email}"
}

resource "google_project_iam_member" "cloud_build_editor" {
  project = var.project_id
  role    = "roles/cloudbuild.builds.editor"
  member  = "serviceAccount:${google_service_account.cloud_run_deployer.email}"
}

resource "google_project_iam_member" "iam_token_creator" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  member  = "serviceAccount:${google_service_account.cloud_run_deployer.email}"
}

resource "google_project_iam_member" "artifact_registry_admin" {
  project = var.project_id
  role    = "roles/artifactregistry.admin"
  member  = "serviceAccount:${google_service_account.cloud_run_deployer.email}"
}

# Fetch the default Compute Engine service account
data "google_compute_default_service_account" "default" {
  project = var.project_id  # Replace with your project ID variable or literal value
}

# Grant the deployer service account permission to act as the default service account
resource "google_service_account_iam_member" "act_as_default_sa" {
  service_account_id = data.google_compute_default_service_account.default.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:cloud-run-deployer@***.iam.gserviceaccount.com"
}

output "service_account_email" {
  value = google_service_account.cloud_run_deployer.email
}

resource "google_service_account_key" "cloud_run_deployer_key" {
  service_account_id = google_service_account.cloud_run_deployer.name
}

output "service_account_key_json" {
  value     = google_service_account_key.cloud_run_deployer_key.private_key
  sensitive = true
}