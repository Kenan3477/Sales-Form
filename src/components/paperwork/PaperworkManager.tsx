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
    setGenerating(templateType)
    setError('')
    setSuccess('')

    try {
      const response = await fetch('/api/paperwork/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          saleId,
          templateType,
          templateId,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to generate document')
      }

      const data = await response.json()
      if (data.success) {
        setSuccess(`Document "${templateType}" generated successfully!`)
        await loadDocuments() // Refresh the documents list
        setShowTemplateSelector(false)
      }
    } catch (error) {
      console.error('Error generating document:', error)
      setError(error instanceof Error ? error.message : 'Failed to generate document')
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
                    <div key={template.id} className="relative">
                      <button
                        onClick={() => generateDocument(template.templateType, template.id)}
                        disabled={generating !== null}
                        className="w-full text-left p-3 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                      >
                        <div className="flex items-center">
                          <span className="text-2xl mr-3">
                            {getTemplateIcon(template.templateType)}
                          </span>
                          <div className="flex-1">
                            <div className="text-sm font-medium text-gray-900">
                              {template.name}
                            </div>
                            <div className="text-sm text-gray-500">
                              {template.description}
                            </div>
                          </div>
                        </div>
                      </button>
                      {generating === template.templateType && (
                        <div className="absolute inset-0 bg-gray-50 bg-opacity-75 flex items-center justify-center rounded-md">
                          <div className="text-sm text-gray-600">Generating...</div>
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
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
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
                        onClick={() => deleteDocument(doc.id)}
                        className="inline-flex items-center px-3 py-1.5 border border-red-300 text-xs font-medium rounded text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
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
      </div>
    </div>
  )
}