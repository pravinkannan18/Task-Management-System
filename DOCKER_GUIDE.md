# Docker Build and Deployment Guide

## Prerequisites
- Docker Desktop installed on your machine
- Docker Compose (comes with Docker Desktop)

## Method 1: Using Docker Compose (Recommended)

### Step 1: Update Environment Variables
Before building, update the `docker-compose.yml` file with your actual Gmail App Password:

```yaml
environment:
  - SMTP_PASSWORD=your_actual_16_char_app_password
```

### Step 2: Build and Run with Docker Compose
```bash
# Navigate to project directory
cd "P:\My_Project\Task Management API"

# Build and start all services (database, redis, and app)
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d

# To stop the services
docker-compose down

# To rebuild after code changes
docker-compose up --build --force-recreate
```

### Step 3: Access the Application
- API Documentation: http://localhost:8000/docs
- API Base URL: http://localhost:8000
- Database: localhost:5432 (accessible from host)

## Method 2: Using Docker Build Only

### Step 1: Build the Docker Image
```bash
# Navigate to project directory
cd "P:\My_Project\Task Management API"

# Build the Docker image
docker build -t task-management-api .

# Or with a specific tag
docker build -t task-management-api:v1.0 .
```

### Step 2: Run PostgreSQL Database Separately
```bash
# Run PostgreSQL container
docker run -d \
  --name postgres-db \
  -e POSTGRES_DB=task_management \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin \
  -p 5432:5432 \
  postgres:15
```

### Step 3: Run the Application
```bash
# Run the application container
docker run -d \
  --name task-management-app \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:admin@host.docker.internal:5432/task_management \
  -e SECRET_KEY=a7816f7f9f1d85dd1abb294491cec98f26dd9ad8704573678c393e85143382bf \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USER=pravinkannan18@gmail.com \
  -e SMTP_PASSWORD=your_16_char_app_password \
  task-management-api
```

## Method 3: Development with Docker

### For development with hot-reload:
```bash
# Use docker-compose with volume mounting
docker-compose -f docker-compose.dev.yml up --build
```

## Common Docker Commands

### View running containers
```bash
docker ps
```

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs app
docker-compose logs postgres

# Follow logs
docker-compose logs -f app
```

### Access container shell
```bash
# Access app container
docker-compose exec app bash

# Access database container
docker-compose exec postgres psql -U postgres -d task_management
```

### Clean up
```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove images
docker rmi task-management-api

# Clean up everything
docker system prune -a
```

## Database Migration in Docker

### Run database setup
```bash
# Execute inside the running container
docker-compose exec app python setup_database.py

# Or run as a one-time container
docker-compose run --rm app python setup_database.py
```

## Production Deployment

### Build for production
```bash
# Build optimized image
docker build -t task-management-api:prod --target production .

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Check container health
```bash
docker-compose ps
```

### View detailed logs
```bash
docker-compose logs app
```

### Restart specific service
```bash
docker-compose restart app
```

### Database connection issues
```bash
# Check if database is ready
docker-compose exec postgres pg_isready -U postgres
```

## Environment Variables for Docker

Make sure these are set in your `docker-compose.yml` or `.env` file:

```yaml
environment:
  - DATABASE_URL=postgresql://postgres:admin@postgres:5432/task_management
  - SECRET_KEY=your-secret-key-here
  - SMTP_HOST=smtp.gmail.com
  - SMTP_PORT=587
  - SMTP_USER=your-email@gmail.com
  - SMTP_PASSWORD=your-app-password
  - ENABLE_CELERY=false
```
