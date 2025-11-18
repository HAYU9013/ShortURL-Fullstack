variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
}

variable "project_name" {
  description = "Human friendly project name used for tagging and resource naming"
  type        = string
}

variable "environment" {
  description = "Deployment environment label"
  type        = string
  default     = "prod"
}

variable "vpc_cidr" {
  description = "CIDR range for the primary VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
  default     = [
    "10.0.0.0/24",
    "10.0.1.0/24",
  ]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the private subnets"
  type        = list(string)
  default     = [
    "10.0.10.0/24",
    "10.0.11.0/24",
  ]
}

variable "availability_zones" {
  description = "Optional list of availability zones to use. Leave empty to automatically select."
  type        = list(string)
  default     = []
}

variable "route53_zone_id" {
  description = "Route53 hosted zone ID that contains the application domains"
  type        = string
}

variable "alb_subdomain" {
  description = "Subdomain to use for the backend/API load balancer (e.g. api.example.com)"
  type        = string
}

variable "frontend_subdomain" {
  description = "Subdomain to use for the frontend CloudFront distribution (e.g. app.example.com)"
  type        = string
}

variable "alb_certificate_arn" {
  description = "ACM certificate ARN (in the same region as the ALB) for HTTPS termination"
  type        = string
}

variable "cloudfront_certificate_arn" {
  description = "ACM certificate ARN (in us-east-1) for the CloudFront distribution"
  type        = string
}

variable "allowed_origins" {
  description = "List of allowed origins for CORS"
  type        = list(string)
  default     = []
}

variable "container_cpu" {
  description = "CPU units to allocate to the backend task"
  type        = number
  default     = 512
}

variable "container_memory" {
  description = "Memory (in MiB) to allocate to the backend task"
  type        = number
  default     = 1024
}

variable "desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 2
}

variable "min_capacity" {
  description = "Minimum number of ECS tasks"
  type        = number
  default     = 2
}

variable "max_capacity" {
  description = "Maximum number of ECS tasks"
  type        = number
  default     = 6
}

variable "container_image_tag" {
  description = "Image tag to deploy from the ECR repository"
  type        = string
  default     = "latest"
}

variable "log_retention_in_days" {
  description = "CloudWatch log retention period"
  type        = number
  default     = 30
}

variable "docdb_instance_class" {
  description = "Instance class for DocumentDB"
  type        = string
  default     = "db.r5.large"
}

variable "docdb_instance_count" {
  description = "Number of DocumentDB instances to deploy"
  type        = number
  default     = 2
}

variable "docdb_backup_retention_period" {
  description = "Number of days to retain automated backups"
  type        = number
  default     = 7
}

variable "docdb_database" {
  description = "Database name to create in DocumentDB"
  type        = string
  default     = "shorturl"
}

variable "docdb_port" {
  description = "Port DocumentDB listens on"
  type        = number
  default     = 27017
}

variable "frontend_default_root_object" {
  description = "Default root object served by CloudFront"
  type        = string
  default     = "index.html"
}

variable "frontend_price_class" {
  description = "CloudFront price class"
  type        = string
  default     = "PriceClass_100"
}

variable "extra_tags" {
  description = "Additional tags to add to all resources"
  type        = map(string)
  default     = {}
}
