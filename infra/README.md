# Infrastructure as Code (Terraform)

This directory contains the Terraform configuration to provision the AWS infrastructure for the ShortURL Fullstack application.

## Architecture Overview

The infrastructure is designed for high availability and security, following standard AWS best practices:

- **VPC**: A custom Virtual Private Cloud with public and private subnets across two Availability Zones.
- **Networking**:
  - **Public Subnets**: Host the Load Balancer and NAT Gateway.
  - **Private Subnets**: Host the application servers (EC2) and database.
  - **NAT Gateway**: Allows private instances to access the internet (e.g., for updates) without being exposed to incoming traffic.
- **Compute**:
  - **Application Load Balancer (ALB)**: Distributes incoming API traffic to backend instances.
  - **Auto Scaling Group (ASG)**: Manages EC2 instances running the Express.js backend.
- **Database**:
  - **Amazon DocumentDB**: A managed MongoDB-compatible database cluster (Primary + Replica) for high availability.
- **Frontend & CDN**:
  - **S3 Bucket**: Stores the static assets for the Vue.js frontend.
  - **CloudFront**: A Content Delivery Network (CDN) that serves the frontend from S3 and proxies API requests to the backend ALB.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (v1.0+) installed.
- [AWS CLI](https://aws.amazon.com/cli/) installed and configured with appropriate credentials (`aws configure`).

## Directory Structure

- `provider.tf`: AWS provider configuration.
- `vpc.tf`: VPC, subnets, gateways, and route tables.
- `security_groups.tf`: Security groups for ALB, EC2, and Database.
- `compute.tf`: ALB, Launch Template, and Auto Scaling Group.
- `database.tf`: DocumentDB cluster and subnet group.
- `frontend.tf`: S3 bucket and CloudFront distribution.
- `variables.tf`: Input variables for customization.
- `outputs.tf`: Output values (e.g., Load Balancer URL, CloudFront Domain).

## Deployment Instructions

1.  **Initialize Terraform**:
    Download the required providers and initialize the backend.

    ```bash
    cd infra
    terraform init
    ```

2.  **Review the Plan**:
    See what resources will be created.

    ```bash
    terraform plan
    ```

3.  **Apply the Configuration**:
    Provision the infrastructure.

    ```bash
    terraform apply
    ```

    Type `yes` when prompted to confirm.

4.  **Post-Deployment**:
    - **Frontend Deployment**: Build your Vue.js app (`npm run build`) and sync the `dist` folder to the created S3 bucket:
      ```bash
      aws s3 sync ../frontend/dist s3://<OUTPUT_S3_BUCKET_NAME>
      ```
    - **Backend Deployment**: The current Launch Template in `compute.tf` has a placeholder `user_data` script. You need to update it to clone your repository, install dependencies, and start the server.

## Configuration

You can customize the deployment by modifying `variables.tf` or passing a `terraform.tfvars` file.

| Variable       | Description                    | Default              |
| -------------- | ------------------------------ | -------------------- |
| `aws_region`   | AWS Region to deploy to        | `us-east-1`          |
| `project_name` | Prefix for resource names      | `shorturl-fullstack` |
| `environment`  | Environment tag (dev/prod)     | `dev`                |
| `db_username`  | Master username for DocumentDB | `admin`              |
| `db_password`  | Master password for DocumentDB | `ChangeMe123!`       |

**Security Note**: For production, **DO NOT** keep the database password in `variables.tf`. Pass it as an environment variable or use AWS Secrets Manager.

## Clean Up

To destroy all resources created by this configuration:

```bash
terraform destroy
```
