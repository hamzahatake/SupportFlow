# Database Setup Guide

This guide explains how to set up the database for the SupportFlow project.

## Quick Start (SQLite - Recommended for Development)

The easiest way to get started is with SQLite:

```bash
# Set environment variable and run migrations
$env:USE_SQLITE="1"
python manage.py makemigrations
python manage.py migrate
```

## PostgreSQL Options

### Option 1: Docker (Recommended)

1. **Install Docker Desktop** from https://www.docker.com/products/docker-desktop/

2. **Start PostgreSQL with Docker**:
   ```bash
   docker-compose up -d db
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Stop PostgreSQL** (when done):
   ```bash
   docker-compose down
   ```

### Option 2: Local PostgreSQL Installation

1. **Download PostgreSQL** from https://www.postgresql.org/download/windows/

2. **Install and set password** for the `postgres` user

3. **Create database**:
   ```sql
   CREATE DATABASE supportdb;
   ```

4. **Update settings** in `support_dashboard/settings.py` if needed:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'supportdb',
           'USER': 'postgres',
           'PASSWORD': 'your_password_here',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Using the Setup Script

Run the interactive setup script:

```bash
python setup_database.py
```

This will guide you through the database setup process.

## Environment Variables

- `USE_SQLITE=1` - Use SQLite instead of PostgreSQL
- `POSTGRES_DB` - PostgreSQL database name
- `POSTGRES_USER` - PostgreSQL username
- `POSTGRES_PASSWORD` - PostgreSQL password
- `POSTGRES_HOST` - PostgreSQL host
- `POSTGRES_PORT` - PostgreSQL port

## Current Status

✅ **PostgreSQL with Docker is currently configured and working**
- Database: PostgreSQL 15 running in Docker
- Host: localhost:5432
- Database Name: supportdb
- Migrations: Applied successfully
- JWT token blacklist: Ready
- Superuser: admin@supportflow.com / admin123

## Next Steps

1. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

2. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the admin panel** at http://127.0.0.1:8000/admin/
