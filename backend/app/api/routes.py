from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import pandas as pd
import os
import uuid
from pathlib import Path
import aiofiles

from app.core.config import settings

api_router = APIRouter()

# Ensure temp directory exists
os.makedirs(settings.TEMP_DIR, exist_ok=True)

# Supported file types
SUPPORTED_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.json', '.parquet'}

@api_router.get("/")
async def api_root():
    return {"message": "Flownix API v1"}


@api_router.post("/dataset/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload a dataset file for analysis (CSV, Excel, JSON, Parquet)"""
    
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    
    # Validate file size
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE / (1024*1024):.0f}MB"
        )
    
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    # Generate unique dataset ID
    dataset_id = str(uuid.uuid4())
    file_path = os.path.join(settings.TEMP_DIR, f"{dataset_id}{file_ext}")
    
    try:
        # Save file temporarily
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Read with pandas based on file type and validate
        try:
            df = None
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_ext == '.json':
                df = pd.read_json(file_path)
            elif file_ext == '.parquet':
                df = pd.read_parquet(file_path)
            
            # Basic validation
            if df is None:
                raise HTTPException(status_code=400, detail="Failed to read file")
            
            if df.empty:
                raise HTTPException(status_code=400, detail="File contains no data")
            
            if len(df.columns) == 0:
                raise HTTPException(status_code=400, detail="File has no columns")
            
            # Get dataset info
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()
            
            dataset_info = {
                "dataset_id": dataset_id,
                "filename": file.filename,
                "file_type": file_ext.replace('.', '').upper(),
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "numeric_columns": numeric_cols,
                "categorical_columns": categorical_cols,
                "datetime_columns": datetime_cols,
                "missing_values": df.isnull().sum().to_dict(),
                "total_missing": int(df.isnull().sum().sum()),
                "duplicate_rows": int(df.duplicated().sum()),
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
                "file_path": file_path,
                "preview": df.head(5).to_dict('records')  # First 5 rows preview
            }
            
            return {
                "status": "success",
                "message": "Dataset uploaded and validated successfully",
                "data": dataset_info
            }
            
        except pd.errors.EmptyDataError:
            # Clean up the file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail="File is empty or invalid")
        
        except pd.errors.ParserError as e:
            # Clean up the file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse file: {str(e)}"
            )
        
        except ValueError as e:
            # Clean up the file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format: {str(e)}"
            )
        
        except Exception as e:
            # Clean up the file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving file: {str(e)}"
        )


@api_router.post("/dataset/analyze")
async def analyze_dataset(dataset_id: str):
    """Perform intelligent analysis on uploaded dataset"""
    return {
        "dataset_id": dataset_id,
        "status": "analyzed",
        "insights": {
            "data_health_score": 0.85,
            "leakage_detected": False,
            "recommended_models": ["random_forest", "gradient_boosting"],
            "warnings": []
        }
    }


@api_router.post("/pipeline/generate")
async def generate_pipeline(dataset_id: str, config: Dict[str, Any] = None):
    """Generate ML pipeline based on dataset analysis"""
    return {
        "pipeline_id": "pipeline_001",
        "status": "generated",
        "steps": [
            "data_preprocessing",
            "feature_engineering",
            "model_training",
            "validation"
        ]
    }


@api_router.post("/pipeline/execute")
async def execute_pipeline(pipeline_id: str):
    """Execute the generated ML pipeline"""
    return {
        "pipeline_id": pipeline_id,
        "status": "executing",
        "message": "Pipeline execution started"
    }


@api_router.get("/pipeline/{pipeline_id}/status")
async def get_pipeline_status(pipeline_id: str):
    """Get the status of pipeline execution"""
    return {
        "pipeline_id": pipeline_id,
        "status": "completed",
        "progress": 100,
        "metrics": {
            "accuracy": 0.92,
            "f1_score": 0.89
        }
    }


@api_router.post("/export/code")
async def export_code(pipeline_id: str, format: str = "python"):
    """Export pipeline as production-ready code"""
    return {
        "pipeline_id": pipeline_id,
        "format": format,
        "download_url": f"/download/{pipeline_id}.zip"
    }
