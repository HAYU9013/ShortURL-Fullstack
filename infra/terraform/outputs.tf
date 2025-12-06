output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.this.name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.backend.name
}

output "application_load_balancer_dns" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.this.dns_name
}

output "cloudfront_domain" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "frontend_bucket_name" {
  description = "Name of the S3 bucket hosting the frontend"
  value       = aws_s3_bucket.frontend.id
}

output "ecr_repository_url" {
  description = "URL of the ECR repository for backend images"
  value       = aws_ecr_repository.backend.repository_url
}

output "backend_secret_arn" {
  description = "ARN of the Secrets Manager secret with backend environment variables"
  value       = aws_secretsmanager_secret.backend_env.arn
}
