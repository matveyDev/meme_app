# Build stage
FROM node:20 AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set npm configuration for better reliability
RUN npm config set fetch-retries 5 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm config set engine-strict false

# Copy package files
COPY package*.json ./

# Install dependencies with specific configuration
RUN npm cache clean --force && \
    NODE_OPTIONS="--max-old-space-size=4096" npm install --legacy-peer-deps --force && \
    npm install rpc-websockets@5.0.0 --legacy-peer-deps --force

# Copy source files
COPY . .

# Set build environment variables
ENV NODE_ENV=production
ENV VUE_APP_API_URL=http://localhost:8000

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 