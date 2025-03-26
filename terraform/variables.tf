variable "project_id" {
  description = "The Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "The region for resources"
  type        = string
  default     = "us-east1"
}