FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production

# Install dependencies using package-lock.json for reproducible builds
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Copy source code, views and public assets
COPY src/ ./src/
COPY views/ ./views/
COPY public/ ./public/

# Setup logs directory with proper non-root permissions
RUN mkdir -p /app/logs && chown -R node:node /app

# Switch to unprivileged non-root user (UID 1000)
USER node

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/health || exit 1

CMD ["node", "src/server.js"]
