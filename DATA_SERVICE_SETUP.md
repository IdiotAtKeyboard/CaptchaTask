# Data Service - Quick Start Guide

## 🚀 Running Tests with Automatic Service Startup

The data service will **automatically start** when you run pytest. No manual setup required!

### Prerequisites

First, install all dependencies:

```bash
# Install Poetry dependencies (includes requests, Flask, etc.)
poetry install
```

### Option 1: Simple - Run Tests with Auto Service Startup (RECOMMENDED)

```bash
# From project root
poetry run pytest tests/test_contact_form.py -v

# Or with allure reporting
poetry run pytest tests/test_contact_form.py -v --alluredir=allure-results
```

**What happens automatically:**
- Flask service starts on `http://localhost:5000`
- Service waits until it's ready to accept requests
- Tests run and fetch data from the service
- Service stops when tests complete

### Option 2: Manual Service Setup

If you want to run the service separately:

```bash
# Terminal 1: Start data service
cd data-service
pip install -r requirements.txt
python app.py

# Terminal 2: Run tests (in project root)
poetry run pytest tests/test_contact_form.py -v
```

### Option 3: Run Service in Background (Windows)

```bash
# Start service in background
cd data-service
start python app.py

# Run tests
cd ..
poetry run pytest tests/test_contact_form.py -v
```

### Custom Service URL

If you want to use a different service URL:

```bash
# Set environment variable
$env:DATA_SERVICE_URL = "http://localhost:8080"

# Then run tests
poetry run pytest tests/test_contact_form.py -v
```

Or create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
# Edit .env with your DATA_SERVICE_URL
```

### View Service Response

Test the service manually:

```bash
# Terminal 1: Start service
cd data-service
python app.py

# Terminal 2: Test endpoint
curl http://localhost:5000/users

# Response:
# [
#   {"id": "alice-acme-corp", "name": "Alice Johnson", "email": "alice@example.com", "company": "Acme Corp"},
#   {"id": "bob-techstart", "name": "Bob Smith", "email": "bob@example.com", "company": "TechStart Inc"}
# ]
```

### 🐳 Docker (When Ready)

```bash
# Build image
docker build -t data-service data-service/

# Run container
docker run -p 5000:5000 data-service

# Then run tests normally
poetry run pytest tests/test_contact_form.py -v
```

### Troubleshooting

**Port 5000 already in use:**
```bash
# Find and kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Service fails to start:**
- Check if Flask is installed: `pip list | grep Flask`
- Check `data-service/requirements.txt` exists
- Check `data-service/users.json` exists

**Tests timeout waiting for service:**
- Increase max_retries in `tests/conftest.py` (line 39)
- Check if there are any import errors in `data-service/app.py`

