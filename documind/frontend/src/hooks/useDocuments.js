import { useState, useEffect, useCallback } from 'react';
import { getDocuments, deleteDocument as apiDeleteDocument } from '../services/api';
import toast from 'react-hot-toast';

export const useDocuments = () => {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDocuments = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await getDocuments();
      setDocuments(data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch documents');
      toast.error('Failed to fetch documents');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const deleteDocument = async (docId) => {
    try {
      await apiDeleteDocument(docId);
      setDocuments(docs => docs.filter(d => d.doc_id !== docId));
      toast.success('Document deleted');
    } catch (err) {
      console.error(err);
      toast.error('Failed to delete document');
    }
  };

  return { documents, isLoading, error, fetchDocuments, deleteDocument };
};
