# AWS Architecture Guide

This guide dives into the production architecture that Terraform provisions under `infra/terraform`. The stack is designed for a globally available, latency-sensitive URL shortener that must withstand sudden traffic spikes and sustained high throughput.

## High-level topology

```
Users ─▶ Route 53 ─┬────────▶ CloudFront CDN ─▶ S3 static site (Vue frontend)
                   │
                   └────────▶ Application Load Balancer ─▶ ECS Fargate service ─▶ Amazon DocumentDB cluster
                                                          │                         ▲
                                                          └────────▶ CloudWatch Logs│
                                                                                   Secrets Manager (credentials)
```

Key tenets of the design:

- **Layered networking** keeps compute and data isolated in private subnets while exposing only edge surfaces.
- **Elastic compute** on AWS Fargate auto-scales horizontally based on CPU and memory load, keeping latency low during bursts.
- **Managed data tier** on Amazon DocumentDB handles replica-based reads and encrypted storage without self-managing MongoDB.
- **Global delivery** via Amazon CloudFront caches the Vue frontend close to users and shields origin load.
- **Traffic management** with Amazon Route 53 directs clients to the optimal entry point and supports health-aware failover.

## Networking foundation

| Component | Terraform resource(s) | Notes for operations |
| --- | --- | --- |
| VPC | `aws_vpc.main` | `/16` CIDR (default `10.0.0.0/16`) with DNS hostnames enabled for service discovery. |
| Public subnets | `aws_subnet.public[*]` | Two AZs by default for ALB and NAT gateway; map public IPs for edge services. |
| Private subnets | `aws_subnet.private[*]` | Two AZs, isolated for ECS tasks and DocumentDB instances. |
| Internet access | `aws_internet_gateway.this`, `aws_nat_gateway.this` | Outbound-only egress from private subnets goes through the NAT gateway to fetch updates securely. |
| Routing | `aws_route_table.*` | Separate public/private route tables keep blast radius constrained. |
| Security groups | `aws_security_group.alb`, `aws_security_group.ecs`, `aws_security_group.docdb` | ALB only exposes 80/443; ECS tasks accept traffic solely from the ALB SG; DocumentDB is reachable only from ECS SG. |

## Compute & autoscaling

| Capability | Implementation | Scaling behavior |
| --- | --- | --- |
| Container registry | `aws_ecr_repository.backend` with lifecycle policy | Keeps last 30 images and enables on-push scanning. |
| Orchestrator | `aws_ecs_cluster.this` (Fargate) | No EC2 fleet to manage; integrates with ECS Exec for debugging. |
| Task definition | `aws_ecs_task_definition.backend` | Allocates 0.5 vCPU / 1 GiB RAM by default (`container_cpu`/`container_memory`). Injects env secrets and TLS CA bundle. |
| Load balancing | `aws_lb.this` + listeners + target group | HTTPS listener uses `ELBSecurityPolicy-TLS13-1-2-2021-06`; HTTP is auto-redirected to HTTPS. Health checks hit `/healthz`. |
| Service | `aws_ecs_service.backend` | Runs in private subnets without public IPs, using ALB for ingress. Deployment circuit breaker auto-rolls back bad revisions. |
| Autoscaling | `aws_appautoscaling_target.ecs` with CPU & memory policies | Default floor/ceiling of 2–6 tasks (`min_capacity`/`max_capacity`). Target tracking scales out when CPU >55% or memory >65% for sustained periods. |

### Performance considerations

- Set `desired_count` ≥ 2 for multi-AZ resilience.
- Adjust `container_cpu`/`container_memory` for heavier workloads; metrics stream to CloudWatch automatically.
- Health checks (`curl` command inside the task) ensure only healthy containers receive traffic.

## Data services

