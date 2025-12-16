# Configuration Documentation

## Overview

This document describes all configuration options available for the Flownix backend. Configuration can be set through environment variables or the `config.py` file.

## Configuration File

**Location:** `backend/app/core/config.py`

## Configuration Options

### Server Settings

#### HOST
- **Type:** String
- **Default:** `"0.0.0.0"`
- **Description:** Host address the server binds to
- **Values:**
  - `"0.0.0.0"` - Listen on all network interfaces (recommended for production)
  - `"127.0.0.1"` - Listen only on localhost (more secure for development)
  - Specific IP address - Listen on specific interface

**Example:**
```python
HOST = "0.0.0.0"
```

#### PORT
- **Type:** Integer
- **Default:** `8000`
- **Description:** Port number the server listens on
- **Common Ports:**
  - `8000` - Default FastAPI/Uvicorn port
  - `8080` - Alternative HTTP port
  - `5000` - Flask default (if migrating)

**Example:**
```python
PORT = 8000
```

#### DEBUG
- **Type:** Boolean
- **Default:** `True`
- **Description:** Enable debug mode with detailed error messages
- **Values:**
  - `True` - Development mode (verbose errors, auto-reload)
  - `False` - Production mode (minimal errors, better performance)

**Example:**
```python
DEBUG = True
```

---

### File Upload Settings

#### MAX_UPLOAD_SIZE
- **Type:** Integer (bytes)
- **Default:** `104857600` (100MB)
- **Description:** Maximum allowed file upload size
- **Common Values:**
  - `10485760` - 10MB
  - `52428800` - 50MB
  - `104857600` - 100MB
  - `524288000` - 500MB
  - `1073741824` - 1GB

**Example:**
```python
MAX_UPLOAD_SIZE = 104857600  # 100MB
```

**Calculate custom size:**
```python
# Formula: size_in_MB * 1024 * 1024
MAX_UPLOAD_SIZE = 250 * 1024 * 1024  # 250MB
```

#### TEMP_DIR
- **Type:** String (path)
- **Default:** `"./temp"`
- **Description:** Directory for storing uploaded files temporarily
- **Recommendations:**
  - Use absolute paths for production
  - Ensure directory has write permissions
  - Consider separate disk/partition for large files

**Example:**
```python
TEMP_DIR = "./temp"  # Relative path
# or
TEMP_DIR = "/var/flownix/uploads"  # Absolute path (Linux)
# or
TEMP_DIR = "C:\\Flownix\\uploads"  # Absolute path (Windows)
```

---

### CORS Settings

#### ALLOWED_ORIGINS
- **Type:** List of strings
- **Default:** `["http://localhost:5173", "http://localhost:3000"]`
- **Description:** List of allowed origins for CORS (Cross-Origin Resource Sharing)
- **Usage:** Add your frontend URLs here

**Example:**
```python
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # React dev server
    "https://myapp.com",      # Production frontend
    "https://www.myapp.com"   # Production frontend with www
]
```

**Allow all origins (NOT recommended for production):**
```python
ALLOWED_ORIGINS = ["*"]
```

---

## Environment Variables

You can override configuration using a `.env` file in the backend directory.

### Creating .env File

**Windows:**
```bash
type nul > .env
```

**Linux/macOS:**
```bash
touch .env
```

### .env File Format

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# File Upload Settings
MAX_UPLOAD_SIZE=104857600
TEMP_DIR=./temp

# CORS Settings (comma-separated)
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,https://myapp.com
```

### Loading Environment Variables

The application uses `pydantic-settings` to automatically load environment variables.

**Priority Order:**
1. Environment variables (highest priority)
2. `.env` file
3. Default values in `config.py` (lowest priority)

---

## Configuration Examples

### Development Configuration

**.env file:**
```env
HOST=127.0.0.1
PORT=8000
DEBUG=True
MAX_UPLOAD_SIZE=52428800
TEMP_DIR=./temp
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Production Configuration

**.env file:**
```env
HOST=0.0.0.0
PORT=8000
DEBUG=False
MAX_UPLOAD_SIZE=104857600
TEMP_DIR=/var/flownix/uploads
ALLOWED_ORIGINS=https://myapp.com,https://www.myapp.com
```

### Docker Configuration

