import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ZoomIn, ZoomOut } from 'lucide-react';
import { getChartImageUrl } from '../services/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export const SourceViewer = ({ citation, onClose }) => {
  const [scale, setScale] = useState(1);

  if (!citation) return null;

  const pageImageUrl = `http://localhost:8000/static/pages/${citation.doc_id}_page_${citation.page_number}.png`;

  return (
    <AnimatePresence>
      <motion.div 
        initial={{ x: '100%' }}
        animate={{ x: 0 }}
        exit={{ x: '100%' }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className="absolute top-0 right-0 w-[500px] h-full bg-navy-800 border-l border-navy-700 shadow-2xl flex flex-col z-20"
      >
        <div className="p-4 border-b border-navy-700 flex items-center justify-between bg-navy-900/50">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 text-xs font-bold border border-blue-500/30">
                Source {citation.source_number}
              </span>
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">
                {citation.content_type}
              </span>
            </div>
            <h3 className="text-slate-200 font-medium truncate max-w-[350px]" title={citation.doc_name}>
              {citation.doc_name} • Page {citation.page_number}
            </h3>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-navy-700 rounded-lg text-slate-400 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto">
          {citation.content_type === 'chart' && citation.image_path && (
            <div className="p-4 border-b border-navy-700">
              <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Extracted Visual</h4>
              <div className="bg-navy-900 rounded-lg border border-navy-700 p-2 overflow-hidden flex justify-center">
                <img 
                  src={getChartImageUrl(citation.image_path)} 
                  alt="Extracted Chart" 
                  className="max-w-full max-h-[300px] object-contain rounded"
                />
              </div>
            </div>
          )}

          <div className="p-4 border-b border-navy-700">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
              {citation.content_type === 'chart' ? 'Vision Model Description' : 'Extracted Text'}
            </h4>
            <div className="bg-navy-900 rounded-lg border border-navy-700 p-4">
              {citation.content_type === 'table' ? (
                <div className="prose prose-invert prose-sm max-w-none overflow-x-auto">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {citation.chunk_text}
                  </ReactMarkdown>
                </div>
              ) : (
                <p className="text-sm text-slate-300 font-mono whitespace-pre-wrap leading-relaxed">
                  {citation.chunk_text}
                </p>
              )}
            </div>
          </div>

          <div className="p-4 flex flex-col h-full min-h-[400px]">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Page Context</h4>
              <div className="flex gap-1">
                <button onClick={() => setScale(s => Math.max(0.5, s - 0.25))} className="p-1 hover:bg-navy-700 rounded text-slate-400"><ZoomOut className="w-4 h-4"/></button>
                <button onClick={() => setScale(s => Math.min(3, s + 0.25))} className="p-1 hover:bg-navy-700 rounded text-slate-400"><ZoomIn className="w-4 h-4"/></button>
              </div>
            </div>
            
            <div className="flex-1 bg-navy-900 rounded-lg border border-navy-700 overflow-auto relative flex items-start justify-center p-4">
               <div style={{ transform: `scale(${scale})`, transformOrigin: 'top center', transition: 'transform 0.2s' }}>
                 <img
                    src={pageImageUrl}
                    alt={`Page ${citation.page_number}`}
                    className="max-w-full h-auto bg-white"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                 />
                 <div className="hidden flex-col items-center justify-center h-48 text-slate-500 text-sm">
                   <p>Page preview not available</p>
                 </div>
               </div>
            </div>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};
