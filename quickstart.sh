#!/bin/bash

# Quick Start Script for Fullstack Application
# This script sets up and starts the application locally

set -e

echo "======================================"
echo "  Fullstack App - Quick Start Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker from https://www.docker.com"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Please install Docker Compose"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"
echo ""

# Create environment files
echo -e "${YELLOW}Creating environment files...${NC}"
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✅ Created backend/.env${NC}"
else
    echo -e "${YELLOW}⚠️  backend/.env already exists${NC}"
fi

if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✅ Created frontend/.env${NC}"
else
    echo -e "${YELLOW}⚠️  frontend/.env already exists${NC}"
fi

echo ""

# Build Docker images
echo -e "${YELLOW}Building Docker images...${NC}"
docker-compose build --quiet
echo -e "${GREEN}✅ Docker images built${NC}"
echo ""

# Start services
echo -e "${YELLOW}Starting services...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Services started${NC}"
echo ""

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Check if services are running
echo ""
echo -e "${YELLOW}Checking service status...${NC}"
docker-compose ps
echo ""

# Display access information
echo ""
echo "======================================"
echo -e "${GREEN}✅ Application is ready!${NC}"
echo "======================================"
echo ""
echo "📱 Frontend:    http://localhost:3000"
echo "🔌 Backend API: http://localhost:5000"
echo "📊 Database:    localhost:5432"
echo ""
echo "📝 Useful commands:"
echo "   docker-compose logs -f           # View logs"
echo "   docker-compose down              # Stop all services"
echo "   make test                        # Run backend tests"
echo ""
echo "Documentation: See README.md for detailed information"
echo "======================================"
