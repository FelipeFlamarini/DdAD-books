#!/bin/bash

# Build all Docker images for production
echo "Building Docker images for production..."
docker-compose -f docker-compose.prod.yml build

# Start all services
echo "Starting all services in production mode..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 15

# Check service status
echo "Checking service status..."
docker-compose -f docker-compose.prod.yml ps

echo "Production services are starting up. You can check logs with:"
echo "  docker-compose -f docker-compose.prod.yml logs -f api"
echo "  docker-compose -f docker-compose.prod.yml logs -f email-worker"
echo "  docker-compose -f docker-compose.prod.yml logs -f notification-worker"

echo "API will be available at: http://localhost:8000"
echo "RabbitMQ management at: http://localhost:15672 (guest/guest)"