/**
 * Application Configuration
 * Centralized configuration for API endpoints and app settings
 */

const isDevelopment = process.env.NODE_ENV === 'development';

export const config = {
    // API Configuration
    api: {
        baseUrl: isDevelopment
            ? 'http://localhost:8000'
            : process.env.VITE_API_URL || 'http://localhost:8000',
        prefix: '/api/v1',
        timeout: 30000, // 30 seconds
    },

    // Upload Configuration
    upload: {
        maxSizeMB: 100,
        maxSizeBytes: 100 * 1024 * 1024,
        supportedFormats: ['.csv', '.xlsx', '.xls', '.json', '.parquet'],
        supportedMimeTypes: [
            'text/csv',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/json',
            'application/octet-stream', // for parquet
        ],
    },

    // App Configuration
    app: {
        name: 'Flownix',
        version: '0.1.0',
    },
} as const;

// Helper function to get full API URL
export const getApiUrl = (endpoint: string): string => {
    const { baseUrl, prefix } = config.api;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${baseUrl}${prefix}${cleanEndpoint}`;
};

// Helper function to get base API URL (without prefix)
export const getBaseApiUrl = (endpoint: string): string => {
    const { baseUrl } = config.api;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${baseUrl}${cleanEndpoint}`;
};
