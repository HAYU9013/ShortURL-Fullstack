# 專案上雲遷移指南 (Migration Guide)

本文件詳細說明將 ShortURL Fullstack 專案部署至 AWS 的完整流程。請依照順序執行。

## 1. 前置準備 (Prerequisites)

確保本機已安裝以下工具：

- **AWS CLI**: 執行 `aws configure` 設定 Credentials 與 Region (建議 `us-east-1`)。
- **Terraform**: 用於部署基礎設施。
- **Docker**: 用於建置後端映像檔。
- **Node.js (v18+)**: 用於前端建置。

---

## 2. 步驟一：部署基礎設施 (Infrastructure)

首先建立 AWS 資源 (VPC, EC2, DocumentDB, S3, CloudFront)。

1.  進入 `infra` 目錄：

    ```bash
    cd infra
    ```

2.  初始化與部署：

    ```bash
    terraform init
    terraform apply
    ```

    - 輸入 `yes` 確認部署。

3.  **記錄輸出資訊 (Outputs)**：
    部署完成後，終端機會顯示綠色的 Outputs，請務必記錄下列數值 (後續步驟會用到)：
    - `alb_dns_name`: 後端 API 位址 (例如: `shorturl-alb-123.us-east-1.elb.amazonaws.com`)
    - `cloudfront_domain_name`: 前端網站位址 (例如: `d12345.cloudfront.net`)
    - `s3_bucket_name`: 存放前端檔案的 Bucket (例如: `shorturl-frontend-bucket`)
    - `docdb_endpoint`: 資料庫連線位址 (例如: `shorturl-docdb.cluster-xyz.us-east-1.docdb.amazonaws.com`)

---

## 3. 步驟二：後端部署 (Backend)

### 2.1 建置與推送 Docker Image

1.  回到專案根目錄。
2.  登入 Docker Hub (或您的 Registry)：
    ```bash
    docker login
    ```
3.  建置並推送 (請將 `your-username` 替換為您的 Docker Hub 帳號)：
    ```bash
    docker build -t your-username/shorturl-backend:latest ./backend
    docker push your-username/shorturl-backend:latest
    ```

### 2.2 修改 Terraform 設定 (`compute.tf`)

我們需要更新 EC2 的啟動腳本 (`user_data`)，注入環境變數並執行 Docker 容器。

1.  開啟 `infra/compute.tf`。
2.  找到 `resource "aws_launch_template" "main"` 中的 `user_data` 區塊。
3.  **將其完全替換為以下內容** (請務必修改 `<...>` 的部分)：

    ```hcl
    user_data = base64encode(<<-EOF
                #!/bin/bash
                # 1. 安裝 Docker
                yum update -y
                amazon-linux-extras install docker -y
                service docker start
                usermod -a -G docker ec2-user

                # 2. 執行後端容器
                # 請替換以下變數值：
                # <DOCDB_ENDPOINT>: 步驟一取得的 docdb_endpoint
                # <CLOUDFRONT_DOMAIN>: 步驟一取得的 cloudfront_domain_name (需加上 https://)
                # your-username/shorturl-backend:latest: 您的 Image 名稱

                docker run -d \
                  --name backend \
                  --restart always \
                  -p 80:3000 \
                  -e PORT=3000 \
                  -e NODE_ENV=production \
                  -e MONGO_URL="mongodb://admin:ChangeMe123!@<DOCDB_ENDPOINT>:27017/shorturl" \
                  -e MONGO_TLS=true \
                  -e MONGO_TLS_CA_FILE=/etc/ssl/certs/rds-combined-ca-bundle.pem \
                  -e MONGO_REPLICA_SET=rs0 \
                  -e MONGO_READ_PREFERENCE=secondaryPreferred \
                  -e MONGO_RETRY_WRITES=false \
                  -e ALLOWED_ORIGINS="http://localhost:5173,https://<CLOUDFRONT_DOMAIN>" \
                  your-username/shorturl-backend:latest
                EOF
    )
    ```

    > **注意**：
    >
    > - `MONGO_URL` 中的帳號密碼 (`admin:ChangeMe123!`) 需與 `infra/variables.tf` 設定一致。
    > - `ALLOWED_ORIGINS` 必須包含 CloudFront 的網址 (加上 `https://`)，否則前端會出現 CORS 錯誤。

