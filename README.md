# ShortURL Fullstack

Full-stack URL shortener featuring a Vue 3 frontend, Express backend, and MongoDB-compatible database. The repository now includes a production-ready AWS stack focused on running smoothly under heavy traffic.

---

## Technology overview

| Layer | Local tool | Production service |
| --- | --- | --- |
| Frontend | Vue 3 + Vite | Amazon S3 + CloudFront |
| Backend | Express.js | Amazon ECS (Fargate) |
| Database | MongoDB (Docker) | Amazon DocumentDB |
| Networking | Docker Compose | Amazon VPC + Route 53 |

---

## From zero to running locally

These steps walk you from an empty machine to a working local development environment.

### 1. Install prerequisites

| Tool | Windows | macOS | Linux |
| --- | --- | --- | --- |
| Git | [Download](https://git-scm.com/download/win) | `brew install git` | `sudo apt install git` (Debian/Ubuntu) |
| Node.js 18+ & npm | [Download LTS](https://nodejs.org/en/download/) | `brew install node@18` | `sudo apt install nodejs npm` |
| Docker Engine | [Docker Desktop](https://www.docker.com/products/docker-desktop/) | [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Follow the [official engine docs](https://docs.docker.com/engine/install/) |
| Docker Compose | Bundled with Docker Desktop | Bundled with Docker Desktop | Install per [docs](https://docs.docker.com/compose/install/) if not available |

> **Tip:** On Windows, enable the “Use WSL 2 based engine” option in Docker Desktop for best performance.

### 2. Clone the repository

```bash
git clone https://github.com/<your-org>/ShortURL-Fullstack.git
cd ShortURL-Fullstack
```

### 3. Configure environment variables

Create a `backend/.env.local` file for local development to override defaults used by Docker Compose when running outside containers:

```bash
cat <<'ENV' > backend/.env.local
MONGO_URL=mongodb://localhost:27017/UsersData
Base_URL=http://localhost
Expose_PORT=8000
ALLOWED_ORIGINS=http://localhost:5173
ENV
```

You can load the variables with `export $(cat backend/.env.local | xargs)` on macOS/Linux or `Get-Content backend/.env.local | Foreach-Object { $name, $value = $_ -split '='; Set-Item -Path Env:\$name -Value $value }` in PowerShell when running the backend without Docker.

### 4. Start the stack

#### Windows (PowerShell or CMD)

```powershell
./run.bat
```

The script launches the backend, MongoDB, and frontend containers, then opens [http://localhost:5173](http://localhost:5173).

#### macOS/Linux

```bash
cd backend
docker compose up --build -d
cd ../frontend
docker build -t url-shortener-frontend --build-arg NAME=frontend .
docker run -d -p 5173:5173 --name url-shortener-frontend url-shortener-frontend
```

Stop the containers with `docker compose down` (backend) and `docker rm -f url-shortener-frontend` when finished.

### 5. Develop and test

- Backend source: `backend/src`
- Frontend source: `frontend/src`
- Selenium smoke test:
  ```bash
  cd testing/selenium_test
  pip install selenium
  python main.py
  ```

---

## From zero to production on AWS

The `infra/terraform` directory contains an opinionated Terraform stack to provision everything required to run the application at scale.

### 1. Install and configure tooling

1. Install the following:
   - [Terraform ≥ 1.5](https://developer.hashicorp.com/terraform/downloads)
   - [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
   - Docker (already installed from the local setup steps)
2. Configure AWS credentials for an IAM user/role with permissions for VPC, ECS, ECR, Secrets Manager, CloudFront, ACM, Route 53, and DocumentDB:
   ```bash
   aws configure
   ```
3. Ensure you have the following resources ready:
   - A Route 53 hosted zone for your domain.
   - An ACM certificate in your deployment region for the API load balancer.
   - An ACM certificate in `us-east-1` for CloudFront.

### 2. Understand the architecture

| Layer | Service | Notes |
| --- | --- | --- |
| Networking | Amazon VPC | Two public and two private subnets across AZs, internet gateway, and NAT. |
| Compute | Amazon ECS on Fargate | Backend tasks run behind an Application Load Balancer with auto-scaling policies. |
| Data | Amazon DocumentDB | TLS-enabled cluster with automated backups and secrets stored in AWS Secrets Manager. |
| Delivery | Amazon S3 + CloudFront | Hosts and accelerates the static Vue frontend globally. |
| Traffic management | Amazon Route 53 | Routes API traffic to the ALB and web traffic to CloudFront with health checks. |

### 3. Create Terraform variables

1. Copy the example variables file:
   ```bash
   cd infra/terraform
   cp terraform.tfvars.example terraform.tfvars
   ```
2. Fill in the required values (`project_name`, `aws_region`, `route53_zone_id`, certificate ARNs, CIDR blocks, etc.). Refer to `variables.tf` for full descriptions.

### 4. Provision the infrastructure

```bash
terraform init
terraform plan
terraform apply
```

Terraform outputs the following key values:

- `ecr_repository_url` – push backend images here.
- `frontend_bucket_name` – upload built frontend assets here.
- `alb_dns_name` – API endpoint (Route 53 CNAME target).
- `cloudfront_domain_name` – Frontend CDN endpoint.

### 5. Deploy application artifacts

1. Build, tag, and push the backend image:
   ```bash
   cd ../../backend
   docker build -t shorturl-backend:latest .
   aws ecr get-login-password --region <aws_region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<aws_region>.amazonaws.com
   docker tag shorturl-backend:latest <ecr_repository_url>:latest
   docker push <ecr_repository_url>:latest
   ```
   Update the `container_image_tag` variable if you push a tag other than `latest`.
2. Build the frontend and upload it to S3:
   ```bash
   cd ../frontend
   npm install
   npm run build
   aws s3 sync dist/ s3://<frontend_bucket_name>/ --delete
   aws cloudfront create-invalidation --distribution-id <distribution_id> --paths '/*'
   ```

### 6. Configure DNS and post-provision checks

1. In Route 53, create records pointing your chosen domain(s) to the `alb_dns_name` (API) and `cloudfront_domain_name` (frontend).
2. Verify health checks at `/healthz` respond with HTTP 200 via the ALB.
3. Monitor CloudWatch metrics for ECS service scaling and DocumentDB performance under load.

> **Note:** DocumentDB deletion protection is enabled by default. Disable it in the AWS Console before destroying the stack if you ever need to tear the cluster down.
