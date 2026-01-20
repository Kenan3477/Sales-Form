'use client';

import { useState, useEffect, useCallback } from 'react';
import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation';
import TemplateEditor from '../../../components/paperwork/TemplateEditor';
import { formatCurrency } from '@/lib/schemas';

interface DocumentTemplate {
  id: string;
  name: string;
  description?: string | null;
  templateType: string;
  htmlContent: string;
  version: number;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

interface GeneratedDocument {
  id: string;
  saleId: string;
  templateId: string;
  templateName: string;
  fileName: string;
  downloadCount: number;
  createdAt: string;
  sale: {
    id: string;
    customer: {
      fullName: string;
      email: string;
    };
    status: string;
  };
}

export default function AdminPaperworkPage() {
  const { data: session, status } = useSession();
  const [activeTab, setActiveTab] = useState<'templates' | 'documents' | 'generate'>('templates');
  const [templates, setTemplates] = useState<DocumentTemplate[]>([]);
  const [documents, setDocuments] = useState<GeneratedDocument[]>([]);
  const [sales, setSales] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showEditor, setShowEditor] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<DocumentTemplate | null>(null);
  const [newTemplateType, setNewTemplateType] = useState<string>('');
  const [selectedSales, setSelectedSales] = useState<string[]>([]);
  const [selectedTemplates, setSelectedTemplates] = useState<string[]>([]);
  const [generating, setGenerating] = useState(false);
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);
  const [documentFilter, setDocumentFilter] = useState<'all' | 'downloaded' | 'undownloaded'>('all');
  const [customerStatusFilter, setCustomerStatusFilter] = useState<string>('all');
  const [documentsGeneratedFilter, setDocumentsGeneratedFilter] = useState<'all' | 'generated' | 'not-generated'>('all');
  const [bulkDownloading, setBulkDownloading] = useState(false);

  // Redirect if not admin
  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (!session || session.user.role !== 'ADMIN') {
    redirect('/dashboard');
  }

  const fetchData = useCallback(async () => {
    // Don't fetch if not authenticated or not admin
    if (!session?.user || session.user.role !== 'ADMIN') {
      console.log('📋 Not authenticated or not admin, skipping fetch');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      if (activeTab === 'templates') {
        const response = await fetch('/api/paperwork/templates');
        if (!response.ok) throw new Error('Failed to fetch templates');
        const data = await response.json();
        setTemplates(data.templates || []);
      } else if (activeTab === 'documents') {
        console.log('📋 Fetching documents...');
        const url = new URL('/api/paperwork/documents', window.location.origin);
        if (customerStatusFilter !== 'all') {
          url.searchParams.set('customerStatus', customerStatusFilter);
        }
        const response = await fetch(url.toString());
        if (!response.ok) throw new Error('Failed to fetch documents');
        const data = await response.json();
        console.log('📋 Documents response:', data);
        setDocuments(data.documents || []);
      } else if (activeTab === 'generate') {
        // Fetch both templates and sales data
        const salesUrl = new URL('/api/sales', window.location.origin);
        if (customerStatusFilter !== 'all') {
          salesUrl.searchParams.set('status', customerStatusFilter.toUpperCase());
        }
        
        const [templatesResponse, salesResponse] = await Promise.all([
          fetch('/api/paperwork/templates?activeOnly=true'),
          fetch(salesUrl.toString())
        ]);
        
        if (!templatesResponse.ok) throw new Error('Failed to fetch templates');
        if (!salesResponse.ok) throw new Error('Failed to fetch sales');
        
        const templatesData = await templatesResponse.json();
        const salesData = await salesResponse.json();
        
        console.log('📋 Templates data received:', templatesData);
        console.log('📋 Individual templates:', templatesData.templates);
        
        setTemplates(templatesData.templates || []);
        
        // Transform sales data to match expected format
        const rawSales = Array.isArray(salesData) ? salesData : salesData.sales || [];
        const transformedSales = rawSales.map((sale: any) => ({
          ...sale,
          customer: {
            fullName: `${sale.customerFirstName} ${sale.customerLastName}`,
            email: sale.email
          },
          totalPrice: sale.totalPlanCost || 0
        }));
        setSales(transformedSales);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [activeTab, customerStatusFilter, documentsGeneratedFilter, session]);

  useEffect(() => {
    // Only fetch data when properly authenticated
    if (session?.user && session.user.role === 'ADMIN') {
      fetchData();
    }
  }, [fetchData, session]);

  const toggleTemplateStatus = async (templateId: string, currentStatus: boolean) => {
    try {
      const response = await fetch(`/api/paperwork/templates/${templateId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ isActive: !currentStatus })
      });

      if (!response.ok) throw new Error('Failed to update template');
      
      await fetchData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update template');
    }
  };

  const handleCreateTemplate = (templateType: string) => {
    // Set up a new template for creation
    const newTemplate: DocumentTemplate = {
      id: '',
      name: `New ${templateType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}`,
      description: `Template for generating ${templateType.replace('_', ' ').toLowerCase()} documents`,
      templateType: templateType,
      htmlContent: `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${templateType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</title>
</head>
<body>
  <h1>${templateType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h1>
  <p>Dear {{customerName}},</p>
  
  <p>Your template content goes here...</p>
  
  <!-- Available variables: -->
  <!-- {{customerName}}, {{email}}, {{phone}}, {{address}} -->
  <!-- {{totalCost}}, {{monthlyCost}}, {{policyNumber}} -->
  <!-- {{coverageStartDate}}, {{currentDate}} -->
  
  <p>Best regards,<br>The Flash Team</p>
</body>
</html>`,
      version: 1,
      isActive: true,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    setEditingTemplate(newTemplate);
    setShowEditor(true);
    setNewTemplateType('');
  };

  const handleEditTemplate = (template: DocumentTemplate) => {
    setEditingTemplate(template);
    setShowEditor(true);
  };

  const handleSaveTemplate = async (name: string, content: string, description?: string) => {
    if (!editingTemplate) return;

    try {
      const url = editingTemplate.id 
        ? `/api/paperwork/templates/${editingTemplate.id}`
        : '/api/paperwork/templates';
      
      const method = editingTemplate.id ? 'PUT' : 'POST';
      
      const requestBody: any = {
        name,
        description: description || null,
        templateType: editingTemplate.templateType,
        htmlContent: content,
        isActive: true
      };

      // Add ID for PUT requests
      if (method === 'PUT') {
        requestBody.id = editingTemplate.id;
      }
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to save template');
      }

      const result = await response.json();
      console.log('Template saved successfully:', result);

      setShowEditor(false);
      setEditingTemplate(null);
      await fetchData();
      
      // Show success message
      setError(null);
    } catch (err) {
      console.error('Save template error:', err);
      setError(err instanceof Error ? err.message : 'Failed to save template');
    }
  };

  const handleDeleteTemplate = async (template: DocumentTemplate) => {
    // Prevent deletion of system templates
    if (['welcome-letter', 'service-agreement', 'direct-debit-form', 'coverage-summary'].includes(template.id)) {
      setError('Cannot delete system templates.');
      return;
    }

    if (!confirm(`Are you sure you want to delete "${template.name}"? This action cannot be undone.`)) {
      return;
    }

    try {
      const response = await fetch(`/api/paperwork/templates/${template.id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete template');
      }

      const result = await response.json();
      console.log('Template deleted:', result);

      // Refresh templates list
      await fetchData();
      setError(null);
      
    } catch (err) {
      console.error('Delete template error:', err);
      setError(err instanceof Error ? err.message : 'Failed to delete template');
    }
  };

  const handleCancelEdit = () => {
    setShowEditor(false);
    setEditingTemplate(null);
    setNewTemplateType('');
  };

  const handleSaleSelection = (saleId: string) => {
    setSelectedSales(prev => 
      prev.includes(saleId) 
        ? prev.filter(id => id !== saleId)
        : [...prev, saleId]
    );
  };

  const handleSelectAllSales = () => {
    const filteredSales = getFilteredSales();
    if (selectedSales.length === filteredSales.length) {
      setSelectedSales([]);
    } else {
      setSelectedSales(filteredSales.map(sale => sale.id));
    }
  };

  const handleBulkGenerate = async (templateIds: string[]) => {
    if (selectedSales.length === 0 || templateIds.length === 0) {
      setError('Please select at least one sale and one template');
      return;
    }
    
    console.log('Starting bulk generation with:', {
      selectedSales,
      templateIds,
      salesData: sales.filter(s => selectedSales.includes(s.id))
    });

    setGenerating(true);
    try {
      const requestBody = {
        saleIds: selectedSales,
        templateIds: templateIds
      };
      
      console.log('Request body:', requestBody);
      
      const response = await fetch('/api/paperwork/generate/bulk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Error response:', errorData);
        throw new Error(errorData.message || 'Failed to generate documents');
      }

      const result = await response.json();
      console.log('Success result:', result);
      
      // Log detailed error information if there are failures
      if (result.failed > 0) {
        console.error('❌ Generation failures:', result.failed);
        console.error('❌ Error details:', result.errors);
        result.errors?.forEach((error: string, index: number) => {
          console.error(`❌ Error ${index + 1}:`, error);
        });
      }
      
      if (result.generated > 0) {
        console.log(`✅ Successfully generated ${result.generated} documents`);
        result.documents?.forEach((doc: any, index: number) => {
          console.log(`📄 Document ${index + 1}:`, {
            fileName: doc.fileName,
            customer: doc.customerName,
            templateName: doc.templateName
          });
        });
      }
      
      // Show success message and refresh data
      setError(null);
      
      // Show detailed message including failures
      const message = result.generated > 0 
        ? `Successfully generated ${result.generated} documents!${result.failed > 0 ? ` (${result.failed} failed)` : ''}`
        : `Failed to generate documents. ${result.errors?.join(', ') || 'Unknown error'}`;
        
      alert(message);
      setSelectedSales([]);
      await fetchData();
    } catch (err) {
      console.error('Bulk generation error:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate documents');
    } finally {
      setGenerating(false);
    }
  };

  // Document management functions
  const handleDocumentSelection = (documentId: string) => {
    setSelectedDocuments(prev => 
      prev.includes(documentId) 
        ? prev.filter(id => id !== documentId)
        : [...prev, documentId]
    );
  };

  const handleSelectAllDocuments = () => {
    const filteredDocuments = getFilteredDocuments();
    if (selectedDocuments.length === filteredDocuments.length) {
      setSelectedDocuments([]);
    } else {
      setSelectedDocuments(filteredDocuments.map(doc => doc.id));
    }
  };

  const getFilteredDocuments = () => {
    return documents.filter(doc => {
      if (documentFilter === 'downloaded') return doc.downloadCount > 0;
      if (documentFilter === 'undownloaded') return doc.downloadCount === 0;
      return true;
    });
  };

  const getFilteredSales = () => {
    return sales.filter(sale => {
      if (documentsGeneratedFilter === 'generated') return sale.documentsGenerated === true;
      if (documentsGeneratedFilter === 'not-generated') return !sale.documentsGenerated;
      return true;
    });
  };

  const handleBulkDownload = async (downloadAll: boolean = false) => {
    if (!downloadAll && selectedDocuments.length === 0) {
      setError('Please select at least one document to download');
      return;
    }

    setBulkDownloading(true);
    setError(null);

    try {
      const response = await fetch('/api/paperwork/bulk-download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          documentIds: selectedDocuments,
          downloadAll,
          filter: documentFilter !== 'all' ? documentFilter : undefined
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create document archive');
      }

      // Download the zip file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      
      // Get filename from response header or use default
      const contentDisposition = response.headers.get('content-disposition');
      const filename = contentDisposition?.match(/filename="([^"]+)"/)?.[1] || 'documents.zip';
      a.download = filename;
      
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      // Reset selection and refetch to update download counts
      setSelectedDocuments([]);
      await fetchData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to download documents');
    } finally {
      setBulkDownloading(false);
    }
  };

  const handleDeleteDocument = async (documentId: string) => {
    try {
      setError(null);
      
      const response = await fetch('/api/paperwork/delete-document', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documentId })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete document');
      }

      // Remove the document from the local state
      setDocuments(documents.filter(doc => doc.id !== documentId));
      setSelectedDocuments(selectedDocuments.filter(id => id !== documentId));
      
      // Show success message
      alert('Document deleted successfully');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete document';
      setError(errorMessage);
      alert(errorMessage);
    }
  };

  const handleRegenerateDocument = async (documentId: string, saleId: string, templateId: string) => {
    try {
      setError(null);
      
      const response = await fetch('/api/paperwork/regenerate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          documentId,
          saleId,
          templateId
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to regenerate document');
      }

      // Refresh the documents list
      await fetchData();
      
      // Show success message
      alert('Document regenerated successfully');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to regenerate document';
      setError(errorMessage);
      alert(errorMessage);
    }
  };

  if (showEditor && editingTemplate) {
    return (
      <TemplateEditor
        templateId={editingTemplate.id}
        templateName={editingTemplate.name}
        templateDescription={editingTemplate.description || ''}
        templateType={editingTemplate.templateType}
        currentContent={editingTemplate.htmlContent}
        onSave={handleSaveTemplate}
        onCancel={handleCancelEdit}
      />
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-lg shadow p-8">
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3">Loading paperwork data...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const templateTypes = [
    { value: 'welcome_letter', label: 'Welcome Letter' },
    { value: 'service_agreement', label: 'Service Agreement' },
    { value: 'direct_debit_form', label: 'Direct Debit Form' },
    { value: 'coverage_summary', label: 'Coverage Summary' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Paperwork Management</h1>
          <p className="text-gray-600 mt-2">Manage document templates and generated paperwork</p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
                <button 
                  onClick={() => setError(null)}
                  className="text-red-600 hover:text-red-500 text-sm underline mt-2"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8" aria-label="Tabs">
              <button
                onClick={() => setActiveTab('templates')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'templates'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Document Templates ({templates.length})
              </button>
              <button
                onClick={() => setActiveTab('generate')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'generate'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Generate Documents
              </button>
              <button
                onClick={() => setActiveTab('documents')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'documents'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Generated Documents ({documents.length})
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'templates' ? (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">Document Templates</h2>
                  <div className="flex items-center space-x-4">
                    <select
                      value={newTemplateType}
                      onChange={(e) => setNewTemplateType(e.target.value)}
                      className="border border-gray-300 rounded-md px-3 py-2 text-sm"
                    >
                      <option value="">Select template type...</option>
                      {templateTypes.map(type => (
                        <option key={type.value} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </select>
                    <button 
                      onClick={() => newTemplateType && handleCreateTemplate(newTemplateType)}
                      disabled={!newTemplateType}
                      className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                    >
                      Create New Template
                    </button>
                  </div>
                </div>

                {templates.length === 0 ? (
                  <div className="text-center py-12 bg-gray-50 rounded-lg">
                    <div className="text-gray-400 text-6xl mb-4">📄</div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No Templates Found</h3>
                    <p className="text-gray-500 mb-4">Get started by creating your first document template</p>
                    <div className="flex justify-center space-x-2">
                      {templateTypes.slice(0, 2).map(type => (
                        <button
                          key={type.value}
                          onClick={() => handleCreateTemplate(type.value)}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm"
                        >
                          Create {type.label}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {templates.map((template) => (
                      <div key={template.id} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-4">
                          <div className="flex-1">
                            <h3 className="text-lg font-semibold text-gray-900 mb-1">
                              {template.name}
                            </h3>
                            {template.description && (
                              <p className="text-sm text-gray-600 mb-2">{template.description}</p>
                            )}
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              {template.templateType?.replace('_', ' ') || 'Unknown Type'}
                            </span>
                          </div>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            template.isActive 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            {template.isActive ? 'Active' : 'Inactive'}
                          </span>
                        </div>

                        <div className="text-sm text-gray-500 mb-4">
                          <p>Version: {template.version}</p>
                          <p>Updated: {new Date(template.updatedAt).toLocaleDateString()}</p>
                        </div>

                        <div className="flex flex-wrap gap-2">
                          <button 
                            onClick={() => handleEditTemplate(template)}
                            className="flex-1 bg-blue-50 text-blue-600 px-3 py-2 rounded-md hover:bg-blue-100 text-sm font-medium"
                          >
                            Edit
                          </button>
                          <button 
                            onClick={() => window.open(`/api/paperwork/preview/${template.id}`, '_blank')}
                            className="flex-1 bg-gray-50 text-gray-600 px-3 py-2 rounded-md hover:bg-gray-100 text-sm font-medium"
                          >
                            Preview
                          </button>
                          <button 
                            onClick={() => toggleTemplateStatus(template.id, template.isActive)}
                            className={`flex-1 px-3 py-2 rounded-md text-sm font-medium ${
                              template.isActive 
                                ? 'bg-red-50 text-red-600 hover:bg-red-100' 
                                : 'bg-green-50 text-green-600 hover:bg-green-100'
                            }`}
                          >
                            {template.isActive ? 'Disable' : 'Enable'}
                          </button>
                          {/* Only show delete button for non-system templates */}
                          {!['welcome-letter', 'service-agreement', 'direct-debit-form', 'coverage-summary'].includes(template.id) && (
                            <button 
                              onClick={() => handleDeleteTemplate(template)}
                              className="bg-red-50 text-red-600 px-3 py-2 rounded-md hover:bg-red-100 text-sm font-medium"
                              title="Delete template"
                            >
                              🗑️
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : activeTab === 'generate' ? (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">Generate Documents</h2>
                    <p className="text-gray-600">Select customers and templates to generate paperwork documents.</p>
                  </div>
                  
                  {/* Filters */}
                  <div className="flex items-center space-x-6">
                    <div className="flex items-center space-x-2">
                      <label className="text-sm font-medium text-gray-700">Status:</label>
                      <select
                        value={customerStatusFilter}
                        onChange={(e) => {
                          setCustomerStatusFilter(e.target.value);
                          setSelectedSales([]); // Reset selection when filter changes
                        }}
                        className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                      >
                        <option value="all">All Customers</option>
                        <option value="active">Active</option>
                        <option value="cancelled">Cancelled</option>
                        <option value="cancellation_notice_received">CNR</option>
                        <option value="failed_payment">Failed Payment</option>
                        <option value="process_dd">Process DD</option>
                      </select>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <label className="text-sm font-medium text-gray-700">Documents:</label>
                      <select
                        value={documentsGeneratedFilter}
                        onChange={(e) => {
                          setDocumentsGeneratedFilter(e.target.value as 'all' | 'generated' | 'not-generated');
                          setSelectedSales([]); // Reset selection when filter changes
                        }}
                        className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                      >
                        <option value="all">All Customers</option>
                        <option value="not-generated">No Documents Generated</option>
                        <option value="generated">Documents Generated</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Import BulkOperations here or create inline interface */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Sales Selection */}
                  <div className="bg-gray-50 rounded-lg p-6">
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">Select Customers</h3>
                      <div className="flex items-center space-x-3">
                        <span className="text-sm text-gray-600">
                          {selectedSales.length} of {getFilteredSales().length} selected
                        </span>
                        <button
                          onClick={handleSelectAllSales}
                          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                        >
                          {selectedSales.length === getFilteredSales().length ? 'Deselect All' : 'Select All'}
                        </button>
                      </div>
                    </div>

                    <div className="max-h-96 overflow-y-auto space-y-2">
                      {getFilteredSales().map((sale) => (
                        <label key={sale.id} className="flex items-center p-3 bg-white rounded-lg border hover:shadow-sm cursor-pointer">
                          <input
                            type="checkbox"
                            checked={selectedSales.includes(sale.id)}
                            onChange={() => handleSaleSelection(sale.id)}
                            className="mr-3 h-4 w-4 text-blue-600 rounded"
                          />
                          <div className="flex-1">
                            <div className="font-medium text-gray-900">
                              {sale.customerFirstName} {sale.customerLastName}
                            </div>
                            <div className="text-sm text-gray-500">
                              {sale.email} • Sale #{sale.id.slice(-6)}
                            </div>
                            <div className="flex items-center gap-2 text-sm text-gray-400">
                              <span>{new Date(sale.createdAt).toLocaleDateString()}</span>
                              •
                              <span className={`inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium ${
                                sale.status === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                                sale.status === 'CANCELLED' ? 'bg-red-100 text-red-800' :
                                sale.status === 'CANCELLATION_NOTICE_RECEIVED' ? 'bg-orange-100 text-orange-800' :
                                sale.status === 'FAILED_PAYMENT' ? 'bg-yellow-100 text-yellow-800' :
                                sale.status === 'PROCESS_DD' ? 'bg-blue-100 text-blue-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {sale.status === 'ACTIVE' ? 'Active' :
                                 sale.status === 'CANCELLED' ? 'Cancelled' :
                                 sale.status === 'CANCELLATION_NOTICE_RECEIVED' ? 'CNR' :
                                 sale.status === 'FAILED_PAYMENT' ? 'Failed Payment' :
                                 sale.status === 'PROCESS_DD' ? 'Process DD' :
                                 sale.status}
                              </span>
                              •
                              <span className={`inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium ${
                                sale.documentsGenerated ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-600'
                              }`} title={sale.documentsGenerated ? 
                                `Documents generated ${sale.documentsGeneratedAt ? 'on ' + new Date(sale.documentsGeneratedAt).toLocaleDateString() : ''}` : 
                                'No documents generated yet'}>
                                {sale.documentsGenerated ? '📄 Documents' : '📝 No Docs'}
                              </span>
                            </div>
                          </div>
                          <div className="text-sm font-medium text-green-600">
                            {formatCurrency(sale.totalPlanCost)}/month
                          </div>
                        </label>
                      ))}
                    </div>

                    {getFilteredSales().length === 0 && (
                      <div className="text-center py-8 text-gray-500">
                        <div className="text-4xl mb-2">🏪</div>
                        <p>
                          {documentsGeneratedFilter === 'all' ? 'No sales found' : 
                           documentsGeneratedFilter === 'generated' ? 'No sales with generated documents found' :
                           'No sales without generated documents found'}
                        </p>
                        {documentsGeneratedFilter !== 'all' && (
                          <button 
                            onClick={() => setDocumentsGeneratedFilter('all')}
                            className="mt-2 text-blue-600 hover:text-blue-800 text-sm underline"
                          >
                            Show all sales
                          </button>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Template Selection & Generation */}
                  <div className="bg-gray-50 rounded-lg p-6">
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">Select Templates</h3>
                      <div className="flex items-center space-x-3">
                        <span className="text-sm text-gray-600">
                          {selectedTemplates.length} of {templates.filter(t => t.isActive).length} selected
                        </span>
                        <button
                          onClick={() => {
                            const activeTemplates = templates.filter(t => t.isActive);
                            if (selectedTemplates.length === activeTemplates.length) {
                              setSelectedTemplates([]);
                            } else {
                              setSelectedTemplates(activeTemplates.map(t => t.id));
                            }
                          }}
                          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                        >
                          {selectedTemplates.length === templates.filter(t => t.isActive).length ? 'Deselect All' : 'Select All'}
                        </button>
                      </div>
                    </div>
                    
                    <div className="space-y-3 mb-6">
                      {templates.filter(t => t.isActive).map((template) => (
                        <label key={template.id} className="flex items-center p-4 bg-white rounded-lg border hover:shadow-sm cursor-pointer">
                          <input
                            type="checkbox"
                            checked={selectedTemplates.includes(template.id)}
                            onChange={() => {
                              if (selectedTemplates.includes(template.id)) {
                                setSelectedTemplates(selectedTemplates.filter(id => id !== template.id));
                              } else {
                                setSelectedTemplates([...selectedTemplates, template.id]);
                              }
                            }}
                            className="mr-3 h-4 w-4 text-blue-600 rounded"
                          />
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <div>
                                <h4 className="font-medium text-gray-900">{template.name}</h4>
                                <p className="text-sm text-gray-500">
                                  {template.templateType?.replace(/[-_]/g, ' ') || 'Unknown Type'}
                                </p>
                                {template.description && (
                                  <p className="text-sm text-gray-400 mt-1">{template.description}</p>
                                )}
                              </div>
                              <div className="text-right ml-4">
                                <div className="text-sm text-gray-500">v{template.version}</div>
                                <button
                                  onClick={(e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    window.open(`/api/paperwork/preview/${template.id}`, '_blank');
                                  }}
                                  className="text-blue-600 hover:text-blue-800 text-sm"
                                >
                                  Preview
                                </button>
                              </div>
                            </div>
                          </div>
                        </label>
                      ))}
                    </div>

                    {templates.filter(t => t.isActive).length === 0 && (
                      <div className="text-center py-8 text-gray-500">
                        <div className="text-4xl mb-2">📄</div>
                        <p>No active templates</p>
                      </div>
                    )}

                    {selectedSales.length > 0 && selectedTemplates.length > 0 && (
                      <div className="mt-6 pt-4 border-t">
                        <button
                          onClick={() => handleBulkGenerate(selectedTemplates)}
                          disabled={generating}
                          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
                        >
                          {generating 
                            ? 'Generating Documents...' 
                            : `Generate ${selectedTemplates.length} Template${selectedTemplates.length === 1 ? '' : 's'} for ${selectedSales.length} Customer${selectedSales.length === 1 ? '' : 's'}`
                          }
                        </button>
                        <p className="text-sm text-gray-500 text-center mt-2">
                          This will generate {selectedSales.length} × {selectedTemplates.length} = {selectedSales.length * selectedTemplates.length} documents
                        </p>
                      </div>
                    )}

                    {selectedSales.length > 0 && selectedTemplates.length === 0 && (
                      <div className="mt-6 pt-4 border-t">
                        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                          <div className="flex">
                            <div className="text-yellow-400 text-xl mr-3">⚠️</div>
                            <div>
                              <h4 className="text-yellow-800 font-medium">Select Templates</h4>
                              <p className="text-yellow-700 text-sm">Please select at least one template to generate documents.</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {selectedSales.length === 0 && selectedTemplates.length > 0 && (
                      <div className="mt-6 pt-4 border-t">
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                          <div className="flex">
                            <div className="text-blue-400 text-xl mr-3">ℹ️</div>
                            <div>
                              <h4 className="text-blue-800 font-medium">Select Customers</h4>
                              <p className="text-blue-700 text-sm">Please select at least one customer to generate documents for.</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">Generated Documents</h2>
                  
                  {/* Filter and Bulk Actions */}
                  <div className="flex items-center space-x-4">
                    {/* Customer Status Filter Dropdown */}
                    <select
                      value={customerStatusFilter}
                      onChange={(e) => {
                        setCustomerStatusFilter(e.target.value);
                        setSelectedDocuments([]); // Reset selection when filter changes
                      }}
                      className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    >
                      <option value="all">All Customers</option>
                      <option value="active">Active</option>
                      <option value="cancelled">Cancelled</option>
                      <option value="cancellation_notice_received">CNR</option>
                      <option value="failed_payment">Failed Payment</option>
                      <option value="process_dd">Process DD</option>
                    </select>

                    {/* Document Filter Dropdown */}
                    <select
                      value={documentFilter}
                      onChange={(e) => {
                        setDocumentFilter(e.target.value as 'all' | 'downloaded' | 'undownloaded');
                        setSelectedDocuments([]); // Reset selection when filter changes
                      }}
                      className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    >
                      <option value="all">All Documents</option>
                      <option value="downloaded">Downloaded</option>
                      <option value="undownloaded">Not Downloaded</option>
                    </select>

                    {/* Bulk Download Buttons */}
                    {getFilteredDocuments().length > 0 && (
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleBulkDownload(false)}
                          disabled={selectedDocuments.length === 0 || bulkDownloading}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
                        >
                          {bulkDownloading ? (
                            <>
                              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                              </svg>
                              Creating...
                            </>
                          ) : (
                            <>📦 Download Selected ({selectedDocuments.length})</>
                          )}
                        </button>
                        
                        <button
                          onClick={() => handleBulkDownload(true)}
                          disabled={bulkDownloading}
                          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
                        >
                          📥 Download All {documentFilter !== 'all' ? `(${documentFilter})` : ''}
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {getFilteredDocuments().length === 0 ? (
                  <div className="text-center py-12 bg-gray-50 rounded-lg">
                    <div className="text-gray-400 text-6xl mb-4">📑</div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      {documentFilter === 'all' ? 'No Documents Found' : `No ${documentFilter} Documents`}
                    </h3>
                    <p className="text-gray-500">
                      {documentFilter === 'all' 
                        ? 'Generated documents will appear here' 
                        : `No documents match the ${documentFilter} filter`
                      }
                    </p>
                    <div className="flex space-x-2 justify-center mt-4">
                      <button 
                        onClick={fetchData}
                        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                      >
                        Refresh Documents
                      </button>
                      {documentFilter !== 'all' && (
                        <button 
                          onClick={() => setDocumentFilter('all')}
                          className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
                        >
                          Show All Documents
                        </button>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="min-w-full bg-white border border-gray-200 rounded-lg">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            <input
                              type="checkbox"
                              checked={selectedDocuments.length === getFilteredDocuments().length}
                              onChange={handleSelectAllDocuments}
                              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Customer
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Customer Status
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Template
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            File Name
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Generated
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Actions
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {getFilteredDocuments().map((document) => (
                          <tr key={document.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <input
                                type="checkbox"
                                checked={selectedDocuments.includes(document.id)}
                                onChange={() => handleDocumentSelection(document.id)}
                                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                              />
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm font-medium text-gray-900">
                                {document.sale.customer.fullName}
                              </div>
                              <div className="text-sm text-gray-500">
                                {document.sale.customer.email}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                document.sale.status === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                                document.sale.status === 'CANCELLED' ? 'bg-red-100 text-red-800' :
                                document.sale.status === 'CANCELLATION_NOTICE_RECEIVED' ? 'bg-orange-100 text-orange-800' :
                                document.sale.status === 'FAILED_PAYMENT' ? 'bg-yellow-100 text-yellow-800' :
                                document.sale.status === 'PROCESS_DD' ? 'bg-blue-100 text-blue-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {document.sale.status === 'ACTIVE' ? '✓ Active' :
                                 document.sale.status === 'CANCELLED' ? '✗ Cancelled' :
                                 document.sale.status === 'CANCELLATION_NOTICE_RECEIVED' ? '⚠️ CNR' :
                                 document.sale.status === 'FAILED_PAYMENT' ? '💳 Failed Payment' :
                                 document.sale.status === 'PROCESS_DD' ? '🔄 Process DD' :
                                 document.sale.status}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">{document.templateName}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900 font-mono">{document.fileName}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              {document.downloadCount > 0 ? (
                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                  ✓ Downloaded ({document.downloadCount}×)
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                  ⏳ Not Downloaded
                                </span>
                              )}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {new Date(document.createdAt).toLocaleDateString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                              <div className="flex space-x-3">
                                <a
                                  href={`/api/paperwork/download/${document.id}`}
                                  className="text-blue-600 hover:text-blue-900"
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  title="Download Document"
                                >
                                  📥 Download
                                </a>
                                <button
                                  onClick={() => {
                                    if (confirm('Are you sure you want to regenerate this document? This will overwrite the existing document.')) {
                                      handleRegenerateDocument(document.id, document.saleId, document.templateId);
                                    }
                                  }}
                                  className="text-yellow-600 hover:text-yellow-900"
                                  title="Regenerate Document"
                                >
                                  🔄 Regenerate
                                </button>
                                <a
                                  href={`/admin/sales/${document.saleId}`}
                                  className="text-green-600 hover:text-green-900"
                                  title="View Sale Details"
                                >
                                  👁️ View Sale
                                </a>
                                <button
                                  onClick={() => {
                                    if (confirm(`Are you sure you want to delete the document "${document.fileName}"? This action cannot be undone.`)) {
                                      handleDeleteDocument(document.id);
                                    }
                                  }}
                                  className="text-red-600 hover:text-red-900"
                                  title="Delete Document"
                                >
                                  🗑️ Delete
                                </button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}