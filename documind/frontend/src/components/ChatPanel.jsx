import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { EmptyState } from './EmptyState';
import { useChat } from '../hooks/useChat';

export const ChatPanel = ({ documents, selectedDocIds, onCitationClick }) => {
  const [input, setInput] = useState('');
  const { messages, sendMessage, isLoading } = useChat();
  const messagesEndRef = useRef(null);

  const hasDocuments = documents && documents.length > 0;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    sendMessage(input, selectedDocIds);
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (!hasDocuments) {
    return <EmptyState onUploadComplete={() => {}} />;
  }

  return (
    <div className="flex-1 flex flex-col h-full relative">
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-lg mx-auto">
            <h3 className="text-2xl font-semibold text-slate-200 mb-2">How can I help you?</h3>
            <p className="text-slate-400">
              Ask questions about your uploaded documents. I'll search through text, tables, and charts to find the answer.
            </p>
          </div>
        ) : (
          messages.map(msg => (
            <MessageBubble 
              key={msg.id} 
              message={msg} 
              onCitationClick={onCitationClick}
            />
          ))
        )}
        
        {isLoading && (
          <div className="flex items-center gap-3 text-slate-400 p-4 rounded-xl bg-navy-800/50 mr-auto max-w-[80%]">
            <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
            <span className="animate-pulse">DocuMind is analyzing...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-navy-900 border-t border-navy-700">
        <form 
          onSubmit={handleSubmit}
          className="max-w-4xl mx-auto relative flex items-end bg-navy-800 rounded-xl border border-navy-700 focus-within:border-blue-500 transition-colors"
        >
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your documents..."
            className="w-full max-h-48 min-h-[56px] py-4 pl-4 pr-12 bg-transparent text-slate-100 placeholder-slate-500 resize-none outline-none overflow-y-auto"
            rows="1"
            style={{ height: '56px' }}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 bottom-2 p-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <p className="text-center text-xs text-slate-500 mt-2">
          DocuMind can make mistakes. Consider verifying important information with the cited sources.
        </p>
      </div>
    </div>
  );
};
