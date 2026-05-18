# Multi-stage build for fullstack app

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/src ./src

# Stage 2: Build backend
FROM python:3.11-slim AS backend-builder
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app.py .

# Stage 3: Final image with both services
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    postgresql-client \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy frontend
COPY --from=frontend-builder /app/frontend /app/frontend

# Copy backend
COPY --from=backend-builder /app/backend /app/backend

# Install Node.js in final image for frontend
RUN cd /app/frontend && npm ci --only=production

# Expose ports
EXPOSE 5000 3000

# Set environment variables
ENV FLASK_APP=/app/backend/app.py
ENV PORT=5000

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app/backend && python -m gunicorn --bind 0.0.0.0:5000 --timeout 60 app:app &\n\
cd /app/frontend && npm start\n\
wait' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
