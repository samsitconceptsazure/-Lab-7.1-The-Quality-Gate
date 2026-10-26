terraform {
  required_version = ">= 1.5.0"
}
# Lab-only security scanning fixture. No provider/resources are provisioned.
# Add real infrastructure in a separate, reviewed module before any apply.
locals {
  lab_name = "retailops-devsecops"
  data_classification = "training"
}
