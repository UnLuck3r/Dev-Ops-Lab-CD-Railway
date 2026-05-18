# Use Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production

# Copy source files
COPY src ./src

# Expose port 3000
EXPOSE 3000

# Set environment variable
ENV REACT_APP_API_URL=https://YOUR_BACKEND_URL/api

# Start the server
CMD ["npm", "start"]
