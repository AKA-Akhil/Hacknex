import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File as FileIcon } from 'lucide-react';
import { useUpload } from '../hooks/useUpload';
import { ProcessingStatus } from './ProcessingStatus';

export const UploadZone = ({ onComplete }) => {
  const { uploadFile, isUploading, uploadStatus } = useUpload(onComplete);

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0 && !isUploading) {
      uploadFile(acceptedFiles[0]);
    }
  }, [uploadFile, isUploading]);

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false,
    disabled: isUploading
  });

  return (
    <div className="w-full">
      <div 
        {...getRootProps()} 
        className={`w-full border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center transition-colors cursor-pointer
          ${isDragActive ? 'border-blue-500 bg-blue-500/10' : 'border-navy-700 hover:border-navy-600 bg-navy-800/50 hover:bg-navy-800'}
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        <UploadCloud className={`w-12 h-12 mb-4 ${isDragActive ? 'text-blue-500' : 'text-slate-400'}`} />
        
        {acceptedFiles.length > 0 ? (
          <div className="flex items-center gap-2 text-slate-200 font-medium">
            <FileIcon className="w-5 h-5 text-blue-400" />
            {acceptedFiles[0].name}
          </div>
        ) : (
          <>
            <p className="text-slate-200 font-medium mb-1">
              {isDragActive ? "Drop the PDF here" : "Drag & drop a PDF here"}
            </p>
            <p className="text-slate-400 text-sm">or click to browse</p>
          </>
        )}
      </div>

      {isUploading && uploadStatus && (
        <ProcessingStatus status={uploadStatus} />
      )}
    </div>
  );
};
