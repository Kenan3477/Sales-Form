import React, { useState } from 'react';

interface BulkOperationsProps {
  selectedSales: string[];
  onBulkGenerate: (templateIds: string[], salesIds: string[]) => Promise<void>;
  onClearSelection: () => void;
  availableTemplates: { id: string; name: string; templateType: string }[];
}

export default function BulkOperations({
  selectedSales,
  onBulkGenerate,
  onClearSelection,
  availableTemplates
}: BulkOperationsProps) {
  const [selectedTemplates, setSelectedTemplates] = useState<string[]>([]);
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState<{ success: number; failed: number; errors: string[] } | null>(null);

  const handleTemplateToggle = (templateId: string) => {
    setSelectedTemplates(prev =>
      prev.includes(templateId)
        ? prev.filter(id => id !== templateId)
        : [...prev, templateId]
    );
  };

  const handleBulkGenerate = async () => {
    if (selectedTemplates.length === 0 || selectedSales.length === 0) {
      return;
    }

    setProcessing(true);
    setResults(null);

    try {
      await onBulkGenerate(selectedTemplates, selectedSales);
      
      // Mock results for demo - in real implementation this would come from the API
      setResults({
        success: selectedSales.length * selectedTemplates.length,
        failed: 0,
        errors: []
      });
    } catch (error) {
      setResults({
        success: 0,
        failed: selectedSales.length * selectedTemplates.length,
        errors: [error instanceof Error ? error.message : 'Unknown error occurred']
      });
    } finally {
      setProcessing(false);
    }
  };

  const totalOperations = selectedSales.length * selectedTemplates.length;

  return (
    <div className="bulk-operations-panel">
      <div className="panel-header">
        <h3 className="panel-title">Bulk Document Generation</h3>
        <p className="panel-subtitle">
          Generate documents for {selectedSales.length} selected sales
        </p>
      </div>

      <div className="template-selection">
        <h4 className="section-title">Select Templates to Generate</h4>
        <div className="template-grid">
          {availableTemplates.map((template) => (
            <label key={template.id} className="template-checkbox">
              <input
                type="checkbox"
                checked={selectedTemplates.includes(template.id)}
                onChange={() => handleTemplateToggle(template.id)}
                className="checkbox-input"
              />
              <div className="template-card">
                <div className="template-icon">
                  {template.templateType === 'welcome_letter' && '📄'}
                  {template.templateType === 'service_agreement' && '📋'}
                  {template.templateType === 'direct_debit_form' && '🏦'}
                  {template.templateType === 'coverage_summary' && '📊'}
                </div>
                <div className="template-info">
                  <h5 className="template-name">{template.name}</h5>
                  <p className="template-type">
                    {template.templateType?.replace('_', ' ').toUpperCase() || 'UNKNOWN TYPE'}
                  </p>
                </div>
              </div>
            </label>
          ))}
        </div>
      </div>

      {selectedTemplates.length > 0 && (
        <div className="operation-summary">
          <div className="summary-card">
            <h4 className="summary-title">Generation Summary</h4>
            <div className="summary-stats">
              <div className="stat">
                <span className="stat-label">Selected Sales:</span>
                <span className="stat-value">{selectedSales.length}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Selected Templates:</span>
                <span className="stat-value">{selectedTemplates.length}</span>
              </div>
              <div className="stat total">
                <span className="stat-label">Total Documents:</span>
                <span className="stat-value">{totalOperations}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {results && (
        <div className="results-section">
          <div className={`results-card ${results.failed > 0 ? 'has-errors' : 'success'}`}>
            <h4 className="results-title">Generation Results</h4>
            <div className="results-stats">
              <div className="result-stat success">
                <span className="stat-icon">✅</span>
                <span className="stat-text">
                  {results.success} documents generated successfully
                </span>
              </div>
              {results.failed > 0 && (
                <div className="result-stat error">
                  <span className="stat-icon">❌</span>
                  <span className="stat-text">
                    {results.failed} documents failed to generate
                  </span>
                </div>
              )}
            </div>
            {results.errors.length > 0 && (
              <div className="error-details">
                <h5>Error Details:</h5>
                <ul>
                  {results.errors.map((error, index) => (
                    <li key={index}>{error}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="action-buttons">
        <button
          onClick={onClearSelection}
          className="btn-secondary"
          disabled={processing}
        >
          Clear Selection
        </button>
        <button
          onClick={handleBulkGenerate}
          disabled={selectedTemplates.length === 0 || selectedSales.length === 0 || processing}
          className="btn-primary"
        >
          {processing ? (
            <>
              <span className="spinner"></span>
              Generating {totalOperations} Documents...
            </>
          ) : (
            `Generate ${totalOperations} Documents`
          )}
        </button>
      </div>

      <style jsx>{`
        .bulk-operations-panel {
          background: white;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
          border: 1px solid #e5e7eb;
        }

        .panel-header {
          margin-bottom: 24px;
        }

        .panel-title {
          font-size: 20px;
          font-weight: 600;
          color: #374151;
          margin: 0 0 4px;
        }

        .panel-subtitle {
          color: #6b7280;
          margin: 0;
        }

        .section-title {
          font-size: 16px;
          font-weight: 500;
          color: #374151;
          margin: 0 0 16px;
        }

        .template-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 12px;
          margin-bottom: 24px;
        }

        .template-checkbox {
          cursor: pointer;
          display: block;
        }

        .checkbox-input {
          display: none;
        }

        .template-card {
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          padding: 16px;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .template-checkbox:hover .template-card {
          border-color: #3b82f6;
        }

        .checkbox-input:checked + .template-card {
          border-color: #3b82f6;
          background: #f0f9ff;
        }

        .template-icon {
          font-size: 24px;
          width: 40px;
          text-align: center;
        }

        .template-info {
          flex: 1;
        }

        .template-name {
          font-size: 14px;
          font-weight: 500;
          color: #374151;
          margin: 0 0 2px;
        }

        .template-type {
          font-size: 12px;
          color: #6b7280;
          margin: 0;
        }

        .operation-summary {
          margin-bottom: 24px;
        }

        .summary-card {
          background: #f8fafc;
          border-radius: 8px;
          padding: 16px;
          border-left: 4px solid #3b82f6;
        }

        .summary-title {
          font-size: 14px;
          font-weight: 500;
          color: #374151;
          margin: 0 0 12px;
        }

        .summary-stats {
          display: flex;
          flex-wrap: wrap;
          gap: 16px;
        }

        .stat {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .stat.total {
          padding-left: 16px;
          border-left: 2px solid #d1d5db;
          font-weight: 600;
        }

        .stat-label {
          font-size: 14px;
          color: #6b7280;
        }

        .stat-value {
          font-size: 14px;
          font-weight: 600;
          color: #374151;
        }

        .results-section {
          margin-bottom: 24px;
        }

        .results-card {
          border-radius: 8px;
          padding: 16px;
        }

        .results-card.success {
          background: #f0fdf4;
          border-left: 4px solid #10b981;
        }

        .results-card.has-errors {
          background: #fef2f2;
          border-left: 4px solid #ef4444;
        }

        .results-title {
          font-size: 14px;
          font-weight: 500;
          color: #374151;
          margin: 0 0 12px;
        }

        .results-stats {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .result-stat {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .stat-icon {
          font-size: 16px;
        }

        .stat-text {
          font-size: 14px;
        }

        .result-stat.success .stat-text {
          color: #065f46;
        }

        .result-stat.error .stat-text {
          color: #b91c1c;
        }

        .error-details {
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid #fecaca;
        }

        .error-details h5 {
          font-size: 14px;
          font-weight: 500;
          color: #b91c1c;
          margin: 0 0 8px;
        }

        .error-details ul {
          margin: 0;
          padding-left: 20px;
          color: #b91c1c;
          font-size: 12px;
        }

        .error-details li {
          margin-bottom: 4px;
        }

        .action-buttons {
          display: flex;
          justify-content: space-between;
          gap: 12px;
        }

        .btn-secondary, .btn-primary {
          padding: 12px 20px;
          border-radius: 6px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
          border: none;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .btn-secondary {
          background: #f3f4f6;
          color: #6b7280;
        }

        .btn-secondary:hover {
          background: #e5e7eb;
        }

        .btn-primary {
          background: #3b82f6;
          color: white;
          flex: 1;
        }

        .btn-primary:hover:not(:disabled) {
          background: #2563eb;
        }

        .btn-primary:disabled, .btn-secondary:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top: 2px solid white;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
          .template-grid {
            grid-template-columns: 1fr;
          }
          
          .summary-stats {
            flex-direction: column;
          }
          
          .stat.total {
            padding-left: 0;
            border-left: none;
            border-top: 2px solid #d1d5db;
            padding-top: 8px;
          }
          
          .action-buttons {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
}