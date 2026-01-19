import React, { useState } from 'react';

interface TemplateEditorProps {
  templateId?: string;
  templateName: string;
  templateDescription?: string;
  templateType: string;
  currentContent: string;
  onSave: (name: string, content: string, description?: string) => Promise<void>;
  onCancel: () => void;
}

export default function TemplateEditor({
  templateId,
  templateName,
  templateDescription = '',
  templateType,
  currentContent,
  onSave,
  onCancel
}: TemplateEditorProps) {
  const [name, setName] = useState(templateName);
  const [description, setDescription] = useState(templateDescription);
  const [content, setContent] = useState(currentContent);
  const [isPreviewMode, setIsPreviewMode] = useState(false);
  const [saving, setSaving] = useState(false);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  const validateTemplate = () => {
    const errors: string[] = [];
    
    if (!name.trim()) {
      errors.push('Template name is required');
    }
    
    if (!content.trim()) {
      errors.push('Template content is required');
    }

    // Check for required template structure
    if (!content.includes('<div class="header">')) {
      errors.push('Template should include a header section');
    }

    if (!content.includes('<div class="content">')) {
      errors.push('Template should include a content section');
    }

    if (!content.includes('<div class="footer">')) {
      errors.push('Template should include a footer section');
    }

    // Check for basic CSS styling
    if (!content.includes('<style>')) {
      errors.push('Template should include CSS styling');
    }

    setValidationErrors(errors);
    return errors.length === 0;
  };

  const handleSave = async () => {
    if (!validateTemplate()) {
      return;
    }

    setSaving(true);
    try {
      await onSave(name, content, description);
    } finally {
      setSaving(false);
    }
  };

  const insertHandlebarHelper = (helper: string) => {
    const textarea = document.getElementById('template-editor') as HTMLTextAreaElement;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newContent = content.substring(0, start) + helper + content.substring(end);
      setContent(newContent);
      
      // Restore cursor position
      setTimeout(() => {
        textarea.focus();
        textarea.setSelectionRange(start + helper.length, start + helper.length);
      }, 0);
    }
  };

  const handlebarsHelpers = [
    { label: 'Customer Name', value: '{{customer.fullName}}' },
    { label: 'Customer Email', value: '{{customer.email}}' },
    { label: 'Customer Phone', value: '{{customer.phoneNumber}}' },
    { label: 'Customer Address', value: '{{customer.address.fullAddress}}' },
    { label: 'Sale ID', value: '{{metadata.saleId}}' },
    { label: 'Agent Name', value: '{{metadata.agentName}}' },
    { label: 'Generation Date', value: '{{date metadata.generationDate "long"}}' },
    { label: 'Monthly Payment', value: '{{agreement.monthlyPaymentFormatted}}' },
    { label: 'Monthly Payment', value: '{{agreement.monthlyPaymentFormatted}}' },
    { label: 'Direct Debit Date', value: '{{date agreement.directDebitDate "long"}}' },
    { label: 'Account Name', value: '{{agreement.accountDetails.accountName}}' },
    { label: 'Sort Code', value: '{{agreement.accountDetails.sortCodeFormatted}}' },
    { label: 'Account Number', value: '{{agreement.accountDetails.accountNumberMasked}}' }
  ];

  const conditionalHelpers = [
    { label: 'If Appliance Cover', value: '{{#if agreement.coverage.hasApplianceCover}}\n<!-- content -->\n{{/if}}' },
    { label: 'If Boiler Cover', value: '{{#if agreement.coverage.hasBoilerCover}}\n<!-- content -->\n{{/if}}' },
    { label: 'Appliance Loop', value: '{{#each appliances}}\n<!-- appliance: {{this.name}} - {{this.costFormatted}} -->\n{{/each}}' }
  ];

  return (
    <div className="template-editor-container">
      <div className="editor-header">
        <div className="header-left">
          <h2 className="editor-title">
            {templateId ? 'Edit Template' : 'Create New Template'}
          </h2>
          <span className="template-type-badge">
            {templateType.replace('_', ' ').toUpperCase()}
          </span>
        </div>
        
        <div className="header-controls">
          <button
            type="button"
            onClick={() => setIsPreviewMode(!isPreviewMode)}
            className="btn-preview"
          >
            {isPreviewMode ? 'Edit' : 'Preview'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="btn-cancel"
            disabled={saving}
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleSave}
            className="btn-save"
            disabled={saving || validationErrors.length > 0}
          >
            {saving ? 'Saving...' : 'Save Template'}
          </button>
        </div>
      </div>

      {validationErrors.length > 0 && (
        <div className="validation-errors">
          <h4>Please fix the following issues:</h4>
          <ul>
            {validationErrors.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="editor-body">
        <div className="editor-sidebar">
          <div className="template-settings">
            <h3>Template Settings</h3>
            <div className="form-group">
              <label htmlFor="template-name">Template Name</label>
              <input
                id="template-name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter template name"
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="template-description">Description (Optional)</label>
              <input
                id="template-description"
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief description of the template"
                className="form-input"
              />
            </div>
          </div>

          <div className="helpers-section">
            <h3>Template Variables</h3>
            <div className="helpers-group">
              <h4>Customer Data</h4>
              <div className="helper-buttons">
                {handlebarsHelpers.slice(0, 7).map((helper, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => insertHandlebarHelper(helper.value)}
                    className="helper-btn"
                    title={helper.value}
                  >
                    {helper.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="helpers-group">
              <h4>Agreement Data</h4>
              <div className="helper-buttons">
                {handlebarsHelpers.slice(7).map((helper, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => insertHandlebarHelper(helper.value)}
                    className="helper-btn"
                    title={helper.value}
                  >
                    {helper.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="helpers-group">
              <h4>Conditional Logic</h4>
              <div className="helper-buttons">
                {conditionalHelpers.map((helper, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => insertHandlebarHelper(helper.value)}
                    className="helper-btn conditional"
                    title={helper.value}
                  >
                    {helper.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="template-tips">
            <h3>Tips</h3>
            <ul>
              <li>Use semantic HTML structure</li>
              <li>Include header, content, and footer sections</li>
              <li>Add CSS styling for professional appearance</li>
              <li>Test with preview mode before saving</li>
              <li>Use conditional blocks for optional content</li>
            </ul>
          </div>
        </div>

        <div className="editor-main">
          {isPreviewMode ? (
            <div className="preview-container">
              <div className="preview-header">
                <h3>Template Preview</h3>
                <p>This shows how your template will appear when rendered</p>
              </div>
              <div className="preview-content">
                <iframe
                  srcDoc={content}
                  className="preview-frame"
                  title="Template Preview"
                />
              </div>
            </div>
          ) : (
            <div className="code-editor">
              <div className="editor-toolbar">
                <span className="editor-mode">HTML + CSS Editor</span>
                <div className="editor-stats">
                  Lines: {content.split('\n').length} | 
                  Characters: {content.length}
                </div>
              </div>
              <textarea
                id="template-editor"
                value={content}
                onChange={(e) => {
                  setContent(e.target.value);
                  if (validationErrors.length > 0) {
                    setValidationErrors([]);
                  }
                }}
                className="code-textarea"
                spellCheck={false}
                placeholder="Enter your HTML template with CSS styling..."
              />
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .template-editor-container {
          background: white;
          border-radius: 12px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
          overflow: hidden;
          height: 90vh;
          display: flex;
          flex-direction: column;
        }

        .editor-header {
          background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
          color: white;
          padding: 20px 24px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .editor-title {
          font-size: 20px;
          font-weight: 600;
          margin: 0;
        }

        .template-type-badge {
          background: rgba(255, 255, 255, 0.2);
          padding: 4px 12px;
          border-radius: 20px;
          font-size: 12px;
          font-weight: 500;
        }

        .header-controls {
          display: flex;
          gap: 12px;
        }

        .btn-preview, .btn-cancel, .btn-save {
          padding: 8px 16px;
          border-radius: 6px;
          border: none;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-preview {
          background: rgba(255, 255, 255, 0.2);
          color: white;
        }

        .btn-preview:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        .btn-cancel {
          background: #6b7280;
          color: white;
        }

        .btn-cancel:hover {
          background: #4b5563;
        }

        .btn-save {
          background: #10b981;
          color: white;
        }

        .btn-save:hover {
          background: #059669;
        }

        .btn-save:disabled, .btn-cancel:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .validation-errors {
          background: #fef2f2;
          border-left: 4px solid #ef4444;
          padding: 16px;
          margin: 0;
        }

        .validation-errors h4 {
          color: #dc2626;
          font-size: 14px;
          margin: 0 0 8px;
        }

        .validation-errors ul {
          margin: 0;
          padding-left: 20px;
          color: #b91c1c;
          font-size: 14px;
        }

        .validation-errors li {
          margin-bottom: 4px;
        }

        .editor-body {
          display: grid;
          grid-template-columns: 300px 1fr;
          height: 100%;
          overflow: hidden;
        }

        .editor-sidebar {
          background: #f8fafc;
          border-right: 1px solid #e2e8f0;
          padding: 20px;
          overflow-y: auto;
        }

        .template-settings, .helpers-section, .template-tips {
          margin-bottom: 24px;
        }

        .template-settings h3, .helpers-section h3, .template-tips h3 {
          color: #374151;
          font-size: 16px;
          font-weight: 600;
          margin: 0 0 12px;
          border-bottom: 2px solid #e5e7eb;
          padding-bottom: 4px;
        }

        .form-group {
          margin-bottom: 16px;
        }

        .form-group label {
          display: block;
          color: #374151;
          font-weight: 500;
          margin-bottom: 4px;
          font-size: 14px;
        }

        .form-input {
          width: 100%;
          padding: 8px 12px;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          font-size: 14px;
        }

        .form-input:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .helpers-group {
          margin-bottom: 16px;
        }

        .helpers-group h4 {
          color: #6b7280;
          font-size: 14px;
          font-weight: 500;
          margin: 0 0 8px;
        }

        .helper-buttons {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .helper-btn {
          background: white;
          border: 1px solid #d1d5db;
          border-radius: 4px;
          padding: 6px 10px;
          text-align: left;
          font-size: 12px;
          cursor: pointer;
          transition: all 0.2s ease;
          color: #374151;
        }

        .helper-btn:hover {
          background: #f3f4f6;
          border-color: #9ca3af;
        }

        .helper-btn.conditional {
          background: #fef3c7;
          border-color: #f59e0b;
          color: #92400e;
        }

        .helper-btn.conditional:hover {
          background: #fef3c7;
          border-color: #d97706;
        }

        .template-tips ul {
          margin: 0;
          padding-left: 16px;
          color: #6b7280;
          font-size: 12px;
        }

        .template-tips li {
          margin-bottom: 4px;
        }

        .editor-main {
          display: flex;
          flex-direction: column;
          height: 100%;
          overflow: hidden;
        }

        .preview-container {
          height: 100%;
          display: flex;
          flex-direction: column;
        }

        .preview-header {
          background: #f8fafc;
          padding: 16px;
          border-bottom: 1px solid #e2e8f0;
        }

        .preview-header h3 {
          margin: 0 0 4px;
          color: #374151;
          font-size: 16px;
        }

        .preview-header p {
          margin: 0;
          color: #6b7280;
          font-size: 14px;
        }

        .preview-content {
          flex: 1;
          overflow: hidden;
        }

        .preview-frame {
          width: 100%;
          height: 100%;
          border: none;
          background: white;
        }

        .code-editor {
          height: 100%;
          display: flex;
          flex-direction: column;
        }

        .editor-toolbar {
          background: #f8fafc;
          padding: 12px 16px;
          border-bottom: 1px solid #e2e8f0;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .editor-mode {
          color: #6b7280;
          font-size: 14px;
          font-weight: 500;
        }

        .editor-stats {
          color: #9ca3af;
          font-size: 12px;
          font-family: monospace;
        }

        .code-textarea {
          flex: 1;
          border: none;
          padding: 16px;
          font-family: 'Fira Code', 'Monaco', 'Cascadia Code', monospace;
          font-size: 13px;
          line-height: 1.6;
          resize: none;
          outline: none;
          background: #fafafa;
          color: #374151;
        }

        .code-textarea:focus {
          background: white;
        }

        @media (max-width: 1024px) {
          .editor-body {
            grid-template-columns: 250px 1fr;
          }
          
          .editor-sidebar {
            padding: 16px;
          }
        }

        @media (max-width: 768px) {
          .template-editor-container {
            height: 100vh;
          }
          
          .editor-header {
            flex-direction: column;
            gap: 12px;
            align-items: stretch;
          }
          
          .header-controls {
            justify-content: center;
          }
          
          .editor-body {
            grid-template-columns: 1fr;
            grid-template-rows: 200px 1fr;
          }
          
          .editor-sidebar {
            overflow-y: auto;
          }
        }
      `}</style>
    </div>
  );
}