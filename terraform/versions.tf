# Specify the required Terraform version
terraform {
  required_version = "~> 1.9.0"

  required_providers {
    aws = {
      version = "~> 5.74"
    }
  }

  backend "s3" {
    bucket = "cpsc436c-g9-tfstate"
    key    = "tfstate"
    region = "ca-central-1"
  }
}
