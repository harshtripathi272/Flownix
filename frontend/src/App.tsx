import { useState } from 'react'
import { useHealthCheck, useUploadDataset } from './hooks/useApi'
import { config } from './config/config'
import type { DatasetInfo } from './types/types'

function App() {
    const { data: healthData, loading: healthLoading, error: healthError } = useHealthCheck()
    const { upload, loading: uploadLoading, error: uploadError, reset } = useUploadDataset()
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [datasetInfo, setDatasetInfo] = useState<DatasetInfo | null>(null)

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (file) {
            setSelectedFile(file)
            reset()
            setDatasetInfo(null)
        }
    }

    const handleUpload = async () => {
        if (!selectedFile) return

        try {
            const response = await upload(selectedFile)
            if (response.status === 'success' && response.data) {
                setDatasetInfo(response.data)
            }
        } catch (error) {
            console.error('Upload failed:', error)
        }
    }

    const formatFileSize = (bytes: number): string => {
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    }

    const isConnected = healthData?.status === 'healthy'

    return (
        <div className="container">
            <header className="header">
                <h1>🌊 Flownix</h1>
                <p className="subtitle">Intelligent ML Pipeline Engine</p>

                {/* Backend Status */}
                <div className={`status-badge ${isConnected ? 'connected' : 'disconnected'}`}>
                    <span className="status-dot"></span>
                    {healthLoading ? 'Connecting...' : isConnected ? 'Backend Connected' : 'Backend Disconnected'}
                </div>

                {healthError && (
                    <div className="error-message">
                        ⚠️ {healthError}
                    </div>
                )}
            </header>

            <main className="main-content">
                {/* File Upload Section */}
                <section className="upload-section">
                    <h2>Upload Dataset</h2>
                    <p className="section-description">
                        Upload your dataset to begin analysis. Supported formats: {config.upload.supportedFormats.join(', ')}
                    </p>

                    <div className="upload-area">
                        <input
                            type="file"
                            id="file-input"
                            className="file-input"
                            accept={config.upload.supportedFormats.join(',')}
                            onChange={handleFileSelect}
                            disabled={uploadLoading || !isConnected}
                        />
                        <label htmlFor="file-input" className="file-label">
                            <div className="upload-icon">📁</div>
                            <div className="upload-text">
                                {selectedFile ? selectedFile.name : 'Choose a file or drag it here'}
                            </div>
                            {selectedFile && (
                                <div className="file-size">
                                    {formatFileSize(selectedFile.size)}
                                </div>
                            )}
                        </label>
                    </div>

                    {selectedFile && (
                        <button
                            className="upload-button"
                            onClick={handleUpload}
                            disabled={uploadLoading || !isConnected}
                        >
                            {uploadLoading ? '⏳ Uploading...' : '🚀 Upload & Analyze'}
                        </button>
                    )}

                    {uploadError && (
                        <div className="error-message">
                            ❌ {uploadError}
                        </div>
                    )}
                </section>

                {/* Dataset Info Section */}
                {datasetInfo && (
                    <section className="dataset-info">
                        <h2>✅ Dataset Uploaded Successfully</h2>

                        <div className="info-grid">
                            <div className="info-card">
                                <div className="info-label">Filename</div>
                                <div className="info-value">{datasetInfo.filename}</div>
                            </div>

                            <div className="info-card">
                                <div className="info-label">File Type</div>
                                <div className="info-value">{datasetInfo.file_type}</div>
                            </div>

                            <div className="info-card">
                                <div className="info-label">Size</div>
                                <div className="info-value">{datasetInfo.file_size_mb} MB</div>
                            </div>

                            <div className="info-card">
                                <div className="info-label">Rows</div>
                                <div className="info-value">{datasetInfo.rows.toLocaleString()}</div>
                            </div>

                            <div className="info-card">
                                <div className="info-label">Columns</div>
                                <div className="info-value">{datasetInfo.columns}</div>
                            </div>

                            <div className="info-card">
                                <div className="info-label">Missing Values</div>
                                <div className="info-value">{datasetInfo.total_missing.toLocaleString()}</div>
                            </div>
                        </div>

                        <div className="column-types">
                            <h3>Column Types</h3>
                            <div className="type-badges">
                                {datasetInfo.numeric_columns.length > 0 && (
                                    <span className="type-badge numeric">
                                        📊 {datasetInfo.numeric_columns.length} Numeric
                                    </span>
                                )}
                                {datasetInfo.categorical_columns.length > 0 && (
                                    <span className="type-badge categorical">
                                        🏷️ {datasetInfo.categorical_columns.length} Categorical
                                    </span>
                                )}
                                {datasetInfo.datetime_columns.length > 0 && (
                                    <span className="type-badge datetime">
                                        📅 {datasetInfo.datetime_columns.length} DateTime
                                    </span>
                                )}
                            </div>
                        </div>

                        {datasetInfo.preview && datasetInfo.preview.length > 0 && (
                            <div className="preview-section">
                                <h3>Data Preview (First 5 Rows)</h3>
                                <div className="table-container">
                                    <table className="data-table">
                                        <thead>
                                            <tr>
                                                {datasetInfo.column_names.map((col) => (
                                                    <th key={col}>{col}</th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {datasetInfo.preview.map((row, idx) => (
                                                <tr key={idx}>
                                                    {datasetInfo.column_names.map((col) => (
                                                        <td key={col}>
                                                            {row[col] !== null && row[col] !== undefined
                                                                ? String(row[col])
                                                                : '—'}
                                                        </td>
                                                    ))}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}
                    </section>
                )}
            </main>

            <footer className="footer">
                <p>Flownix v{config.app.version} • Backend API: {config.api.baseUrl}</p>
            </footer>
        </div>
    )
}

export default App

