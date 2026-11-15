import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import BibtexModal from './components/BibtexModal';

// Application Pages
import ProposalPage from './pages/ProposalPage';
import SimulationsPage from './pages/SimulationsPage';
import DashboardPage from './pages/DashboardPage';
import NeuralLabPage from './pages/NeuralLabPage';
import VideoStudioPage from './pages/VideoStudioPage';
import ReferencesPage from './pages/ReferencesPage';
import RoadmapPage from './pages/RoadmapPage';

function AppContent() {
  const { activeView, activeBibtexRef, setActiveBibtexRef } = useApp();

  return (
    <div className="dustml-app" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Layout Header */}
      <Navbar />

      {/* Dynamic Main Page Content */}
      <main style={{ flex: 1 }}>
        {activeView === 'proposal' && <ProposalPage />}
        {activeView === 'simulations' && <SimulationsPage />}
        {activeView === 'dashboard' && <DashboardPage />}
        {activeView === 'ai-lab' && <NeuralLabPage />}
        {activeView === 'video' && <VideoStudioPage />}
        {activeView === 'references' && <ReferencesPage />}
        {activeView === 'roadmap' && <RoadmapPage />}
      </main>

      {/* BibTeX Modal */}
      {activeBibtexRef && (
        <BibtexModal 
          reference={activeBibtexRef} 
          onClose={() => setActiveBibtexRef(null)} 
        />
      )}

      {/* Layout Footer */}
      <Footer />

    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}
