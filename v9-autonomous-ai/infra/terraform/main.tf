provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_eks_cluster" "v9" {
  name     = "v9-ai-cluster"
  role_arn = "arn:aws:iam::123456:role/EKSRole"

  vpc_config {
    subnet_ids = ["subnet-xxx"]
  }
}
