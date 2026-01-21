'use client'

import { useState, useEffect } from 'react'
import { Download, FileText, Eye, Trash2, Plus, AlertCircle, CheckCircle } from 'lucide-react'

interface GeneratedDocument {
  id: string
  saleId: string
  templateId: string
  filename: string
  filePath: string
  fileSize: number
  downloadUrl: string
  metadata: any
  generatedAt?: string
  downloadCount?: number
}

interface DocumentTemplate {
  id: string
  name: string
  description?: string
  templateType: string
  isActive: boolean
  version: number
  createdAt: string
}

interface PaperworkManagerProps {
  saleId: string
}

export default function PaperworkManager({ saleId }: PaperworkManagerProps) {
  const [documents, setDocuments] = useState<GeneratedDocument[]>([])
  const [templates, setTemplates] = useState<DocumentTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState<string | null>(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [showTemplateSelector, setShowTemplateSelector] = useState(false)
  const [selectedDocuments, setSelectedDocuments] = useState<Set<string>>(new Set())
  const [isDeleting, setIsDeleting] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [deleteMode, setDeleteMode] = useState<'selected'>('selected')

  // Document selection functions
  const toggleDocumentSelection = (documentId: string) => {
    const newSelection = new Set(selectedDocuments)
    if (newSelection.has(documentId)) {
      newSelection.delete(documentId)
    } else {
      newSelection.add(documentId)
    }
    setSelectedDocuments(newSelection)
  }

  const selectAllDocuments = () => {
    setSelectedDocuments(new Set(documents.map(doc => doc.id)))
  }

  const clearSelection = () => {
    setSelectedDocuments(new Set())
  }

  // Document deletion functions
  const deleteSelectedDocuments = async () => {
    if (selectedDocuments.size === 0) return

    setIsDeleting(true)
    setError('')

    const deleteWithRetry = async (documentId: string, retries = 3): Promise<boolean> => {
      for (let attempt = 1; attempt <= retries; attempt++) {
        try {
          // Minimal delay before retries since rate limiting is bypassed for admins
          if (attempt > 1) {
            const delay = 1000 * attempt; // 1s, 2s, 3s
            console.log(`Waiting ${delay/1000}s before retry ${attempt}/${retries} for ${documentId}`);
            await new Promise(resolve => setTimeout(resolve, delay));
          }

          const response = await fetch('/api/paperwork/delete-document', {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ documentId })
          })

          if (response.ok) {
            return true;
          } else if (response.status === 429) {
            // This shouldn't happen for admins anymore, but handle just in case
            console.log(`Unexpected rate limit for admin ${documentId}, attempt ${attempt}/${retries}`);
            if (attempt < retries) {
              await new Promise(resolve => setTimeout(resolve, 2000 * attempt));
              continue;
            }
          } else {
            console.error(`HTTP error ${response.status} for ${documentId}`);
            return false;
          }
          return false;
        } catch (err) {
          console.error(`Error deleting document ${documentId}, attempt ${attempt}:`, err);
          if (attempt < retries) {
            await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
            continue;
          }
          return false;
        }
      }
      return false;
    };

    try {
      let successCount = 0;
      let errorCount = 0;
      const selectedArray = Array.from(selectedDocuments);
      const successfullyDeleted: string[] = [];

      // Delete documents one by one with longer delays
      for (let i = 0; i < selectedArray.length; i++) {
        const documentId = selectedArray[i];
        
        const success = await deleteWithRetry(documentId);
        
        if (success) {
          successCount++;
          successfullyDeleted.push(documentId);
        } else {
          errorCount++;
        }

        // Shorter delay between deletions for individual sales page (0.5 seconds)
        if (i < selectedArray.length - 1) {
          console.log(`Waiting 0.5s before next deletion...`);
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      }

      // Update documents state by removing successfully deleted ones
      setDocuments(prev => prev.filter(doc => !successfullyDeleted.includes(doc.id)))
      setSelectedDocuments(new Set())
      
      if (errorCount === 0) {
        setSuccess(`Successfully deleted all ${successCount} document(s)`)
      } else {
        setSuccess(`Deleted ${successCount} document(s). ${errorCount} failed due to rate limiting.`)
      }
      
    } catch (error) {
      console.error('Error deleting documents:', error)
      setError(error instanceof Error ? error.message : 'Failed to delete documents')
    } finally {
      setIsDeleting(false)
      setShowDeleteConfirm(false)
    }
  }

  const handleDeleteConfirm = () => {
    deleteSelectedDocuments()
  }

  const initiateDelete = (mode: 'selected') => {
    setDeleteMode(mode)
    setShowDeleteConfirm(true)
  }

  useEffect(() => {
    loadDocuments()
    loadTemplates()
  }, [saleId])

  const loadDocuments = async () => {
    try {
      const response = await fetch(`/api/paperwork/documents/${saleId}`)
      if (!response.ok) {
        throw new Error('Failed to load documents')
      }
      const data = await response.json()
      if (data.success) {
        setDocuments(data.documents)
      }
    } catch (error) {
      console.error('Error loading documents:', error)
      setError('Failed to load documents')
    } finally {
      setLoading(false)
    }
  }

  const loadTemplates = async () => {
    try {
      const response = await fetch('/api/paperwork/templates?activeOnly=true')
      if (!response.ok) {
        throw new Error('Failed to load templates')
      }
      const data = await response.json()
      if (data.success) {
        setTemplates(data.templates)
      }
    } catch (error) {
      console.error('Error loading templates:', error)
    }
  }

  const generateDocument = async (templateType: string, templateId?: string) => {
    console.log('🔄 Starting document generation:', { templateType, templateId, saleId });
    
    setGenerating(templateType)
    setError('')
    setSuccess('')

    try {
      const requestData = {
        saleId,
        templateType,
        templateId,
      };
      
      console.log('📝 Sending request:', requestData);
      
      const response = await fetch('/api/paperwork/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })

      console.log('📝 Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json()
        console.error('❌ Response error:', errorData);
        throw new Error(errorData.error || 'Failed to generate document')
      }

      const data = await response.json()
      console.log('✅ Success response:', data);
      
      if (data.success) {
        setSuccess(`Document "${templateType}" generated successfully!`)
        await loadDocuments() // Refresh the documents list
        setShowTemplateSelector(false)
      } else {
        console.error('❌ Response indicates failure:', data);
        throw new Error(data.error || 'Generation failed')
      }
    } catch (error) {
      console.error('❌ Error generating document:', error)
      setError(error instanceof Error ? error.message : 'Failed to generate document')
    } finally {
      setGenerating(null)
    }
  }

  const generateDirectPDF = async (templateType: string, templateId?: string) => {
    console.log('🎯 Starting DIRECT PDF generation for:', templateType);
    setGenerating(`${templateType}-pdf`)
    setError('')
    setSuccess('')

    try {
      const requestData = {
        saleId,
        templateType,
        ...(templateId && { templateId }),
      };

      console.log('🎯 PDF Request data:', requestData);

      const response = await fetch('/api/paperwork/generate-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })

      console.log('🎯 PDF Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json()
        console.error('❌ PDF Response error:', errorData);
        throw new Error(errorData.error || 'Failed to generate PDF')
      }

      // Handle PDF download
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${templateType}-${saleId}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      setSuccess(`PDF "${templateType}" downloaded successfully!`)
      setShowTemplateSelector(false)
    } catch (error) {
      console.error('❌ Error generating PDF:', error)
      setError(error instanceof Error ? error.message : 'Failed to generate PDF')
    } finally {
      setGenerating(null)
    }
  }

  const previewDocument = async (templateType: string, format: 'html' | 'pdf' = 'html') => {
    try {
      const response = await fetch('/api/paperwork/preview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          saleId,
          templateType,
          format,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate preview')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      
      if (format === 'html') {
        // Open in new window for HTML
        window.open(url, '_blank')
      } else {
        // Download or open PDF
        const link = document.createElement('a')
        link.href = url
        link.target = '_blank'
        link.click()
      }
      
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error previewing document:', error)
      setError(error instanceof Error ? error.message : 'Failed to preview document')
    }
  }

  const downloadDocument = async (documentId: string, filename: string) => {
    try {
      const response = await fetch(`/api/paperwork/download/${documentId}`)
      if (!response.ok) {
        throw new Error('Failed to download document')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      link.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error downloading document:', error)
      setError(error instanceof Error ? error.message : 'Failed to download document')
    }
  }

  const deleteDocument = async (documentId: string) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return
    }

    try {
      const response = await fetch(`/api/paperwork/documents/${saleId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documentId }),
      })

      if (!response.ok) {
        throw new Error('Failed to delete document')
      }

      setSuccess('Document deleted successfully')
      await loadDocuments()
    } catch (error) {
      console.error('Error deleting document:', error)
      setError(error instanceof Error ? error.message : 'Failed to delete document')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const getTemplateIcon = (templateType: string) => {
    switch (templateType) {
      case 'welcome_letter':
        return '📄'
      case 'service_agreement':
        return '📋'
      case 'direct_debit_form':
        return '🏦'
      case 'coverage_summary':
        return '📊'
      default:
        return '📄'
    }
  }

  if (loading) {
    return (
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h2 className="text-lg leading-6 font-medium text-gray-900">Documents & Paperwork</h2>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Generate and manage customer documents
          </p>
        </div>
        <div className="border-t border-gray-200 p-6">
          <div className="text-center text-gray-500">Loading...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white shadow sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg leading-6 font-medium text-gray-900">Documents & Paperwork</h2>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Generate and manage customer documents
            </p>
          </div>
          <button
            onClick={() => setShowTemplateSelector(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <Plus className="w-4 h-4 mr-2" />
            Generate Document
          </button>
        </div>
      </div>

      <div className="border-t border-gray-200">
        {/* Alerts */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <div className="flex">
              <AlertCircle className="h-5 w-5 text-red-400" />
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {success && (
          <div className="bg-green-50 border-l-4 border-green-400 p-4">
            <div className="flex">
              <CheckCircle className="h-5 w-5 text-green-400" />
              <div className="ml-3">
                <p className="text-sm text-green-700">{success}</p>
              </div>
            </div>
          </div>
        )}

        {/* Template Selector Modal */}
        {showTemplateSelector && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 text-center">
                  Select Document Template
                </h3>
                <div className="mt-4 space-y-3">
                  {templates.map((template) => (
                    <div key={template.id} className="relative border border-gray-300 rounded-lg overflow-hidden">
                      {/* Generate Direct PDF - FEATURED */}
                      <button
                        onClick={() => generateDirectPDF(template.templateType, template.id)}
                        disabled={generating !== null}
                        className="w-full text-left p-4 hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 bg-gradient-to-r from-blue-50 to-blue-100 border-b-2 border-blue-200"
                      >
                        <div className="flex items-center">
                          <span className="text-3xl mr-3">📄</span>
                          <div className="flex-1">
                            <div className="text-sm font-bold text-blue-900">
                              📥 Generate & Download PDF
                            </div>
                            <div className="text-xs text-blue-700 font-medium">
                              Professional PDF with Flash Team branding - Ready to print
                            </div>
                          </div>
                          <div className="bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-bold">
                            RECOMMENDED
                          </div>
                        </div>
                      </button>
                      
                      {/* Generate HTML Document - Secondary option */}
                      <button
                        onClick={() => generateDocument(template.templateType, template.id)}
                        disabled={generating !== null}
                        className="w-full text-left p-3 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-400 disabled:opacity-50 bg-gray-50"
                      >
                        <div className="flex items-center">
                          <span className="text-2xl mr-3 opacity-60">
                            {getTemplateIcon(template.templateType)}
                          </span>
                          <div className="flex-1">
                            <div className="text-sm font-medium text-gray-700">
                              Generate HTML Document
                            </div>
                            <div className="text-xs text-gray-500">
                              For system storage only - {template.description}
                            </div>
                          </div>
                          <div className="text-xs text-gray-600 font-medium">
                            HTML
                          </div>
                        </div>
                      </button>
                      
                      {/* Loading overlay */}
                      {(generating === template.templateType || generating === `${template.templateType}-pdf`) && (
                        <div className="absolute inset-0 bg-gray-50 bg-opacity-90 flex items-center justify-center rounded-lg">
                          <div className="text-center">
                            <div className="animate-spin text-2xl mb-2">⚙️</div>
                            <div className="text-sm font-medium text-gray-700">
                              {generating?.includes('-pdf') ? 'Generating Professional PDF...' : 'Generating HTML...'}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}

                  <div className="mt-6 space-y-2">
                    <h4 className="text-sm font-medium text-gray-900">Quick Preview</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {templates.slice(0, 2).map((template) => (
                        <button
                          key={`preview-${template.id}`}
                          onClick={() => previewDocument(template.templateType, 'html')}
                          className="px-3 py-2 text-xs border border-gray-300 rounded text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <Eye className="w-3 h-3 inline mr-1" />
                          Preview {template.name.split(' ')[0]}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="items-center px-4 py-3 mt-4 border-t">
                  <button
                    onClick={() => setShowTemplateSelector(false)}
                    className="w-full px-4 py-2 bg-gray-300 text-gray-800 text-base font-medium rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Documents List */}
        <div className="px-4 py-5 sm:p-6">
          {documents.length === 0 ? (
            <div className="text-center py-6">
              <FileText className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No documents yet</h3>
              <p className="mt-1 text-sm text-gray-500">
                Generate your first document by clicking the button above.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Bulk Actions Toolbar */}
              <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3 border border-gray-200">
                <div className="flex items-center space-x-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={selectedDocuments.size === documents.length}
                      onChange={selectedDocuments.size === documents.length ? clearSelection : selectAllDocuments}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span className="ml-2 text-sm text-gray-700">
                      {selectedDocuments.size === 0 
                        ? 'Select all' 
                        : `${selectedDocuments.size} selected`
                      }
                    </span>
                  </label>
                </div>
                <div className="flex items-center space-x-2">
                  {selectedDocuments.size > 0 && (
                    <button
                      onClick={() => initiateDelete('selected')}
                      disabled={isDeleting}
                      className="inline-flex items-center px-3 py-1.5 border border-red-300 text-xs font-medium rounded text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Trash2 className="w-3 h-3 mr-1" />
                      Delete Selected ({selectedDocuments.size})
                    </button>
                  )}
                </div>
              </div>

              {/* Documents Grid */}
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className={`border rounded-lg p-4 hover:bg-gray-50 transition-colors ${
                    selectedDocuments.has(doc.id) 
                      ? 'border-blue-300 bg-blue-50' 
                      : 'border-gray-200'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        checked={selectedDocuments.has(doc.id)}
                        onChange={() => toggleDocumentSelection(doc.id)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="text-2xl">
                        {getTemplateIcon(doc.metadata?.templateType || 'unknown')}
                      </span>
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">
                          {doc.filename}
                        </h4>
                        <p className="text-sm text-gray-500">
                          {formatFileSize(doc.fileSize)} • 
                          {doc.generatedAt && (
                            <> Generated {new Date(doc.generatedAt).toLocaleDateString()}</>
                          )}
                          {doc.downloadCount !== undefined && (
                            <> • Downloaded {doc.downloadCount} times</>
                          )}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => downloadDocument(doc.id, doc.filename)}
                        className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <Download className="w-3 h-3 mr-1" />
                        Download
                      </button>
                      <button
                        onClick={() => {
                          setSelectedDocuments(new Set([doc.id]))
                          initiateDelete('selected')
                        }}
                        disabled={isDeleting}
                        className="inline-flex items-center px-3 py-1.5 border border-red-300 text-xs font-medium rounded text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <Trash2 className="w-3 h-3 mr-1" />
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Delete Confirmation Modal */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
            <div className="relative p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3 text-center">
                <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                  <Trash2 className="h-6 w-6 text-red-600" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mt-4">
                  Delete Selected Documents
                </h3>
                <div className="mt-2 px-7 py-3">
                  <p className="text-sm text-gray-500">
                    Are you sure you want to delete {selectedDocuments.size} selected document(s)? This action cannot be undone.
                  </p>
                </div>
                <div className="items-center px-4 py-3">
                  <div className="flex space-x-3">
                    <button
                      onClick={handleDeleteConfirm}
                      disabled={isDeleting}
                      className="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                      {isDeleting ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Deleting...
                        </>
                      ) : (
                        'Delete'
                      )}
                    </button>
                    <button
                      onClick={() => setShowDeleteConfirm(false)}
                      disabled={isDeleting}
                      className="px-4 py-2 bg-gray-300 text-gray-800 text-base font-medium rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}