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

# In-memory storage for dataset metadata
# In production, this should be replaced with a database
datasets_metadata: Dict[str, Dict[str, Any]] = {}

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
            
            # Store metadata for later retrieval
            datasets_metadata[dataset_id] = dataset_info
            
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
    """Perform comprehensive analysis on uploaded dataset"""
    
    # Check if dataset exists
    if dataset_id not in datasets_metadata:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    metadata = datasets_metadata[dataset_id]
    file_path = metadata["file_path"]
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset file not found")
    
    try:
        # Load dataset based on file type
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_ext == '.json':
            df = pd.read_json(file_path)
        elif file_ext == '.parquet':
            df = pd.read_parquet(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Comprehensive dataset analysis
        
        # Column type categorization
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns.tolist()
        boolean_cols = df.select_dtypes(include=['bool']).columns.tolist()
        
        # Missing values analysis
        missing_values = df.isnull().sum().to_dict()
        missing_percentages = (df.isnull().sum() / len(df) * 100).round(2).to_dict()
        
        # Duplicate analysis
        duplicate_rows = int(df.duplicated().sum())
        
        # Memory usage
        memory_usage = df.memory_usage(deep=True).to_dict()
        total_memory_mb = round(sum(memory_usage.values()) / (1024 * 1024), 2)
        
        # Statistical summary for numeric columns
        numeric_stats = {}
        if numeric_cols:
            stats_df = df[numeric_cols].describe()
            for col in numeric_cols:
                numeric_stats[col] = {
                    "count": int(stats_df.loc['count', col]),
                    "mean": float(stats_df.loc['mean', col]) if not pd.isna(stats_df.loc['mean', col]) else None,
                    "std": float(stats_df.loc['std', col]) if not pd.isna(stats_df.loc['std', col]) else None,
                    "min": float(stats_df.loc['min', col]) if not pd.isna(stats_df.loc['min', col]) else None,
                    "25%": float(stats_df.loc['25%', col]) if not pd.isna(stats_df.loc['25%', col]) else None,
                    "50%": float(stats_df.loc['50%', col]) if not pd.isna(stats_df.loc['50%', col]) else None,
                    "75%": float(stats_df.loc['75%', col]) if not pd.isna(stats_df.loc['75%', col]) else None,
                    "max": float(stats_df.loc['max', col]) if not pd.isna(stats_df.loc['max', col]) else None,
                    "skewness": float(df[col].skew()) if not pd.isna(df[col].skew()) else None,
                    "kurtosis": float(df[col].kurtosis()) if not pd.isna(df[col].kurtosis()) else None,
                    "zeros_count": int((df[col] == 0).sum()),
                    "negative_count": int((df[col] < 0).sum()) if df[col].dtype in ['int64', 'float64'] else 0
                }
        
        # Categorical columns analysis
        categorical_stats = {}
        for col in categorical_cols:
            unique_count = df[col].nunique()
            categorical_stats[col] = {
                "unique_values": unique_count,
                "top_values": df[col].value_counts().head(10).to_dict(),
                "cardinality": "high" if unique_count > len(df) * 0.5 else "medium" if unique_count > 10 else "low"
            }
        
        # Datetime columns analysis
        datetime_stats = {}
        for col in datetime_cols:
            datetime_stats[col] = {
                "min_date": str(df[col].min()),
                "max_date": str(df[col].max()),
                "range_days": (df[col].max() - df[col].min()).days if pd.notna(df[col].min()) else None
            }
        
        # Correlation analysis (only for numeric columns)
        correlations = {}
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            # Find high correlations (excluding diagonal)
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:  # High correlation threshold
                        high_corr.append({
                            "col1": corr_matrix.columns[i],
                            "col2": corr_matrix.columns[j],
                            "correlation": round(float(corr_val), 3)
                        })
            correlations["high_correlations"] = high_corr
        
        # Data quality score
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness_score = round((1 - missing_cells / total_cells) * 100, 2)
        uniqueness_score = round((1 - duplicate_rows / len(df)) * 100, 2) if len(df) > 0 else 100
        data_quality_score = round((completeness_score + uniqueness_score) / 2, 2)
        
        # Build comprehensive response
        analysis_result = {
            "dataset_id": dataset_id,
            "filename": metadata["filename"],
            "file_type": metadata["file_type"],
            
            # Basic info
            "basic_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "total_cells": total_cells,
                "column_names": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "shape": df.shape
            },
            
            # Column categorization
            "column_types": {
                "numeric_columns": numeric_cols,
                "categorical_columns": categorical_cols,
                "datetime_columns": datetime_cols,
                "boolean_columns": boolean_cols,
                "numeric_count": len(numeric_cols),
                "categorical_count": len(categorical_cols),
                "datetime_count": len(datetime_cols),
                "boolean_count": len(boolean_cols)
            },
            
            # Missing values
            "missing_values": {
                "by_column": missing_values,
                "percentages": missing_percentages,
                "total_missing": int(missing_cells),
                "columns_with_missing": [col for col, val in missing_values.items() if val > 0]
            },
            
            # Duplicates
            "duplicates": {
                "duplicate_rows": duplicate_rows,
                "duplicate_percentage": round(duplicate_rows / len(df) * 100, 2) if len(df) > 0 else 0
            },
            
            # Memory
            "memory_usage": {
                "by_column_bytes": memory_usage,
                "total_memory_mb": total_memory_mb,
                "avg_row_size_bytes": round(sum(memory_usage.values()) / len(df), 2) if len(df) > 0 else 0
            },
            
            # Statistical analysis
            "statistics": {
                "numeric_columns": numeric_stats,
                "categorical_columns": categorical_stats,
                "datetime_columns": datetime_stats
            },
            
            # Correlations
            "correlations": correlations,
            
            # Data quality
            "data_quality": {
                "overall_score": data_quality_score,
                "completeness_score": completeness_score,
                "uniqueness_score": uniqueness_score,
                "quality_level": "excellent" if data_quality_score >= 90 else "good" if data_quality_score >= 70 else "fair" if data_quality_score >= 50 else "poor"
            },
            
            # Preview
            "preview": {
                "head": df.head(5).to_dict('records'),
                "tail": df.tail(5).to_dict('records')
            }
        }
        
        return {
            "status": "success",
            "message": "Dataset analyzed successfully",
            "data": analysis_result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing dataset: {str(e)}"
        )


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
