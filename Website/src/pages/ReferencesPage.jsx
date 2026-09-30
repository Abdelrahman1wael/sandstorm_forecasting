import React from 'react';
import ReferencesDatabase from '../components/ReferencesDatabase';
import { useApp } from '../context/AppContext';

export default function ReferencesPage() {
  const { setActiveBibtexRef } = useApp();

  return <ReferencesDatabase onOpenBibtex={ref => setActiveBibtexRef(ref)} />;
}
