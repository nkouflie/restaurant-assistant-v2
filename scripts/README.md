# Development Scripts

This directory contains helpful scripts for managing the Restaurant Assistant development environment.

## Available Scripts

### `dev.sh` - Full Development Setup
Complete development environment setup with all checks.

```bash
./scripts/dev.sh
```

**What it does:**
- ✅ Checks for `.env` file
- ✅ Activates virtual environment
- ✅ Installs/updates dependencies
- ✅ Starts PostgreSQL database
- ✅ Tests database connection
- ✅ Runs code quality checks (Black, isort, flake8)
- ✅ Runs test suite
- ✅ Provides helpful next steps

### `start-db.sh` - Database Only
Quick script to start just the PostgreSQL database.

```bash
./scripts/start-db.sh
```

**What it does:**
- ✅ Starts PostgreSQL database
- ✅ Waits for database to be ready
- ✅ Tests connection

### `stop-dev.sh` - Stop Environment
Stop all development services.

```bash
./scripts/stop-dev.sh
```

**What it does:**
- ✅ Stops all Docker containers
- ✅ Cleans up development environment


## Usage Examples

### First Time Setup
```bash
# Complete setup with all checks
./scripts/dev.sh
```

## Troubleshooting

### Database Connection Issues
Make sure your `.env` file has the correct `DATABASE_URL` (replace `<password>` with your actual password):
```
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/restaurant-db
```

### Permission Issues
If scripts are not executable:
```bash
chmod +x scripts/*.sh
```

### Docker Issues
If Docker containers fail to start:
```bash
docker-compose down
docker-compose up -d db
```
