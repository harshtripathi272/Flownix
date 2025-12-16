# Setup Guide

## Prerequisites

Before setting up the Flownix backend, ensure you have the following installed:

### Required Software

1. **Python 3.13 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **pip (Python package manager)**
   - Usually comes with Python
   - Verify installation: `pip --version`
   - Update to latest: `python -m pip install --upgrade pip`

3. **Git** (optional, for cloning repository)
   - Download from [git-scm.com](https://git-scm.com/)

### System Requirements

- **OS**: Windows 10/11, Linux, macOS
- **RAM**: Minimum 4GB (8GB recommended for large datasets)
- **Disk Space**: At least 500MB for dependencies and temporary files
- **Network**: Internet connection for downloading dependencies

---

## Installation Steps

### 1. Clone or Download the Project

**Using Git:**
```bash
git clone <repository-url>
cd Flownix/backend
```

**Or download and extract the ZIP file**, then navigate to the backend folder.

---

### 2. Create Virtual Environment

Creating a virtual environment isolates your project dependencies.

**Windows:**
```bash
python -m venv venv
```

**Linux/macOS:**
```bash
python3 -m venv venv
```

---

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```bash
venv\Scripts\activate
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal prompt.

---

### 4. Upgrade pip

Ensure you have the latest pip version:

```bash
python -m pip install --upgrade pip
```

---

### 5. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI 0.124.4
- Uvicorn 0.38.0
- Pandas 2.3.3
- NumPy 2.3.5
- Scikit-learn 1.8.0
- PyArrow 22.0.0
- OpenPyXL 3.1.5
- And other dependencies...

**Installation may take 5-10 minutes depending on your internet speed.**

---

### 6. Verify Installation

Check if all packages are installed:

```bash
pip list
```

You should see all packages from `requirements.txt` listed.

---

### 7. Create Required Directories

The temp directory is created automatically, but you can verify:

```bash
# Windows
if not exist "temp" mkdir temp

# Linux/macOS
mkdir -p temp
```

---

### 8. Configuration (Optional)

Create a `.env` file in the backend directory for custom configuration:

```bash
# Create .env file
# Windows
type nul > .env

# Linux/macOS
touch .env
```

Add configuration (optional):
```env
# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Upload Settings
MAX_UPLOAD_SIZE=104857600
TEMP_DIR=./temp

# CORS Settings (for frontend)
ALLOWED_ORIGINS=["http://localhost:5173"]
```

---

## Running the Server

### Development Mode (with auto-reload)

**Recommended for development:**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Features:
- ✅ Auto-reload on code changes
- ✅ Detailed error messages
- ✅ Debug mode enabled

### Production Mode

**For production deployment:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Features:
- ✅ Multiple worker processes
- ✅ Better performance
- ✅ Production-ready

### Using Python Module

Alternative way to start the server:

```bash
python -m uvicorn main:app --reload
```

---

## Verify Server is Running

1. **Check terminal output:**
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```

2. **Open browser and visit:**
   - API Root: http://localhost:8000/api/v1
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

3. **Test with curl:**
   ```bash
   curl http://localhost:8000/api/v1
   ```
   
   Expected response:
   ```json
   {"message": "Flownix API v1"}
   ```

---

## Troubleshooting

### Issue: Port Already in Use

**Error:** `Error: [Errno 98] Address already in use`

**Solution:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001

# Or kill the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### Issue: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: Python Version Incompatible

**Error:** Package installation fails due to Python version

**Solution:**
- Install Python 3.13 or higher
- Or modify `requirements.txt` to use older package versions compatible with your Python version

### Issue: Permission Denied (Linux/macOS)

**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
```bash
# Make sure you have write permissions
chmod +w temp/
# Or run with appropriate permissions
```

### Issue: Import Errors on Windows

**Error:** Build failures during pip install (numpy, pandas, etc.)

**Solution:**
- Ensure you're using Python 3.13 with pre-built wheels
- Update pip: `python -m pip install --upgrade pip`
- Install packages individually to identify the problem

### Issue: Large File Upload Fails

**Error:** 413 Payload Too Large

**Solution:**
- Increase `MAX_UPLOAD_SIZE` in config.py or .env file
- Consider chunked upload for very large files

---

## Testing the Installation

### 1. Upload a Test Dataset

Create a simple CSV file `test.csv`:
```csv
id,name,age,salary
1,Alice,30,50000
2,Bob,25,45000
3,Charlie,35,60000
```

Upload it via curl:
```bash
curl -X POST "http://localhost:8000/api/v1/dataset/upload" \
  -F "file=@test.csv"
```

### 2. Analyze the Dataset

Use the `dataset_id` from the upload response:
```bash
curl -X POST "http://localhost:8000/api/v1/dataset/analyze?dataset_id=<your-dataset-id>"
```

### 3. Use Interactive Docs

Visit http://localhost:8000/docs and test all endpoints interactively.

---

## Development Setup

### Enable Hot Reload

Already enabled with `--reload` flag.

### IDE Configuration

**VS Code:**
1. Install Python extension
2. Select Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter" → Choose venv
3. Install recommended extensions:
   - Python
   - Pylance
   - Python Debugger

**PyCharm:**
1. File → Settings → Project → Python Interpreter
2. Add interpreter → Existing environment → Select venv/Scripts/python.exe

### Debugging

**VS Code launch.json:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

---

## Updating Dependencies

To update all packages to their latest versions:

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade fastapi

# Regenerate requirements.txt with new versions
pip freeze > requirements.txt
```

---

## Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

---

## Uninstalling

To completely remove the backend:

1. Deactivate virtual environment: `deactivate`
2. Delete the venv folder: `rm -rf venv` (Linux/macOS) or `rmdir /s venv` (Windows)
3. Delete temp folder: `rm -rf temp`
4. Delete the backend folder

---

## Next Steps

After successful setup:

1. Read [API_ENDPOINTS.md](./API_ENDPOINTS.md) for API usage
2. Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the codebase
3. Read [CONFIGURATION.md](./CONFIGURATION.md) for advanced settings
4. Start building your frontend or test with Postman/curl

---

## Getting Help

- Check [README.md](./README.md) for general information
- Review [API_ENDPOINTS.md](./API_ENDPOINTS.md) for endpoint details
- Open an issue in the repository for bugs
- Check FastAPI documentation: https://fastapi.tiangolo.com/
