# Docker Commands for SupportFlow

This file contains all the essential Docker commands for running Django operations within containers.

## 🐳 Basic Docker Operations

### Start/Stop Services
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Start only database services
docker-compose up -d db redis

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild containers
docker-compose up --build
```

### Check Service Status
```bash
# List running containers
docker-compose ps

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs web
docker-compose logs db
docker-compose logs redis

# Follow logs in real-time
docker-compose logs -f web
```

## 🔧 Django Commands in Docker

### Method 1: Execute Commands in Running Container
```bash
# Run makemigrations
docker-compose exec web python manage.py makemigrations

# Run migrate
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test

# Collect static files
docker-compose exec web python manage.py collectstatic

# Check Django status
docker-compose exec web python manage.py check

# Show migrations
docker-compose exec web python manage.py showmigrations
```

### Method 2: One-time Command Execution
```bash
# Run makemigrations (creates container, runs command, removes container)
docker-compose run --rm web python manage.py makemigrations

# Run migrate
docker-compose run --rm web python manage.py migrate

# Create superuser
docker-compose run --rm web python manage.py createsuperuser

# Run tests
docker-compose run --rm web python manage.py test

# Run specific app tests
docker-compose run --rm web python manage.py test users
docker-compose run --rm web python manage.py test tickets

# Load sample data
docker-compose run --rm web python manage.py loaddata fixtures/sample_data.json

# Dump data
docker-compose run --rm web python manage.py dumpdata > backup.json
```

### Method 3: Interactive Shell Access
```bash
# Get bash shell access
docker-compose exec web bash

# Get Python shell access
docker-compose exec web python manage.py shell

# Get Django shell with IPython
docker-compose exec web python manage.py shell_plus
```

## 🗄️ Database Operations in Docker

### PostgreSQL Commands
```bash
# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d supportdb

# Backup database
docker-compose exec db pg_dump -U postgres supportdb > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres supportdb < backup.sql

# Create database
docker-compose exec db createdb -U postgres new_database

# Drop database
docker-compose exec db dropdb -U postgres database_name
```

### Redis Commands
```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# Check Redis status
docker-compose exec redis redis-cli ping

# Monitor Redis commands
docker-compose exec redis redis-cli monitor

# Clear Redis cache
docker-compose exec redis redis-cli flushall
```

## 🚀 Development Workflow

### Complete Development Setup
```bash
# 1. Start all services
docker-compose up -d

# 2. Run migrations
docker-compose exec web python manage.py migrate

# 3. Create superuser (if needed)
docker-compose exec web python manage.py createsuperuser

# 4. Run development server
docker-compose up web
```

### Daily Development Commands
```bash
# Start your day
docker-compose up -d

# Run migrations if needed
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Run tests
docker-compose exec web python manage.py test

# Check code quality
docker-compose exec web python manage.py check

# End of day
docker-compose down
```

## 🔍 Debugging Commands

### Container Debugging
```bash
# Inspect container
docker-compose exec web env

# Check container logs
docker-compose logs web --tail=50

# Access container filesystem
docker-compose exec web ls -la

# Check Python packages
docker-compose exec web pip list

# Check Django version
docker-compose exec web python -c "import django; print(django.get_version())"
```

### Database Debugging
```bash
# Check database connection
docker-compose exec web python manage.py dbshell

# Show database tables
docker-compose exec db psql -U postgres -d supportdb -c "\dt"

# Check migration status
docker-compose exec web python manage.py showmigrations

# Validate models
docker-compose exec web python manage.py validate
```

## 🧪 Testing Commands

### Run Tests
```bash
# Run all tests
docker-compose exec web python manage.py test

# Run with coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
docker-compose exec web coverage html

# Run specific test
docker-compose exec web python manage.py test users.tests.TestUserModel

# Run tests with verbose output
docker-compose exec web python manage.py test --verbosity=2
```

## 📦 Package Management

### Install/Update Packages
```bash
# Install new package
docker-compose exec web pip install package_name

# Update requirements.txt
docker-compose exec web pip freeze > requirements.txt

# Install from requirements.txt
docker-compose exec web pip install -r requirements.txt

# Check outdated packages
docker-compose exec web pip list --outdated
```

## 🔄 Backup and Restore

### Database Backup
```bash
# Create backup
docker-compose exec db pg_dump -U postgres supportdb > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker-compose exec -T db psql -U postgres supportdb < backup_file.sql

# Create Django fixture backup
docker-compose exec web python manage.py dumpdata > fixtures/backup_$(date +%Y%m%d_%H%M%S).json
```

## 🚨 Troubleshooting

### Common Issues
```bash
# Restart specific service
docker-compose restart web

# Rebuild specific service
docker-compose up --build web

# Remove and recreate containers
docker-compose down
docker-compose up --build

# Check container health
docker-compose ps
docker-compose logs web --tail=20
```

### Clean Up
```bash
# Remove unused containers
docker-compose down --remove-orphans

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Complete cleanup
docker system prune -a
```

## 📋 Quick Reference

| Task | Command |
|------|---------|
| Start services | `docker-compose up -d` |
| Stop services | `docker-compose down` |
| Run migrations | `docker-compose exec web python manage.py migrate` |
| Create superuser | `docker-compose exec web python manage.py createsuperuser` |
| Run tests | `docker-compose exec web python manage.py test` |
| Access shell | `docker-compose exec web bash` |
| View logs | `docker-compose logs web` |
| Restart service | `docker-compose restart web` |

## 🎯 Environment Variables

### Docker Environment
```bash
# Set environment variables for Docker
export POSTGRES_DB=supportdb
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password
export POSTGRES_HOST=db
export POSTGRES_PORT=5432
export REDIS_URL=redis://redis:6379/0
export DEBUG=True
```

### Windows PowerShell
```powershell
# Set environment variables
$env:POSTGRES_DB="supportdb"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="password"
$env:POSTGRES_HOST="db"
$env:POSTGRES_PORT="5432"
$env:REDIS_URL="redis://redis:6379/0"
$env:DEBUG="True"
```

---

**💡 Tip**: Use `docker-compose exec` for commands in running containers and `docker-compose run --rm` for one-time commands that don't need a persistent container.