**.env file:**
```env
HOST=0.0.0.0
PORT=8000
DEBUG=False
MAX_UPLOAD_SIZE=104857600
TEMP_DIR=/app/uploads
ALLOWED_ORIGINS=https://myapp.com
```

---

## Advanced Configuration

### Custom File Size Limits by Type

To implement different size limits for different file types, modify `routes.py`:

```python
FILE_SIZE_LIMITS = {
    '.csv': 200 * 1024 * 1024,      # 200MB for CSV
    '.xlsx': 100 * 1024 * 1024,     # 100MB for Excel
    '.json': 50 * 1024 * 1024,      # 50MB for JSON
    '.parquet': 500 * 1024 * 1024   # 500MB for Parquet
}
```

### Custom Temporary Directory Structure

Organize uploads by date:

```python
import os
from datetime import datetime

# In config.py
def get_temp_dir():
    base_dir = "./temp"
    date_dir = datetime.now().strftime("%Y/%m/%d")
    full_path = os.path.join(base_dir, date_dir)
    os.makedirs(full_path, exist_ok=True)
    return full_path

TEMP_DIR = get_temp_dir()
```

### File Cleanup Configuration

Add automatic cleanup settings:

```python
# config.py
FILE_RETENTION_HOURS = 24  # Delete files older than 24 hours
CLEANUP_INTERVAL_MINUTES = 60  # Run cleanup every 60 minutes
```

---

## Security Considerations

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Use specific `ALLOWED_ORIGINS` (never use `"*"`)
- [ ] Set appropriate `MAX_UPLOAD_SIZE` to prevent abuse
- [ ] Use absolute paths for `TEMP_DIR`
- [ ] Implement file cleanup mechanism
- [ ] Use HTTPS in production
- [ ] Set up proper file permissions on `TEMP_DIR`
- [ ] Consider rate limiting
- [ ] Implement authentication/authorization

### File Storage Security

```python
# Recommended permissions for TEMP_DIR
# Linux/macOS:
chmod 750 temp/  # rwxr-x---

# Ensure only application user can write
chown appuser:appgroup temp/
```

---

## Monitoring Configuration

### Logging Configuration

Add to `main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring

```python
# config.py
ENABLE_METRICS = True
METRICS_PORT = 9090
```

---

## Database Configuration (Future)

For future database integration:

```env
# Database Settings
DATABASE_URL=postgresql://user:password@localhost:5432/flownix
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

---

## Configuration Validation

The `Settings` class in `config.py` automatically validates configuration:

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024
    TEMP_DIR: str = "./temp"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## Troubleshooting Configuration Issues

### Configuration Not Loading

**Check:**
1. `.env` file is in the correct directory (backend/)
2. `.env` file syntax is correct (no spaces around `=`)
3. Variable names match exactly (case-sensitive)
4. No quotes around values in `.env`

### CORS Errors

**Symptoms:** Frontend can't access API

**Solutions:**
- Add frontend URL to `ALLOWED_ORIGINS`
- Check for `http` vs `https` mismatch
- Check port numbers match
- Clear browser cache

### File Upload Fails

**Check:**
- File size doesn't exceed `MAX_UPLOAD_SIZE`
- `TEMP_DIR` exists and has write permissions
- Sufficient disk space available

---

## Environment-Specific Configurations

### Development
```env
DEBUG=True
HOST=127.0.0.1
MAX_UPLOAD_SIZE=52428800
```

### Staging
```env
DEBUG=True
HOST=0.0.0.0
MAX_UPLOAD_SIZE=104857600
ALLOWED_ORIGINS=https://staging.myapp.com
```

### Production
```env
DEBUG=False
HOST=0.0.0.0
MAX_UPLOAD_SIZE=104857600
ALLOWED_ORIGINS=https://myapp.com
```

---

## Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use environment variables in production** - Don't rely on `.env` file
3. **Validate configuration on startup** - Fail fast if misconfigured
4. **Document all configuration changes** - Keep this file updated
5. **Use different configs per environment** - dev, staging, production
6. **Secure sensitive values** - Use secrets management in production

---

## Related Documentation

- [Setup Guide](./SETUP.md) - Installation and initial configuration
- [API Endpoints](./API_ENDPOINTS.md) - API documentation
- [Architecture](./ARCHITECTURE.md) - System architecture
