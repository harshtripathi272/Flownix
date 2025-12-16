# API Endpoints Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Table of Contents

1. [Root Endpoint](#root-endpoint)
2. [Dataset Upload](#dataset-upload)
3. [Dataset Analysis](#dataset-analysis)
4. [Pipeline Generation](#pipeline-generation)
5. [Pipeline Execution](#pipeline-execution)
6. [Pipeline Status](#pipeline-status)
7. [Code Export](#code-export)

---

## Root Endpoint

### GET `/`

Health check endpoint for the API.

**Response:**
```json
{
  "message": "Flownix API v1"
}
```

---

## Dataset Upload

### POST `/dataset/upload`

Upload a dataset file for analysis.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: 
  - `file`: File upload (CSV, Excel, JSON, or Parquet)

**Supported File Types:**
- `.csv` - Comma-separated values
- `.xlsx` - Excel 2007+ format
- `.xls` - Excel 97-2003 format
- `.json` - JSON format
- `.parquet` - Apache Parquet format

**File Constraints:**
- Maximum file size: 100MB
- File must contain data (not empty)
- File must have at least one column

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Dataset uploaded successfully",
  "data": {
    "dataset_id": "1501dee0-0058-487a-af96-db29dcb2a807",
    "filename": "sales_data.csv",
    "file_type": "CSV",
    "file_size": 2048576,
    "file_size_mb": 1.95,
    "rows": 5000,
    "columns": 23
  }
}
```

**Error Responses:**

**400 Bad Request:**
```json
{
  "detail": "Unsupported file type. Supported formats: .csv, .xlsx, .xls, .json, .parquet"
}
```

**413 Payload Too Large:**
```json
{
  "detail": "File too large. Maximum size is 100MB"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/dataset/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sales_data.csv"
```

---

## Dataset Analysis

### POST `/dataset/analyze`

Perform comprehensive analysis on an uploaded dataset.

**Query Parameters:**
- `dataset_id` (required): The UUID received from the upload endpoint

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Dataset analyzed successfully",
  "data": {
    "dataset_id": "1501dee0-0058-487a-af96-db29dcb2a807",
    "filename": "sales_data.csv",
    "file_type": "CSV",
    
    "basic_info": {
      "rows": 5000,
      "columns": 23,
      "total_cells": 115000,
      "column_names": ["id", "date", "product", "price", "quantity", ...],
      "dtypes": {
        "id": "int64",
        "date": "object",
        "product": "object",
        "price": "float64",
        "quantity": "int64"
      },
      "shape": [5000, 23]
    },
    
    "column_types": {
      "numeric_columns": ["id", "price", "quantity", "discount"],
      "categorical_columns": ["product", "category", "region"],
      "datetime_columns": ["date", "created_at"],
      "boolean_columns": ["is_active"],
      "numeric_count": 4,
      "categorical_count": 3,
      "datetime_count": 2,
      "boolean_count": 1
    },
    
    "missing_values": {
      "by_column": {
        "id": 0,
        "date": 5,
        "product": 12,
        "price": 8
      },
      "percentages": {
        "id": 0.0,
        "date": 0.1,
        "product": 0.24,
        "price": 0.16
      },
      "total_missing": 25,
      "columns_with_missing": ["date", "product", "price"]
    },
    
    "duplicates": {
      "duplicate_rows": 15,
      "duplicate_percentage": 0.3
    },
    
    "memory_usage": {
      "by_column_bytes": {
        "id": 40000,
        "date": 40000,
        "product": 50000
      },
      "total_memory_mb": 1.25,
      "avg_row_size_bytes": 250.5
    },
    
    "statistics": {
      "numeric_columns": {
        "price": {
          "count": 4992,
          "mean": 49.99,
          "std": 15.5,
          "min": 10.0,
          "25%": 35.0,
          "50%": 50.0,
          "75%": 65.0,
          "max": 100.0,
          "skewness": 0.15,
          "kurtosis": -0.5,
          "zeros_count": 0,
          "negative_count": 0
        }
      },
      "categorical_columns": {
        "product": {
          "unique_values": 150,
          "top_values": {
            "Product A": 120,
            "Product B": 95,
            "Product C": 87
          },
          "cardinality": "medium"
        }
      },
      "datetime_columns": {
        "date": {
          "min_date": "2023-01-01",
          "max_date": "2024-12-31",
          "range_days": 730
        }
      }
    },
    
    "correlations": {
      "high_correlations": [
        {
          "col1": "price",
          "col2": "quantity",
          "correlation": 0.856
        }
      ]
    },
    
    "data_quality": {
      "overall_score": 94.5,
      "completeness_score": 99.8,
      "uniqueness_score": 99.7,
      "quality_level": "excellent"
    },
    
    "preview": {
      "head": [
        {"id": 1, "date": "2023-01-01", "product": "Widget A", "price": 29.99},
        {"id": 2, "date": "2023-01-02", "product": "Widget B", "price": 39.99}
      ],
      "tail": [
        {"id": 4999, "date": "2024-12-30", "product": "Widget X", "price": 59.99},
        {"id": 5000, "date": "2024-12-31", "product": "Widget Y", "price": 49.99}
      ]
    }
  }
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Dataset not found"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/dataset/analyze?dataset_id=1501dee0-0058-487a-af96-db29dcb2a807" \
  -H "accept: application/json"
```

---

## Pipeline Generation

### POST `/pipeline/generate`

Generate an ML pipeline based on dataset analysis.

**Status:** 🚧 Coming Soon

**Query Parameters:**
- `dataset_id` (required): The UUID of the uploaded dataset

**Request Body (optional):**
```json
{
  "target_column": "price",
  "problem_type": "regression",
  "algorithms": ["linear_regression", "random_forest", "xgboost"],
  "validation_split": 0.2,
  "cross_validation": 5
}
```

**Response:**
```json
{
  "pipeline_id": "pipeline_001",
  "status": "generated",
  "steps": [
    "data_preprocessing",
    "feature_engineering",
    "model_training",
    "validation"
  ]
}
```

---

## Pipeline Execution

### POST `/pipeline/execute`

Execute a generated ML pipeline.

**Status:** 🚧 Coming Soon

**Query Parameters:**
- `pipeline_id` (required): The pipeline ID from generation

**Response:**
```json
{
  "pipeline_id": "pipeline_001",
  "status": "executing",
  "message": "Pipeline execution started"
}
```

---

## Pipeline Status

### GET `/pipeline/{pipeline_id}/status`

Get the execution status of a pipeline.

**Status:** 🚧 Coming Soon

**Path Parameters:**
- `pipeline_id` (required): The pipeline ID

**Response:**
```json
{
  "pipeline_id": "pipeline_001",
  "status": "completed",
  "progress": 100,
  "metrics": {
    "accuracy": 0.92,
    "f1_score": 0.89
  }
}
```

---

## Code Export

### POST `/export/code`

Export pipeline as production-ready code.

**Status:** 🚧 Coming Soon

**Query Parameters:**
- `pipeline_id` (required): The pipeline ID
- `format` (optional): Export format (`python`, `notebook`, `docker`)

**Response:**
```json
{
  "pipeline_id": "pipeline_001",
  "format": "python",
  "download_url": "/download/pipeline_001.zip"
}
```

---

## Error Handling

All endpoints follow consistent error response format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (validation error, invalid input)
- `404` - Not Found (resource doesn't exist)
- `413` - Payload Too Large (file size exceeds limit)
- `422` - Unprocessable Entity (invalid request format)
- `500` - Internal Server Error (unexpected server error)

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider implementing rate limiting to prevent abuse.

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test all endpoints directly from your browser.
