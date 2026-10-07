import React, { useState } from 'react';
import { FileText, Trash2, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';
import { UploadZone } from './UploadZone';

export const Sidebar = ({ documents, onRefresh, onDelete, selectedDocIds, onToggleDoc }) => {
  const [showUpload, setShowUpload] = useState(false);

  const getStatusIcon = (status) => {
    switch(status) {
      case 'ready': return <CheckCircle2 className="w-4 h-4 text-emerald-500" />;
      case 'error': return <AlertCircle className="w-4 h-4 text-red-500" />;
      default: return <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />;
    }
  };

  return (
    <aside className="w-72 bg-navy-900 border-r border-navy-700 flex flex-col h-full z-10 shrink-0">
      <div className="p-4 border-b border-navy-700 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Documents</h2>
        <button 
          onClick={() => setShowUpload(!showUpload)}
          className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded transition-colors"
        >
          {showUpload ? 'Cancel' : 'Upload'}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {showUpload && (
          <div className="mb-4">
            <UploadZone onComplete={() => { setShowUpload(false); onRefresh(); }} />
          </div>
        )}

        {documents.length === 0 && !showUpload ? (
          <p className="text-slate-500 text-sm text-center mt-4">No documents uploaded yet.</p>
        ) : (
          documents.map(doc => {
            const isSelected = selectedDocIds.includes(doc.doc_id);
            return (
              <div 
                key={doc.doc_id}
                onClick={() => doc.status === 'ready' && onToggleDoc(doc.doc_id)}
                className={`p-3 rounded-lg border cursor-pointer transition-colors group flex items-start gap-3
                  ${isSelected ? 'bg-navy-800 border-blue-500' : 'bg-navy-800/50 border-navy-700 hover:border-navy-600'}
                  ${doc.status !== 'ready' ? 'opacity-70 cursor-not-allowed' : ''}
                `}
              >
                <div className="mt-0.5">
                  <FileText className={`w-5 h-5 ${isSelected ? 'text-blue-500' : 'text-slate-400'}`} />
                </div>
                
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-200 truncate" title={doc.doc_name}>
                    {doc.doc_name}
                  </p>
                  <div className="flex items-center gap-2 mt-1">
                    {getStatusIcon(doc.status)}
                    <span className="text-xs text-slate-400">
                      {doc.status === 'ready' ? `${doc.total_pages} pages` : doc.status}
                    </span>
                  </div>
                </div>

                <button 
                  onClick={(e) => { e.stopPropagation(); onDelete(doc.doc_id); }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-navy-700 rounded text-slate-400 hover:text-red-400 transition-all"
                  title="Delete document"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            );
          })
        )}
      </div>

      <div className="p-4 border-t border-navy-700 bg-navy-800/30">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>Search mode:</span>
          <span className="font-medium text-blue-400">
            {selectedDocIds.length === 0 ? 'All Documents' : `${selectedDocIds.length} Selected`}
          </span>
        </div>
      </div>
    </aside>
  );
};
