# Use a lightweight Node image (adjust version as needed)
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN npm install

# Install crypto module
RUN npm install crypto

# Expose dev server port if needed (often 3000 or 5173)
EXPOSE 5173

# Start development mode
CMD ["npm", "run", "dev"]
