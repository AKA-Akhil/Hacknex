import React from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import { motion } from 'framer-motion';
import { CitationCard } from './CitationCard';
import { User, Bot } from 'lucide-react';

export const MessageBubble = ({ message, onCitationClick }) => {
  const isUser = message.role === 'user';
  const isError = message.role === 'error';

  // Custom component to render [Source N] as clickable chips
  const renderCitations = (text) => {
    if (!text || !message.citations) return text;
    
    // Replace [Source N] with special tokens
    let processedText = text;
    message.citations.forEach(cit => {
      const regex = new RegExp(`\\[Source ${cit.source_number}\\]`, 'g');
      processedText = processedText.replace(regex, `%%CITATION_${cit.source_number}%%`);
    });

    const parts = processedText.split(/(%%CITATION_\d+%%)/g);
    
    return parts.map((part, index) => {
      const match = part.match(/%%CITATION_(\d+)%%/);
      if (match) {
        const num = parseInt(match[1]);
        const cit = message.citations.find(c => c.source_number === num);
        if (cit) {
          return (
            <button
              key={index}
              onClick={() => onCitationClick(cit)}
              className="inline-flex items-center justify-center w-5 h-5 mx-1 text-[10px] font-bold rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30 hover:bg-blue-500 hover:text-white transition-colors cursor-pointer align-middle"
              title={`View Source ${num}`}
            >
              {num}
            </button>
          );
        }
      }
      return part;
    });
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-4 max-w-4xl ${isUser ? 'ml-auto' : 'mr-auto w-full'}`}
    >
      {!isUser && (
        <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1 ${isError ? 'bg-red-500/20 text-red-400' : 'bg-blue-500 text-white'}`}>
          <Bot className="w-5 h-5" />
        </div>
      )}
      
      <div className={`flex flex-col gap-2 ${isUser ? 'items-end' : 'items-start min-w-0'}`}>
        <div className={`px-5 py-3 rounded-2xl ${
          isUser ? 'bg-blue-600 text-white rounded-tr-sm' : 
          isError ? 'bg-red-500/10 border border-red-500/20 text-red-200 rounded-tl-sm' : 
          'bg-navy-800 border border-navy-700 text-slate-200 rounded-tl-sm prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-navy-900 prose-pre:border prose-pre:border-navy-700'
        }`}>
          {isUser ? (
            <p className="whitespace-pre-wrap m-0">{message.content}</p>
          ) : isError ? (
            <p className="m-0">{message.content}</p>
          ) : (
            <ReactMarkdown 
              rehypePlugins={[rehypeHighlight]}
              components={{
                p: ({node, children}) => {
                  // If children is an array, map over it to render citations
                  const newChildren = React.Children.toArray(children).map(child => {
                    if (typeof child === 'string') {
                      return renderCitations(child);
                    }
                    return child;
                  });
                  return <p className="m-0 mb-4 last:mb-0">{newChildren}</p>;
                },
                li: ({node, children}) => {
                   const newChildren = React.Children.toArray(children).map(child => {
                    if (typeof child === 'string') {
                      return renderCitations(child);
                    }
                    return child;
                  });
                  return <li>{newChildren}</li>;
                }
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {!isUser && !isError && message.citations && message.citations.length > 0 && (
          <div className="w-full mt-2">
            <div className="flex overflow-x-auto pb-2 gap-2 snap-x scrollbar-hide">
              {message.citations.map((citation) => (
                <div key={citation.source_number} className="snap-start shrink-0">
                  <CitationCard 
                    citation={citation} 
                    onClick={() => onCitationClick(citation)} 
                  />
                </div>
              ))}
            </div>
            
            {message.retrievalStats && (
              <div className="text-[11px] text-slate-500 mt-1 flex items-center gap-2">
                <span>Retrieved from {message.retrievalStats.total_chunks_searched} chunks in {message.retrievalStats.retrieval_time_ms}ms</span>
                <span>•</span>
                <span>Sources: {Array.from(new Set(message.citations.map(c => c.content_type))).join(', ')}</span>
              </div>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0 mt-1">
          <User className="w-5 h-5 text-slate-300" />
        </div>
      )}
    </motion.div>
  );
};
