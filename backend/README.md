# Flownix Backend

FastAPI-based backend server for the Flownix ML Intelligence Engine.

## Setup

1. **Create and activate virtual environment** (already done):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
copy .env.example .env
# Edit .env with your settings
```

## Running the Server

### Development Mode (with auto-reload)
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

The server will be available at `http://localhost:8000`

### Core Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### API v1 Endpoints (`/api/v1`)
- `POST /api/v1/dataset/upload` - Upload dataset
- `POST /api/v1/dataset/analyze` - Analyze dataset
- `POST /api/v1/pipeline/generate` - Generate ML pipeline
- `POST /api/v1/pipeline/execute` - Execute pipeline
- `GET /api/v1/pipeline/{id}/status` - Get pipeline status
- `POST /api/v1/export/code` - Export production code

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py      # API route definitions
│   └── core/
│       ├── __init__.py
│       └── config.py      # Configuration settings
```

## Development

Visit `http://localhost:8000/docs` for interactive API documentation and testing.
