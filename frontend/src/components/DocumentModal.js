import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { busesAPI } from '../services/api';
import { X, Upload, FileText, AlertTriangle, CheckCircle, Eye, Scan } from 'lucide-react';
import toast from 'react-hot-toast';

const DocumentModal = ({ bus, onClose }) => {
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [uploadData, setUploadData] = useState({
    document_type: 'Insurance',
    document_name: '',
    document_number: '',
    issue_date: '',
    expiry_date: '',
    issuing_authority: '',
  });
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [ocrProcessing, setOcrProcessing] = useState(false);

  const queryClient = useQueryClient();

  // Fetch bus documents
  const { data: documentsData, isLoading } = useQuery(
    ['bus-documents', bus.id],
    () => busesAPI.getDocuments(bus.id)
  );

  // Upload document mutation
  const uploadDocumentMutation = useMutation(
    (formData) => busesAPI.uploadDocument(bus.id, formData),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['bus-documents', bus.id]);
        toast.success('Document uploaded successfully');
        setShowUploadForm(false);
        resetUploadForm();
      },
      onError: (error) => {
        toast.error(error.response?.data?.error || 'Failed to upload document');
      },
    }
  );

  const resetUploadForm = () => {
    setUploadData({
      document_type: 'Insurance',
      document_name: '',
      document_number: '',
      issue_date: '',
      expiry_date: '',
      issuing_authority: '',
    });
    setSelectedFile(null);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'image/tiff'];
      if (!allowedTypes.includes(file.type)) {
        toast.error('Invalid file type. Please upload PDF, JPG, PNG, or TIFF files.');
        return;
      }

      // Validate file size (max 16MB)
      if (file.size > 16 * 1024 * 1024) {
        toast.error('File size too large. Maximum size is 16MB.');
        return;
      }

      setSelectedFile(file);
      
      // Auto-fill document name if empty
      if (!uploadData.document_name) {
        setUploadData(prev => ({
          ...prev,
          document_name: file.name.split('.')[0]
        }));
      }

      // Simulate OCR processing
      performOCR(file);
    }
  };

  const performOCR = async (file) => {
    setOcrProcessing(true);
    
    // Simulate OCR processing delay
    setTimeout(() => {
      // Mock OCR results based on document type
      const ocrResults = {
        Insurance: {
          document_number: 'INS123456789',
          issue_date: '2023-01-01',
          expiry_date: '2024-01-01',
          issuing_authority: 'National Insurance Company',
        },
        RC: {
          document_number: 'RC' + bus.registration_number.replace(/\s/g, ''),
          issue_date: '2020-01-01',
          expiry_date: '2025-01-01',
          issuing_authority: 'Regional Transport Office',
        },
        'Fitness Certificate': {
          document_number: 'FC' + Date.now().toString().slice(-6),
          issue_date: '2023-01-01',
          expiry_date: '2024-01-01',
          issuing_authority: 'Motor Vehicle Inspector',
        },
      };

      const result = ocrResults[uploadData.document_type] || {};
      
      setUploadData(prev => ({
        ...prev,
        ...result
      }));

      setOcrProcessing(false);
      toast.success('Document scanned successfully! Details auto-filled.');
    }, 2000);
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      toast.error('Please select a file to upload');
      return;
    }

    setIsUploading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('document_type', uploadData.document_type);
    formData.append('document_name', uploadData.document_name);
    formData.append('document_number', uploadData.document_number);
    formData.append('issue_date', uploadData.issue_date);
    formData.append('expiry_date', uploadData.expiry_date);
    formData.append('issuing_authority', uploadData.issuing_authority);

    try {
      await uploadDocumentMutation.mutateAsync(formData);
    } finally {
      setIsUploading(false);
    }
  };

  const getDocumentStatusIcon = (document) => {
    if (document.is_expired) {
      return <AlertTriangle className="h-5 w-5 text-red-500" />;
    }
    if (document.is_expiring_soon) {
      return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
    }
    return <CheckCircle className="h-5 w-5 text-green-500" />;
  };

  const getDocumentStatusText = (document) => {
    if (document.is_expired) {
      return 'Expired';
    }
    if (document.is_expiring_soon) {
      return `Expires in ${document.days_to_expiry} days`;
    }
    return 'Valid';
  };

  const documents = documentsData?.data?.data?.documents || [];

  return (
    <div className="modal-overlay">
      <div className="modal-content max-w-4xl">
        <div className="modal-header">
          <h3 className="text-lg font-medium text-gray-900">
            Documents - {bus.bus_number}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-500"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="modal-body">
          {!showUploadForm ? (
            <>
              {/* Documents List */}
              <div className="flex justify-between items-center mb-6">
                <h4 className="text-md font-medium text-gray-900">Uploaded Documents</h4>
                <button
                  onClick={() => setShowUploadForm(true)}
                  className="btn btn-primary flex items-center space-x-2"
                >
                  <Upload className="h-4 w-4" />
                  <span>Upload Document</span>
                </button>
              </div>

              {isLoading ? (
                <div className="text-center py-8">
                  <div className="loading-spinner h-8 w-8 mx-auto"></div>
                  <p className="mt-2 text-gray-600">Loading documents...</p>
                </div>
              ) : documents.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No documents uploaded yet</p>
                  <button
                    onClick={() => setShowUploadForm(true)}
                    className="btn btn-primary mt-4"
                  >
                    Upload First Document
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {documents.map((document) => (
                    <div key={document.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <FileText className="h-8 w-8 text-blue-500" />
                          <div>
                            <h5 className="font-medium text-gray-900">
                              {document.document_name}
                            </h5>
                            <p className="text-sm text-gray-600">
                              {document.document_type} • {document.file_size_mb} MB
                            </p>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center space-x-2">
                            {getDocumentStatusIcon(document)}
                            <span className={`text-sm ${
                              document.is_expired ? 'text-red-600' :
                              document.is_expiring_soon ? 'text-yellow-600' : 'text-green-600'
                            }`}>
                              {getDocumentStatusText(document)}
                            </span>
                          </div>
                          
                          <button className="text-blue-600 hover:text-blue-900">
                            <Eye className="h-4 w-4" />
                          </button>
                        </div>
                      </div>

                      {/* Document Details */}
                      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Document Number:</span>
                          <p className="font-medium">{document.document_number || 'N/A'}</p>
                        </div>
                        <div>
                          <span className="text-gray-600">Issue Date:</span>
                          <p className="font-medium">{document.issue_date || 'N/A'}</p>
                        </div>
                        <div>
                          <span className="text-gray-600">Expiry Date:</span>
                          <p className="font-medium">{document.expiry_date || 'N/A'}</p>
                        </div>
                        <div>
                          <span className="text-gray-600">Issuing Authority:</span>
                          <p className="font-medium">{document.issuing_authority || 'N/A'}</p>
                        </div>
                      </div>

                      {/* OCR Data */}
                      {document.ocr_data && (
                        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center space-x-2 mb-2">
                            <Scan className="h-4 w-4 text-blue-500" />
                            <span className="text-sm font-medium text-gray-900">
                              OCR Extracted Data
                            </span>
                            {document.ocr_confidence && (
                              <span className="text-xs text-gray-600">
                                ({Math.round(document.ocr_confidence * 100)}% confidence)
                              </span>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 line-clamp-3">
                            {document.ocr_data.text}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : (
            /* Upload Form */
            <form onSubmit={handleUploadSubmit} className="space-y-6">
              <div className="flex justify-between items-center">
                <h4 className="text-md font-medium text-gray-900">Upload New Document</h4>
                <button
                  type="button"
                  onClick={() => setShowUploadForm(false)}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="form-label">Document Type *</label>
                  <select
                    value={uploadData.document_type}
                    onChange={(e) => setUploadData(prev => ({ ...prev, document_type: e.target.value }))}
                    className="input"
                    required
                  >
                    <option value="Insurance">Insurance</option>
                    <option value="RC">RC (Registration Certificate)</option>
                    <option value="Fitness Certificate">Fitness Certificate</option>
                    <option value="Permit">Permit</option>
                    <option value="Pollution Certificate">Pollution Certificate</option>
                    <option value="Tax Receipt">Tax Receipt</option>
                    <option value="Service Record">Service Record</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="form-label">Document Name *</label>
                  <input
                    type="text"
                    value={uploadData.document_name}
                    onChange={(e) => setUploadData(prev => ({ ...prev, document_name: e.target.value }))}
                    className="input"
                    required
                    placeholder="Enter document name"
                  />
                </div>

                <div>
                  <label className="form-label">Document Number</label>
                  <input
                    type="text"
                    value={uploadData.document_number}
                    onChange={(e) => setUploadData(prev => ({ ...prev, document_number: e.target.value }))}
                    className="input"
                    placeholder="Will be auto-filled by OCR"
                  />
                </div>

                <div>
                  <label className="form-label">Issuing Authority</label>
                  <input
                    type="text"
                    value={uploadData.issuing_authority}
                    onChange={(e) => setUploadData(prev => ({ ...prev, issuing_authority: e.target.value }))}
                    className="input"
                    placeholder="Will be auto-filled by OCR"
                  />
                </div>

                <div>
                  <label className="form-label">Issue Date</label>
                  <input
                    type="date"
                    value={uploadData.issue_date}
                    onChange={(e) => setUploadData(prev => ({ ...prev, issue_date: e.target.value }))}
                    className="input"
                  />
                </div>

                <div>
                  <label className="form-label">Expiry Date</label>
                  <input
                    type="date"
                    value={uploadData.expiry_date}
                    onChange={(e) => setUploadData(prev => ({ ...prev, expiry_date: e.target.value }))}
                    className="input"
                  />
                </div>
              </div>

              {/* File Upload */}
              <div>
                <label className="form-label">Upload File *</label>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div className="space-y-1 text-center">
                    <Upload className="mx-auto h-12 w-12 text-gray-400" />
                    <div className="flex text-sm text-gray-600">
                      <label className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                        <span>Upload a file</span>
                        <input
                          type="file"
                          className="sr-only"
                          accept=".pdf,.jpg,.jpeg,.png,.tiff"
                          onChange={handleFileSelect}
                          required
                        />
                      </label>
                      <p className="pl-1">or drag and drop</p>
                    </div>
                    <p className="text-xs text-gray-500">
                      PDF, JPG, PNG, TIFF up to 16MB
                    </p>
                  </div>
                </div>
                
                {selectedFile && (
                  <div className="mt-2 flex items-center space-x-2">
                    <FileText className="h-4 w-4 text-blue-500" />
                    <span className="text-sm text-gray-900">{selectedFile.name}</span>
                    <span className="text-xs text-gray-500">
                      ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                    </span>
                  </div>
                )}
              </div>

              {/* OCR Processing Indicator */}
              {ocrProcessing && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center space-x-2">
                    <div className="loading-spinner h-4 w-4"></div>
                    <span className="text-sm text-blue-900">
                      Processing document with AI OCR...
                    </span>
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowUploadForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isUploading || ocrProcessing}
                  className="btn btn-primary"
                >
                  {isUploading ? 'Uploading...' : 'Upload Document'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentModal;
