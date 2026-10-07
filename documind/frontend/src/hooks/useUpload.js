import { useState } from 'react';
import { uploadDocument as apiUpload, getUploadStatus } from '../services/api';
import toast from 'react-hot-toast';

export const useUpload = (onComplete) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  
  const uploadFile = async (file) => {
    setIsUploading(true);
    setUploadStatus({ stage: 'uploading', message: 'Uploading file...' });
    
    try {
      const response = await apiUpload(file);
      const docId = response.doc_id;
      
      setUploadStatus({ stage: 'processing', message: 'Extracting content...' });
      
      // Poll status
      const pollInterval = setInterval(async () => {
        try {
          const statusRes = await getUploadStatus(docId);
          
          if (statusRes.status === 'ready') {
            clearInterval(pollInterval);
            setIsUploading(false);
            setUploadStatus(null);
            toast.success(`${file.name} processed successfully!`);
            if (onComplete) onComplete();
          } else if (statusRes.status === 'error') {
            clearInterval(pollInterval);
            setIsUploading(false);
            setUploadStatus(null);
            toast.error(`Failed to process ${file.name}`);
          } else {
            // Still processing
            setUploadStatus({ stage: 'processing', message: 'Analyzing document structure...' });
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 2000);
      
    } catch (err) {
      console.error(err);
      setIsUploading(false);
      setUploadStatus(null);
      toast.error(err.response?.data?.detail || 'Failed to upload document');
    }
  };

  return { uploadFile, isUploading, uploadStatus };
};
