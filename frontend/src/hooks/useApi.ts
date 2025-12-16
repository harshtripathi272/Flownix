/**
 * Custom React Hooks for API Interactions
 * Provides reusable hooks with loading, error, and data states
 */

import { useState, useEffect, useCallback } from 'react';
import { api, ApiError } from '../services/api';
import type {
    HealthCheckResponse,
    UploadResponse,
    AnalysisResponse,
} from '../types/types';

/**
 * Generic API hook state
 */
interface ApiState<T> {
    data: T | null;
    loading: boolean;
    error: string | null;
}

/**
 * Hook for health check
 */
export function useHealthCheck() {
    const [state, setState] = useState<ApiState<HealthCheckResponse>>({
        data: null,
        loading: true,
        error: null,
    });

    const checkHealth = useCallback(async () => {
        setState({ data: null, loading: true, error: null });
        try {
            const response = await api.healthCheck();
            setState({ data: response, loading: false, error: null });
        } catch (error) {
            const errorMessage = error instanceof ApiError
                ? error.message
                : 'Failed to connect to backend';
            setState({ data: null, loading: false, error: errorMessage });
        }
    }, []);

    useEffect(() => {
        checkHealth();
    }, [checkHealth]);

    return { ...state, refetch: checkHealth };
}

/**
 * Hook for dataset upload
 */
export function useUploadDataset() {
    const [state, setState] = useState<ApiState<UploadResponse>>({
        data: null,
        loading: false,
        error: null,
    });
    const [progress, setProgress] = useState<number>(0);

    const upload = useCallback(async (file: File) => {
        setState({ data: null, loading: true, error: null });
        setProgress(0);

        try {
            const response = await api.uploadDataset(file, (prog) => {
                setProgress(prog);
            });
            setState({ data: response, loading: false, error: null });
            setProgress(100);
            return response;
        } catch (error) {
            const errorMessage = error instanceof ApiError
                ? error.message
                : 'Failed to upload file';
            setState({ data: null, loading: false, error: errorMessage });
            setProgress(0);
            throw error;
        }
    }, []);

    const reset = useCallback(() => {
        setState({ data: null, loading: false, error: null });
        setProgress(0);
    }, []);

    return { ...state, upload, reset, progress };
}

/**
 * Hook for dataset analysis
 */
export function useAnalyzeDataset() {
    const [state, setState] = useState<ApiState<AnalysisResponse>>({
        data: null,
        loading: false,
        error: null,
    });

    const analyze = useCallback(async (datasetId: string) => {
        setState({ data: null, loading: true, error: null });

        try {
            const response = await api.analyzeDataset(datasetId);
            setState({ data: response, loading: false, error: null });
            return response;
        } catch (error) {
            const errorMessage = error instanceof ApiError
                ? error.message
                : 'Failed to analyze dataset';
            setState({ data: null, loading: false, error: errorMessage });
            throw error;
        }
    }, []);

    const reset = useCallback(() => {
        setState({ data: null, loading: false, error: null });
    }, []);

    return { ...state, analyze, reset };
}

/**
 * Generic API hook for any endpoint
 */
export function useApi<T>(
    apiCall: () => Promise<T>,
    immediate: boolean = false
) {
    const [state, setState] = useState<ApiState<T>>({
        data: null,
        loading: immediate,
        error: null,
    });

    const execute = useCallback(async () => {
        setState({ data: null, loading: true, error: null });

        try {
            const response = await apiCall();
            setState({ data: response, loading: false, error: null });
            return response;
        } catch (error) {
            const errorMessage = error instanceof ApiError
                ? error.message
                : 'API request failed';
            setState({ data: null, loading: false, error: errorMessage });
            throw error;
        }
    }, [apiCall]);

    useEffect(() => {
        if (immediate) {
            execute();
        }
    }, [immediate, execute]);

    const reset = useCallback(() => {
        setState({ data: null, loading: false, error: null });
    }, []);

    return { ...state, execute, reset };
}
