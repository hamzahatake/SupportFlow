#!/usr/bin/env python
"""
Database setup script for SupportFlow project.
Run this script to set up your database environment.
"""

import os
import subprocess
import sys

def setup_sqlite():
    """Set up SQLite database for development."""
    print("Setting up SQLite database...")
    os.environ['USE_SQLITE'] = '1'
    
    # Run migrations
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
    
    print("✅ SQLite database setup complete!")

def setup_postgresql_docker():
    """Set up PostgreSQL using Docker."""
    print("Setting up PostgreSQL with Docker...")
    
    # Check if Docker is running
    try:
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not running. Please install Docker Desktop.")
        return False
    
    # Start PostgreSQL container
    subprocess.run(['docker-compose', 'up', '-d', 'db'], check=True)
    
    # Wait for database to be ready
    print("Waiting for PostgreSQL to be ready...")
    import time
    time.sleep(10)
    
    # Run migrations
    os.environ.pop('USE_SQLITE', None)  # Remove SQLite flag
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
    
    print("✅ PostgreSQL database setup complete!")
    return True

def main():
    print("SupportFlow Database Setup")
    print("=" * 30)
    print("1. SQLite (Quick setup for development)")
    print("2. PostgreSQL with Docker")
    print("3. Exit")
    
    choice = input("\nSelect an option (1-3): ").strip()
    
    if choice == '1':
        setup_sqlite()
    elif choice == '2':
        setup_postgresql_docker()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
