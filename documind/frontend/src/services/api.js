import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const getUploadStatus = async (docId) => {
  const response = await api.get(`/api/upload/status/${docId}`);
  return response.data;
};

export const getDocuments = async () => {
  const response = await api.get('/api/documents');
  return response.data;
};

export const deleteDocument = async (docId) => {
  const response = await api.delete(`/api/documents/${docId}`);
  return response.data;
};

export const askQuestion = async (question, docIds = null) => {
  const response = await api.post('/api/query', {
    question,
    doc_ids: docIds && docIds.length > 0 ? docIds : null,
  });
  return response.data;
};

export const getHealthStatus = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export const getPageImageUrl = (docId, pageNum) => {
  return `http://localhost:8000/api/documents/${docId}/page/${pageNum}/image`;
};

export const getChartImageUrl = (imagePath) => {
  if (!imagePath) return null;
  const filename = imagePath.split(/[\/\\]/).pop();
  return `http://localhost:8000/static/charts/${filename}`;
};
