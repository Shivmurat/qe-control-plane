terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.37.1"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

module "qe_namespace" {
  source = "../../modules/kubernetes-namespace"
  namespace = var.namespace
}