| Feature | Terraform resource(s) | Details |
| --- | --- | --- |
| DocumentDB cluster | `aws_docdb_cluster.this` + `aws_docdb_cluster_instance.this` | Two instances (`docdb_instance_count=2`) span AZs. TLS enabled, backups retained 7 days by default, deletion protection on. |
| Secrets | `aws_secretsmanager_secret.docdb`, `aws_secretsmanager_secret.backend_env` | Stores generated DB credentials and backend env (CORS, replica set, TLS flags). ECS task reads them at runtime. |
| Connectivity | `aws_docdb_subnet_group.this`, `aws_security_group.docdb` | Restricts access to private subnets and ECS security group to contain blast radius. |

### Working with DocumentDB

- Credentials rotate by updating the corresponding `aws_secretsmanager_secret_version` and recycling tasks.
- Replica set connection string defaults to `secondaryPreferred` reads to offload primaries during heavy GET traffic.
- Disable `deletion_protection` via console/CLI only when tearing down non-production clusters.

## Content delivery

| Component | Terraform resource(s) | Notes |
| --- | --- | --- |
| S3 bucket | `aws_s3_bucket.frontend` | Random suffix prevents naming collisions; versioning and SSE-S3 encryption enabled. |
| Access control | `aws_s3_bucket_public_access_block.frontend`, `aws_cloudfront_origin_access_control.frontend`, `aws_s3_bucket_policy.frontend` | Frontend bucket is private—only CloudFront can read objects. Logging writes to the same bucket under `cloudfront-logs/`. |
| CDN | `aws_cloudfront_distribution.frontend` | Enforces HTTPS, defaults to `index.html`, uses managed caching/CORS policies, supports custom domain via ACM in `us-east-1`. |

To publish a build:

1. `npm run build` in `frontend/`.
2. `aws s3 sync dist/ s3://<frontend_bucket_name>/ --delete`.
3. `aws cloudfront create-invalidation --distribution-id <id> --paths '/*'` for zero-downtime updates.

## Traffic management & DNS

- **Route 53 hosted zone** (`data.aws_route53_zone.selected`) anchors both API and frontend records.
- **API records** (`aws_route53_record.api`, `.api_ipv6`) alias the Application Load Balancer for IPv4/IPv6 clients with health-evaluated routing.
- **Frontend records** (`aws_route53_record.frontend`, `.frontend_ipv6`) alias CloudFront, letting the CDN terminate TLS near users.
- Provision ACM certificates for both endpoints (`alb_certificate_arn`, `cloudfront_certificate_arn`) prior to deployment.

## Observability & operations

- **Logs**: Backend container logs stream to `/aws/ecs/<project>-<env>-backend` (`aws_cloudwatch_log_group.backend`) with 30-day retention by default (`log_retention_in_days`). CloudFront access logs land in S3 for long-term analysis.
- **Metrics**: ECS/Fargate, ALB, and DocumentDB publish CloudWatch metrics suitable for scaling policies and alarms. Configure dashboards/alarms via additional Terraform modules as needed.
- **Deployments**: Push backend images to the provisioned ECR repository (`ecr_repository_url` output) and rerun `terraform apply` with a new `container_image_tag` or trigger blue/green deploys via CodeDeploy/CodePipeline enhancements.

## Hardening checklist

- Enforce least-privilege IAM by scoping task roles to only required secrets (already applied via `aws_iam_policy.secrets_read`).
- Enable AWS WAF or Shield Advanced on CloudFront/ALB for additional DDoS mitigation in high-risk regions.
- Turn on ALB access logging and additional CloudWatch alarms for 4xx/5xx spikes under heavy load.
- Consider multi-region DR by replicating this stack and using Route 53 failover routing policies.

## Customization pointers

- Adjust CIDR blocks and AZs via `vpc_cidr`, `public_subnet_cidrs`, `private_subnet_cidrs`, and `availability_zones`.
- Tune scaling with `min_capacity`, `max_capacity`, and per-task CPU/memory reservations.
- Swap DocumentDB for Amazon Aurora or DynamoDB by replacing `docdb.tf` and updating backend drivers if workload patterns change.
- Add background workers by creating additional ECS services and Secrets Manager entries following the established patterns.

Refer to `infra/terraform/terraform.tfvars.example` for the minimum configuration needed to instantiate this architecture in your AWS account.
