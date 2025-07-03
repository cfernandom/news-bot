# Multi-stage build for React Dashboard
FROM node:22-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies (including dev for build)
RUN npm ci

# Copy source code and configuration files
COPY src/ ./src/
COPY public/ ./public/
COPY *.json ./
COPY *.js ./
COPY *.ts ./
COPY *.html ./
COPY tailwind.config.js vite.config.ts tsconfig*.json ./
COPY .env.production* ./

# Set production environment
RUN if [ -f .env.production ]; then \
        cp .env.production .env; \
    else \
        cp .env.production.template .env; \
    fi

# Verify environment is correct
RUN cat .env

# Build the application
RUN npm run build

# Production stage
FROM nginx:1.27-alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