### 2.3 更新基礎設施

回到 `infra` 目錄並套用變更：

```bash
cd infra
terraform apply
```

- **重要**：更新 Launch Template 不會自動重啟現有的 EC2。
- 請前往 **AWS Console > EC2**，將現有的 Instance 終止 (Terminate)。
- Auto Scaling Group 會自動啟動新的 Instance，並執行新的 `user_data` 腳本。

---

## 4. 步驟三：前端部署 (Frontend)

### 4.1 設定環境變數

1.  開啟 `frontend/.env` (若無則建立)。
2.  修改 `VITE_API_BASE_URL`，填入步驟一取得的 `alb_dns_name`：

    ```env
    # 注意：ALB 預設為 HTTP (若有設定 HTTPS 則用 https)
    VITE_API_BASE_URL=http://<ALB_DNS_NAME>
    ```

### 4.2 建置與上傳

1.  回到 `frontend` 目錄：
    ```bash
    cd frontend
    npm install
    npm run build
    ```
2.  同步檔案至 S3 (使用步驟一取得的 `s3_bucket_name`)：
    ```bash
    aws s3 sync ./dist s3://<S3_BUCKET_NAME>
    ```

### 4.3 清除 CDN 快取

為了確保使用者讀取到最新的 index.html：

```bash
# 需先查詢 CloudFront Distribution ID (可由 AWS Console 查看)
aws cloudfront create-invalidation --distribution-id <DISTRIBUTION_ID> --paths "/*"
```

---

## 5. 步驟四：資料庫初始化 (Database Seed)

DocumentDB 位於私有網路，需透過 EC2 執行初始化。

1.  **連線至 EC2**：

    - 進入 AWS Console > EC2。
    - 選取一台 Backend Instance，點擊 **Connect** > **Session Manager** > **Connect**。

2.  **執行 Seed**：

    - 在終端機中輸入：

      ```bash
      # 進入容器
      docker exec -it backend sh

      # 執行 Seed 腳本
      npm run seed
      ```

    - 若顯示 "MongoDB connected" 與 "Data imported"，即表示成功。

---

## 6. 驗證 (Verification)

1.  打開瀏覽器。
2.  輸入 `https://<CLOUDFRONT_DOMAIN>`。
3.  測試註冊、登入與縮網址功能。

---

## 附錄：環境變數總表

### Backend (Docker 執行時傳入)

| 變數名稱            | 說明                | 範例值                                      |
| :------------------ | :------------------ | :------------------------------------------ |
| `PORT`              | 服務 Port           | `3000`                                      |
| `NODE_ENV`          | 環境                | `production`                                |
| `MONGO_URL`         | 連線字串 (不含參數) | `mongodb://user:pass@host:27017/db`         |
| `MONGO_TLS`         | 啟用 TLS            | `true`                                      |
| `MONGO_TLS_CA_FILE` | CA 憑證路徑         | `/etc/ssl/certs/rds-combined-ca-bundle.pem` |
| `MONGO_REPLICA_SET` | Replica Set 名稱    | `rs0`                                       |
| `ALLOWED_ORIGINS`   | 允許的 CORS 來源    | `https://d123.cloudfront.net`               |

### Frontend (.env)

| 變數名稱            | 說明          | 範例值                                  |
| :------------------ | :------------ | :-------------------------------------- |
| `VITE_API_BASE_URL` | 後端 API 位址 | `http://shorturl-alb-....amazonaws.com` |
