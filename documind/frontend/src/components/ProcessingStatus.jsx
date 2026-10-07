import React from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

export const ProcessingStatus = ({ status }) => {
  if (!status) return null;

  return (
    <div className="w-full bg-navy-800 border border-navy-700 rounded-xl p-4 flex items-center justify-between mt-4">
      <div className="flex items-center gap-3">
        <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
        <div className="flex flex-col">
          <span className="text-slate-200 font-medium capitalize">{status.stage}</span>
          <span className="text-slate-400 text-sm">{status.message}</span>
        </div>
      </div>
      <div className="w-32 bg-navy-900 h-2 rounded-full overflow-hidden">
        <motion.div 
          className="h-full bg-blue-500"
          initial={{ width: "0%" }}
          animate={{ width: "100%" }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </div>
    </div>
  );
};
