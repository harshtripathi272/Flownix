# Flownix Backend Documentation

## Overview

The Flownix backend is a FastAPI-based REST API that provides dataset upload, analysis, and machine learning pipeline generation capabilities. It's designed to handle various data formats and provide comprehensive insights into uploaded datasets.

## Technology Stack

- **Framework**: FastAPI 0.124.4
- **Server**: Uvicorn 0.38.0
- **Data Processing**: 
  - Pandas 2.3.3
  - NumPy 2.3.5
  - Scikit-learn 1.8.0
- **File Formats Support**:
  - CSV (pandas)
  - Excel (openpyxl, xlrd)
  - JSON (pandas)
  - Parquet (pyarrow)
- **Python Version**: 3.13

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── temp/                   # Temporary storage for uploaded files
└── app/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   └── routes.py       # API endpoints
    └── core/
        ├── __init__.py
        └── config.py       # Configuration settings
```

## Documentation Files

- [API Endpoints](./API_ENDPOINTS.md) - Detailed API documentation
- [Configuration](./CONFIGURATION.md) - Environment and configuration settings
- [Setup Guide](./SETUP.md) - Installation and setup instructions
- [Architecture](./ARCHITECTURE.md) - System design and architecture

## Quick Start

### Prerequisites
- Python 3.13 or higher
- pip (latest version)

### Installation

1. Create virtual environment:
```bash
cd backend
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

**Development mode (with auto-reload):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Key Features

### 1. Dataset Upload
- Upload datasets in multiple formats (CSV, Excel, JSON, Parquet)
- File size validation (max 100MB)
- Automatic file type detection
- Unique dataset ID generation

### 2. Dataset Analysis
- **Basic Information**: Row/column counts, data types, shape
- **Column Classification**: Numeric, categorical, datetime, boolean
- **Missing Values**: Per-column analysis with percentages
- **Duplicates**: Detection and percentage calculation
- **Statistical Analysis**: 
  - Numeric columns: mean, std, min, max, quartiles, skewness, kurtosis
  - Categorical columns: unique values, top values, cardinality
  - Datetime columns: date ranges
- **Correlation Analysis**: High correlations detection (>0.7)
- **Data Quality Score**: Overall quality assessment
- **Memory Usage**: Per-column and total memory consumption
- **Data Preview**: First and last 5 rows

### 3. ML Pipeline Generation (Coming Soon)
- Automated pipeline generation based on dataset analysis
- Pipeline execution and monitoring
- Code export functionality

## API Workflow

```
1. Upload Dataset
   POST /api/v1/dataset/upload
   ↓
   Receive dataset_id
   ↓
2. Analyze Dataset
   POST /api/v1/dataset/analyze?dataset_id={id}
   ↓
   Get comprehensive analysis
   ↓
3. Generate Pipeline (Coming Soon)
   POST /api/v1/pipeline/generate
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# File Upload Settings
MAX_UPLOAD_SIZE=104857600  # 100MB in bytes
TEMP_DIR=./temp

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

## Error Handling

The API uses standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid file, format issues)
- **404**: Not Found (dataset doesn't exist)
- **413**: Payload Too Large (file size exceeds limit)
- **500**: Internal Server Error

## Current Limitations

⚠️ **Important Notes:**

1. **In-Memory Storage**: Dataset metadata is stored in memory and will be lost on server restart. For production, implement database storage.

2. **File Persistence**: Uploaded files are stored in the `temp/` directory. Implement cleanup mechanisms for production.

3. **No Authentication**: Currently no user authentication. Add authentication for production use.

4. **Single Instance**: The current implementation doesn't support multiple server instances due to in-memory storage.

## Future Enhancements

- [ ] Database integration for metadata storage
- [ ] User authentication and authorization
- [ ] File cleanup scheduler
- [ ] ML pipeline generation and execution
- [ ] Model training and evaluation
- [ ] Export functionality for production code
- [ ] Websocket support for real-time updates
- [ ] Caching for analysis results

## Contributing

See the main project README for contribution guidelines.

## License

See the main project LICENSE file.

## Support

For issues and questions, please open an issue in the main repository.
