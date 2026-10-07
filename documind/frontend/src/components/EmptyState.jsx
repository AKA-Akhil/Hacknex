import React from 'react';
import { FileSearch, Layers, AlignLeft, Search } from 'lucide-react';
import { UploadZone } from './UploadZone';

export const EmptyState = ({ onUploadComplete }) => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 overflow-y-auto">
      <div className="max-w-2xl w-full flex flex-col items-center text-center space-y-6">
        <div className="w-20 h-20 bg-navy-800 rounded-full flex items-center justify-center border border-navy-700 mb-2">
          <FileSearch className="w-10 h-10 text-blue-500" />
        </div>
        
        <h2 className="text-3xl font-bold text-slate-100">Upload a document to get started</h2>
        <p className="text-slate-400 text-lg max-w-lg pb-4">
          DocuMind analyzes text, tables, and charts to answer your questions with precise citations.
        </p>

        <div className="w-full max-w-md pb-8">
          <UploadZone onComplete={onUploadComplete} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-4">
          <div className="bg-navy-800 p-5 rounded-xl border border-navy-700 flex flex-col items-center text-center">
            <Layers className="w-6 h-6 text-blue-400 mb-3" />
            <h3 className="text-slate-200 font-semibold mb-1">Multi-format Analysis</h3>
            <p className="text-slate-400 text-sm">Understands text, tables, and visual charts natively.</p>
          </div>
          
          <div className="bg-navy-800 p-5 rounded-xl border border-navy-700 flex flex-col items-center text-center">
            <AlignLeft className="w-6 h-6 text-emerald-400 mb-3" />
            <h3 className="text-slate-200 font-semibold mb-1">Cited Answers</h3>
            <p className="text-slate-400 text-sm">Every claim is traced back to the exact source page.</p>
          </div>
          
          <div className="bg-navy-800 p-5 rounded-xl border border-navy-700 flex flex-col items-center text-center">
            <Search className="w-6 h-6 text-purple-400 mb-3" />
            <h3 className="text-slate-200 font-semibold mb-1">Cross-Document Search</h3>
            <p className="text-slate-400 text-sm">Query and compare information across multiple PDFs.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
