# Eurococ Order Management System

A full-stack application for managing vehicle orders, built with FastAPI (backend) and Vue.js (frontend).

## Features

- Order management (create, read, update, delete)
- Vehicle category management
- Order status tracking
- Advanced filtering and search
- Responsive design

## Tech Stack

- Backend: FastAPI, Python 3.10
- Frontend: Vue.js 3, Vite
- Database: MySQL 8.0
- Containerization: Docker, Docker Compose

## Prerequisites

- Docker
- Docker Compose
- Git

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd eurococ-zadanie
```

2. Create a `.env` file in the root directory with the following content:

```
DATABASE_HOST=db
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=root
DATABASE_NAME=orders_db
VITE_API_URL=http://localhost:8008  # Change this to your server's IP if deploying
```

3. Start the application:

```bash
docker-compose up -d
```

The application will be available at:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8008
- phpMyAdmin: http://localhost:8081

## Development

### Running Tests

```bash
make test
```

### Cleaning Up

```bash
make clean
```

### Rebuilding Containers

```bash
docker-compose up -d --build
```

## Project Structure

- `api/` - Backend FastAPI application
- `web/` - Frontend Vue.js application
- `mysql/` - Database data directory
- `mysql-init/` - Database initialization scripts

## Environment Variables

- `DATABASE_HOST`: Database host (default: db)
- `DATABASE_PORT`: Database port (default: 3306)
- `DATABASE_USER`: Database user (default: root)
- `DATABASE_PASSWORD`: Database password (default: root)
- `DATABASE_NAME`: Database name (default: orders_db)
- `VITE_API_URL`: Frontend API URL (default: http://localhost:8008)

## License

[Your License Here]
