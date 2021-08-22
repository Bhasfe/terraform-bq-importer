module "datasets" {
  source = "./datasets"
}

terraform {
  backend "gcs" {
    bucket = "<bucket-name>"
    prefix = "state"
  }
}

provider "google" {
  project = "<project-name>"
  region  = "<region>"
}