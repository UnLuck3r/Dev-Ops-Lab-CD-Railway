.PHONY: help setup build up down logs test clean

help:
	@echo "===== Fullstack Application Makefile ====="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - Set up the project (create .env files)"
	@echo "  make build          - Build Docker images"
	@echo "  make up             - Start all services with Docker Compose"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - View Docker Compose logs"
	@echo "  make logs-backend   - View backend logs only"
	@echo "  make logs-frontend  - View frontend logs only"
	@echo "  make logs-db        - View database logs only"
	@echo "  make test           - Run backend tests"
	@echo "  make test-watch     - Run tests in watch mode"
	@echo "  make clean          - Clean up Docker containers and volumes"
	@echo "  make ps             - Show running containers"
	@echo "  make restart        - Restart all services"
	@echo ""

setup:
	@echo "Setting up environment files..."
	@cp backend/.env.example backend/.env 2>/dev/null || echo "backend/.env already exists"
	@cp frontend/.env.example frontend/.env 2>/dev/null || echo "frontend/.env already exists"
	@echo "✅ Setup complete!"

build:
	@echo "Building Docker images..."
	docker-compose build
	@echo "✅ Build complete!"

up:
	@echo "Starting all services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo ""
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:5000"
	@echo "Database: localhost:5432"
	@echo ""

down:
	@echo "Stopping all services..."
	docker-compose down
	@echo "✅ Services stopped!"

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f postgres

ps:
	docker-compose ps

test:
	@echo "Running backend tests..."
	docker-compose exec backend python -m pytest test_app.py -v

test-watch:
	@echo "Running backend tests in watch mode..."
	docker-compose exec backend python -m pytest test_app.py -v --tb=short -s

clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	@echo "✅ Clean complete!"

restart:
	@echo "Restarting all services..."
	docker-compose restart
	@echo "✅ Services restarted!"

# Backend specific commands
backend-shell:
	docker-compose exec backend bash

backend-python:
	docker-compose exec backend python

# Frontend specific commands
frontend-shell:
	docker-compose exec frontend sh

# Database specific commands
db-shell:
	docker-compose exec postgres psql -U fullstack_user -d fullstack_db

# Development setup without Docker
dev-setup:
	@echo "Setting up local development environment..."
	@echo "Backend setup..."
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Frontend setup..."
	cd frontend && npm install
	@echo "✅ Development setup complete!"

# Install dependencies
install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

# Local run (without Docker)
run-backend:
	cd backend && flask run

run-frontend:
	cd frontend && npm start

# Help aliases
.PHONY: h
h: help

# Default target
.DEFAULT_GOAL := help
