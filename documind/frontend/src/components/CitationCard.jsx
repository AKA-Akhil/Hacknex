import React from 'react';
import { FileText, Table, BarChart2 } from 'lucide-react';

export const CitationCard = ({ citation, onClick }) => {
  const getIcon = () => {
    switch(citation.content_type) {
      case 'text': return <FileText className="w-3.5 h-3.5 text-blue-400" />;
      case 'table': return <Table className="w-3.5 h-3.5 text-emerald-400" />;
      case 'chart': return <BarChart2 className="w-3.5 h-3.5 text-purple-400" />;
      default: return <FileText className="w-3.5 h-3.5" />;
    }
  };

  return (
    <button 
      onClick={onClick}
      className="flex items-center gap-3 p-2 pr-4 bg-navy-800 border border-navy-700 rounded-lg hover:border-navy-500 hover:bg-navy-700/50 transition-all text-left w-48 group relative"
    >
      <div className="w-6 h-6 rounded-full bg-navy-900 flex items-center justify-center text-xs font-bold text-slate-300 shrink-0 border border-navy-700">
        {citation.source_number}
      </div>
      
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-1.5 mb-0.5">
          {getIcon()}
          <span className="text-xs text-slate-400 capitalize">{citation.content_type}</span>
        </div>
        <p className="text-xs font-medium text-slate-200 truncate" title={citation.doc_name}>
          {citation.doc_name}
        </p>
        <p className="text-[10px] text-slate-500">Page {citation.page_number}</p>
      </div>

      {/* Tooltip on hover */}
      <div className="absolute bottom-full left-0 mb-2 w-64 bg-navy-900 border border-navy-700 p-3 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-20 pointer-events-none">
        <p className="text-xs text-slate-300 line-clamp-4 whitespace-pre-wrap font-mono">
          {citation.chunk_text}
        </p>
      </div>
    </button>
  );
};
