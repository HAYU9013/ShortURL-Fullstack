variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  default     = "shorturl-fullstack"
}

variable "environment" {
  description = "Environment (dev, prod)"
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  default     = "10.0.0.0/16"
}

variable "db_username" {
  description = "Database master username"
  default     = "admin"
}

variable "db_password" {
  description = "Database master password"
  sensitive   = true
  default     = "ChangeMe123!" # In production, use Secrets Manager or input variable
}
