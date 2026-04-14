provider "aws" { region = "ap-southeast-1" }

resource "aws_eks_cluster" "v14" {
  name = "v14-cluster"
  role_arn = "arn:aws:iam::123:role/EKSRole"
  vpc_config { subnet_ids = ["subnet-xxx"] }
}
