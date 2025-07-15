#!/bin/bash

# Build all Docker images
echo "Building Docker images..."
docker-compose build

# Start all services
echo "Starting all services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check service status
echo "Checking service status..."
docker-compose ps

echo "Services are starting up. You can check logs with:"
echo "  docker-compose logs -f api"
echo "  docker-compose logs -f email-worker"
echo "  docker-compose logs -f notification-worker"

echo "API will be available at: http://localhost:8000"
echo "RabbitMQ management at: http://localhost:15672 (guest/guest)"