# 選用 Node 輕量版映像檔 (根據你的 Node 版本需求調整)
FROM node:18-alpine

# 設定工作目錄
WORKDIR /app

# 複製專案所有檔案
COPY . .

# 安裝相依套件
RUN npm install

# 安裝 crypto 模塊
RUN npm install crypto

# 如有需要，暴露開發伺服器的 port (預設 vite dev 可能是 3000 或 5173，請依照實際情況調整)
EXPOSE 5173

# 啟動開發模式
CMD ["npm", "run", "dev"]