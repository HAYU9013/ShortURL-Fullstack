# Use the official lightweight Node.js image as the base image
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

# Install dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Install runtime utilities required for health checks
RUN apk add --no-cache curl

# Copy application source
COPY . .

# Download the AWS RDS CA bundle for DocumentDB TLS connections
ADD https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem /etc/ssl/certs/rds-combined-ca-bundle.pem

# Expose the port the app runs on
EXPOSE 3000

# Start the production server
CMD ["node", "src/index.js"]
