@echo off
echo Task Management API - Docker Helper Script
echo ==========================================

:menu
echo.
echo Choose an option:
echo 1. Build and run with Docker Compose (Production)
echo 2. Build and run with Docker Compose (Development with hot-reload)
echo 3. Stop all services
echo 4. View logs
echo 5. Clean up (remove containers and volumes)
echo 6. Build Docker image only
echo 7. Setup database tables
echo 8. Exit
echo.

set /p choice=Enter your choice (1-8): 

if "%choice%"=="1" goto prod
if "%choice%"=="2" goto dev
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto build
if "%choice%"=="7" goto setup_db
if "%choice%"=="8" goto exit
goto menu

:prod
echo Building and starting production services...
docker-compose up --build -d
echo.
echo Services started! Access the API at: http://localhost:8000/docs
goto menu

:dev
echo Building and starting development services with hot-reload...
docker-compose -f docker-compose.dev.yml up --build
goto menu

:stop
echo Stopping all services...
docker-compose down
docker-compose -f docker-compose.dev.yml down
goto menu

:logs
echo Viewing application logs...
docker-compose logs -f app
goto menu

:cleanup
echo Cleaning up containers, volumes, and images...
docker-compose down -v
docker-compose -f docker-compose.dev.yml down -v
docker system prune -f
echo Cleanup complete!
goto menu

:build
echo Building Docker image...
docker build -t task-management-api .
echo Build complete!
goto menu

:setup_db
echo Setting up database tables...
docker-compose exec app python setup_database.py
echo Database setup complete!
goto menu

:exit
echo Goodbye!
exit
