import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatPanel } from './components/ChatPanel';
import { SourceViewer } from './components/SourceViewer';
import { Header } from './components/Header';
import { useDocuments } from './hooks/useDocuments';

function App() {
  const { documents, fetchDocuments, deleteDocument } = useDocuments();
  const [selectedDocIds, setSelectedDocIds] = useState([]);
  const [selectedCitation, setSelectedCitation] = useState(null);

  const toggleDocSelection = (docId) => {
    setSelectedDocIds(prev => 
      prev.includes(docId) ? prev.filter(id => id !== docId) : [...prev, docId]
    );
  };

  return (
    <div className="flex flex-col h-screen bg-navy-900 text-slate-100 overflow-hidden">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar 
          documents={documents} 
          onRefresh={fetchDocuments}
          onDelete={deleteDocument}
          selectedDocIds={selectedDocIds}
          onToggleDoc={toggleDocSelection}
        />
        <main className="flex-1 flex overflow-hidden relative">
          <ChatPanel 
            documents={documents}
            selectedDocIds={selectedDocIds}
            onCitationClick={setSelectedCitation}
          />
          <SourceViewer 
            citation={selectedCitation} 
            onClose={() => setSelectedCitation(null)} 
          />
        </main>
      </div>
    </div>
  );
}

export default App;
