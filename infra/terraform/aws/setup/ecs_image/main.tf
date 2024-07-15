terraform {
  required_version = "~> 1.0"

  # --- Backend must be provisioned first
  backend "s3" {}
  # --- Backend must be provisioned first

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2.0"
    }
  }
}

locals {
  apps_dir = abspath("${path.module}/../../../../../")
}

data "aws_caller_identity" "current" {}

resource "aws_ecr_repository" "main" {
  name                 = "py-order-system-catalogue"
  image_tag_mutability = "MUTABLE"
  force_delete         = var.ecr_repository_force_delete

  image_scanning_configuration {
    scan_on_push = true
  }
}

module "push_analytics_docker_image" {
  source = "../../modules/push_image"

  region                      = var.region
  ecr_repository_name         = aws_ecr_repository.main.name
  ecr_registry_uri            = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com"
  container_image_tag         = "latest"
  container_image_source_path = "${local.apps_dir}/"
  force_image_rebuild         = false
}
