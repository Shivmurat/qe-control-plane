resource "kubernetes_namespace" "qe_namespace" {

  metadata {
    name = var.namespace
  }

}