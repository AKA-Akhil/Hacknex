import { useState } from 'react';
import { askQuestion } from '../services/api';
import toast from 'react-hot-toast';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (question, docIds) => {
    if (!question.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: question,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const data = await askQuestion(question, docIds);
      
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: data.answer,
        citations: data.citations,
        retrievalStats: data.retrieval_stats,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);
      toast.error('Failed to get answer');
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'error',
        content: 'Sorry, I encountered an error while trying to answer your question.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => setMessages([]);

  return { messages, sendMessage, isLoading, clearChat };
};
