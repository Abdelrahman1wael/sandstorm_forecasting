import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [activeView, setActiveView] = useState('proposal');
  const [selectedStationCode, setSelectedStationCode] = useState('DH');
  const [activeBibtexRef, setActiveBibtexRef] = useState(null);

  return (
    <AppContext.Provider
      value={{
        activeView,
        setActiveView,
        selectedStationCode,
        setSelectedStationCode,
        activeBibtexRef,
        setActiveBibtexRef
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
