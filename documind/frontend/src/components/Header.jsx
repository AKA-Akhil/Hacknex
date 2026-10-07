import React, { useEffect, useState } from 'react';
import { getHealthStatus } from '../services/api';

export const Header = () => {
  const [health, setHealth] = useState({ ollama_connected: false });

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await getHealthStatus();
        setHealth(res);
      } catch (err) {
        setHealth({ ollama_connected: false });
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-14 bg-navy-800 border-b border-navy-700 flex items-center justify-between px-6 shrink-0 z-10">
      <div className="flex items-center gap-3">
        <img src="/documind-logo.svg" alt="DocuMind Logo" className="w-8 h-8" />
        <h1 className="text-xl font-bold text-slate-100 tracking-tight">DocuMind</h1>
      </div>
      
      <div className="flex items-center gap-2">
        <div className={`w-2.5 h-2.5 rounded-full ${health.ollama_connected ? 'bg-emerald-500' : 'bg-red-500'}`}></div>
        <span className="text-sm text-slate-400 font-medium">
          {health.ollama_connected ? 'System Online' : 'Ollama Disconnected'}
        </span>
      </div>
    </header>
  );
};
