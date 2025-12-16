/**
 * API Service Layer
 * Centralized API client for backend communication
 */

import { getApiUrl, getBaseApiUrl, config } from '../config/config';
import type {
    HealthCheckResponse,
    RootResponse,
    UploadResponse,
    AnalysisResponse,
    PipelineGenerateResponse,
    PipelineExecuteResponse,
    PipelineStatusResponse,
    ExportCodeResponse,
    ErrorResponse,
} from '../types/types';

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
    constructor(
        message: string,
        public statusCode?: number,
        public detail?: string
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

/**
 * Generic fetch wrapper with error handling
 */
async function fetchWithErrorHandling<T>(
    url: string,
    options?: RequestInit
): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), config.api.timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
        });

        clearTimeout(timeoutId);

        // Handle non-OK responses
        if (!response.ok) {
            let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            let errorDetail: string | undefined;

            try {
                const errorData: ErrorResponse = await response.json();
                errorDetail = errorData.detail;
                errorMessage = errorDetail || errorMessage;
            } catch {
                // If JSON parsing fails, use the default error message
            }

            throw new ApiError(errorMessage, response.status, errorDetail);
        }

        // Parse JSON response
        const data: T = await response.json();
        return data;
    } catch (error) {
        clearTimeout(timeoutId);

        if (error instanceof ApiError) {
            throw error;
        }

        if (error instanceof Error) {
            if (error.name === 'AbortError') {
                throw new ApiError('Request timeout', 408);
            }
            throw new ApiError(error.message);
        }

        throw new ApiError('Unknown error occurred');
    }
}

/**
 * API Client Class
 */
class ApiClient {
    /**
     * Health check endpoint
     */
    async healthCheck(): Promise<HealthCheckResponse> {
        const url = getBaseApiUrl('/health');
        return fetchWithErrorHandling<HealthCheckResponse>(url);
    }

    /**
     * Root API endpoint
     */
    async getRoot(): Promise<RootResponse> {
        const url = getBaseApiUrl('/');
        return fetchWithErrorHandling<RootResponse>(url);
    }

    /**
     * API v1 root endpoint
     */
    async getApiRoot(): Promise<{ message: string }> {
        const url = getApiUrl('/');
        return fetchWithErrorHandling<{ message: string }>(url);
    }

    /**
     * Upload dataset file
     */
    async uploadDataset(
        file: File,
        onProgress?: (progress: number) => void
    ): Promise<UploadResponse> {
        const url = getApiUrl('/dataset/upload');
        const formData = new FormData();
        formData.append('file', file);

        // For progress tracking, we'd need to use XMLHttpRequest
        // For now, using fetch without progress
        if (onProgress) {
            // Progress tracking would require XMLHttpRequest or a library
            console.warn('Progress tracking not yet implemented with fetch API');
        }

        return fetchWithErrorHandling<UploadResponse>(url, {
            method: 'POST',
            body: formData,
        });
    }

    /**
     * Analyze uploaded dataset
     */
    async analyzeDataset(datasetId: string): Promise<AnalysisResponse> {
        const url = getApiUrl(`/dataset/analyze?dataset_id=${datasetId}`);
        return fetchWithErrorHandling<AnalysisResponse>(url, {
            method: 'POST',
        });
    }

    /**
     * Generate ML pipeline
     */
    async generatePipeline(
        datasetId: string,
        config?: Record<string, any>
    ): Promise<PipelineGenerateResponse> {
        const url = getApiUrl('/pipeline/generate');
        const params = new URLSearchParams({ dataset_id: datasetId });

        return fetchWithErrorHandling<PipelineGenerateResponse>(
            `${url}?${params}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: config ? JSON.stringify(config) : undefined,
            }
        );
    }

    /**
     * Execute pipeline
     */
    async executePipeline(pipelineId: string): Promise<PipelineExecuteResponse> {
        const url = getApiUrl('/pipeline/execute');
        const params = new URLSearchParams({ pipeline_id: pipelineId });

        return fetchWithErrorHandling<PipelineExecuteResponse>(
            `${url}?${params}`,
            {
                method: 'POST',
            }
        );
    }

    /**
     * Get pipeline status
     */
    async getPipelineStatus(pipelineId: string): Promise<PipelineStatusResponse> {
        const url = getApiUrl(`/pipeline/${pipelineId}/status`);
        return fetchWithErrorHandling<PipelineStatusResponse>(url);
    }

    /**
     * Export pipeline code
     */
    async exportCode(
        pipelineId: string,
        format: string = 'python'
    ): Promise<ExportCodeResponse> {
        const url = getApiUrl('/export/code');
        const params = new URLSearchParams({
            pipeline_id: pipelineId,
            format,
        });

        return fetchWithErrorHandling<ExportCodeResponse>(
            `${url}?${params}`,
            {
                method: 'POST',
            }
        );
    }
}

// Export singleton instance
export const api = new ApiClient();

// Export the class for testing purposes
export { ApiClient };
