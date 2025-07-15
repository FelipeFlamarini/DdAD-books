#!/bin/bash

echo "Stopping all production services..."
docker-compose -f docker-compose.prod.yml down

echo "Removing containers, networks, and volumes..."
docker-compose -f docker-compose.prod.yml down -v

echo "Cleaning up unused Docker resources..."
docker system prune -f

echo "All production services stopped and cleaned up."