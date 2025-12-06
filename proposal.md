介紹
1. 背景知識

隨著行動裝置與社群平台普及，能夠快速產生易於分享的短網址已成為產品推廣、內容行銷與事件追蹤的重要基礎設施。本專案「ShortURL Fullstack」提供一套自我管理的縮網址解決方案，整合 Vue 3 + Vite 建置的前端介面、Express.js 撰寫的 RESTful API，以及 MongoDB 相容的資料層，讓團隊能以開源方式掌握整個生命週期。為了符合企業級維運需求，系統搭配雲端原生的日誌、壓縮、CORS、身分驗證與健康檢查設計，確保在地端開發與雲端佈署之間的操作體驗一致。

2. 目標

本期專題的核心目標是交付一套可從本機快速啟動、並可平順切換至 AWS 正式環境的縮網址平台。我們將著重於三大面向：
- **可靠性**：以 Docker Compose 與 AWS ECS Fargate 提供一致的容器化執行環境，並透過健康檢查端點與集中化日誌保護服務穩定性。
- **安全性**：導入 JWT Cookie 驗證流程、細緻的 CORS 控制與 HTTPS（ACM 憑證 + CloudFront）來守護使用者資料。
- **可維運性**：藉由 Terraform 自動化建立 VPC、Route 53、DocumentDB 與 S3/CloudFront，讓部署、擴充與回滾流程具備版本控管與可追蹤性。

市場調查與使用者

多數商業縮網址服務（如 Bitly、Rebrandly）雖提供即時分析，但成本與資料主權常是企業或校園團隊的顧慮。ShortURL Fullstack 以開源、可自架為核心，特別適合以下族群：
- **成長型團隊**：需要與既有系統整合或自訂權限控管的行銷／產品團隊。
- **開發與 DevOps 團隊**：希望在內網或特定區域內部署，兼顧安全性與審核流程。
- **教育單位與社群**：需要低成本、可自由調整介面與流程的學習或活動平台。
我們透過現有使用者回饋，聚焦改善登入整合、個人網址清單維護與刪除流程，提升日常操作效率。

心智圖

核心概念可整理為：
- 縮網址服務
  - 使用者註冊／登入
  - 短網址產生與導向
  - 我的網址清單與刪除
- 平台維運
  - Docker 本機環境
  - AWS 容器與 CDN 佈署
  - 監控與健康檢查
- 資料與安全
  - DocumentDB／MongoDB 儲存
  - JWT + Cookie 授權
  - CORS／Helmet／Pino 日誌

產品功能說明
1. 開發技術
   a. Backend API

   - 使用 Express.js 建立 RESTful API，包含 `/api/url/shorten` 匿名縮址、`/api/url/u/shorten` 登入後縮址、`/api/url/my-urls` 取得個人清單與 `/api/url/d/:short_id` 刪除功能。
   - 採用 `helmet`、`compression`、`pino-http`、集中化錯誤處理與 `/healthz` 健康檢查確保服務在高流量下仍穩定。
   - 導入 JWT Cookie 驗證與客製化 CORS 白名單，支援多個前端網域安全訪問。

   b. NoSQL 資料庫

   - 以 MongoDB 模型儲存 `long_url`、`short_id`、`username` 等欄位，可直接對接 AWS DocumentDB。
   - 透過 Terraform 建立 TLS 啟用的 DocumentDB 叢集，並使用 Secrets Manager 管理連線字串，兼顧安全與維運。

   c. 前端應用

   - 使用 Vue 3 + Vite 與組件化設計，提供縮址表單（`ShortenUrl.vue`）、個人列表（`UrlList.vue`）、登入／註冊頁面等介面。
   - 透過 `fetch` 與 `axios` 呼叫後端 API，支援帶入認證 Cookie 與刪除確認提示，並以 Bootstrap 風格強化使用者體驗。

   d. 基礎建設與測試

   - `infra/terraform` 封裝 VPC、ECS、ALB、S3、CloudFront、Route 53 佈署腳本，支援從 `terraform plan` 到 `apply` 的自動化流程。
   - `testing/selenium_test` 提供端對端冒煙測試腳本，確保主要瀏覽情境可在瀏覽器中順利操作。

2. Web 應用功能
   a. 縮網址流程

   - 支援匿名與登入兩種流程，登入後會自動綁定使用者名稱以利後續管理。
   - 每次成功建立短網址即時回傳完整可點擊連結，便於社群分享或內部溝通。

   b. 使用者帳號管理

   - 提供註冊、登入、登出與變更密碼 API，登入後於前端顯示個人化問候與快捷操作。
   - JWT Token 設定過期時間與 Cookie 安全旗標，減少 CSRF 與會期遭竊風險。

   c. 我的網址清單

   - 前端 `UrlList` 組件會自動載入登入使用者的所有短網址並提供刪除操作。
   - 刪除流程包含前端確認視窗與後端權限檢查，避免誤刪或跨帳號存取。

   d. 系統觀測

   - 透過健康檢查與伺服器端日誌，可在 AWS CloudWatch 或本機主控台快速追蹤狀態。
   - 支援於 Terraform Stack 中設定自動化擴充門檻，應對行銷活動期間的尖峰流量。

系統架構

系統分為本機開發與雲端佈署兩層：在本機，Docker Compose 啟動 Express 後端與 MongoDB，再以獨立容器跑 Vue 前端；在雲端，Terraform 建立 VPC 與子網路，並以 ECS Fargate 執行容器化後端、DocumentDB 提供資料儲存、S3 + CloudFront 發佈靜態前端，同時由 Route 53 與 ACM 管理公開網域與 TLS 憑證。應用負載均衡器（ALB）提供 `/healthz` 檢查與自動擴縮能力，確保服務在高負載下仍可用。
