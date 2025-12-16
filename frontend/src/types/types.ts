/**
 * TypeScript Type Definitions
 * Interfaces matching the backend API response models
 */

// Generic API Response wrapper
export interface ApiResponse<T> {
    status: 'success' | 'error';
    message: string;
    data?: T;
    detail?: string; // For error responses
}

// Health Check Response
export interface HealthCheckResponse {
    status: string;
}

// Root API Response
export interface RootResponse {
    message: string;
    version: string;
    status: string;
}

// Dataset Upload Response
export interface DatasetInfo {
    dataset_id: string;
    filename: string;
    file_type: string;
    file_size: number;
    file_size_mb: number;
    rows: number;
    columns: number;
    column_names: string[];
    dtypes: Record<string, string>;
    numeric_columns: string[];
    categorical_columns: string[];
    datetime_columns: string[];
    missing_values: Record<string, number>;
    total_missing: number;
    duplicate_rows: number;
    memory_usage_mb: number;
    file_path: string;
    preview: Record<string, any>[];
}

export type UploadResponse = ApiResponse<DatasetInfo>;

// Dataset Analysis Response
export interface AnalysisResult {
    dataset_id: string;
    filename: string;
    file_type: string;

    basic_info: {
        rows: number;
        columns: number;
        total_cells: number;
        column_names: string[];
        dtypes: Record<string, string>;
        shape: [number, number];
    };

    column_types: {
        numeric_columns: string[];
        categorical_columns: string[];
        datetime_columns: string[];
        boolean_columns: string[];
        numeric_count: number;
        categorical_count: number;
        datetime_count: number;
        boolean_count: number;
    };

    missing_values: {
        by_column: Record<string, number>;
        percentages: Record<string, number>;
        total_missing: number;
        columns_with_missing: string[];
    };

    duplicates: {
        duplicate_rows: number;
        duplicate_percentage: number;
    };

    memory_usage: {
        by_column_bytes: Record<string, number>;
        total_memory_mb: number;
        avg_row_size_bytes: number;
    };

    statistics: {
        numeric_columns: Record<string, NumericStats>;
        categorical_columns: Record<string, CategoricalStats>;
        datetime_columns: Record<string, DatetimeStats>;
    };

    correlations: {
        high_correlations?: HighCorrelation[];
    };

    data_quality: {
        overall_score: number;
        completeness_score: number;
        uniqueness_score: number;
        quality_level: 'excellent' | 'good' | 'fair' | 'poor';
    };

    preview: {
        head: Record<string, any>[];
        tail: Record<string, any>[];
    };
}

export interface NumericStats {
    count: number;
    mean: number | null;
    std: number | null;
    min: number | null;
    '25%': number | null;
    '50%': number | null;
    '75%': number | null;
    max: number | null;
    skewness: number | null;
    kurtosis: number | null;
    zeros_count: number;
    negative_count: number;
}

export interface CategoricalStats {
    unique_values: number;
    top_values: Record<string, number>;
    cardinality: 'high' | 'medium' | 'low';
}

export interface DatetimeStats {
    min_date: string;
    max_date: string;
    range_days: number | null;
}

export interface HighCorrelation {
    col1: string;
    col2: string;
    correlation: number;
}

export type AnalysisResponse = ApiResponse<AnalysisResult>;

// Pipeline Generation Response
export interface PipelineInfo {
    pipeline_id: string;
    status: string;
    steps: string[];
}

export type PipelineGenerateResponse = ApiResponse<PipelineInfo>;

// Pipeline Execution Response
export interface PipelineExecutionInfo {
    pipeline_id: string;
    status: string;
    message: string;
}

export type PipelineExecuteResponse = ApiResponse<PipelineExecutionInfo>;

// Pipeline Status Response
export interface PipelineStatus {
    pipeline_id: string;
    status: string;
    progress: number;
    metrics: Record<string, number>;
}

export type PipelineStatusResponse = ApiResponse<PipelineStatus>;

// Export Code Response
export interface ExportCodeInfo {
    pipeline_id: string;
    format: string;
    download_url: string;
}

export type ExportCodeResponse = ApiResponse<ExportCodeInfo>;

// Error Response
export interface ErrorResponse {
    detail: string;
}
