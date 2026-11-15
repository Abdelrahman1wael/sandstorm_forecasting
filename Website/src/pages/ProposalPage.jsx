import React from 'react';
import Hero from '../components/Hero';
import ProposalChapters from '../components/ProposalChapters';
import { useApp } from '../context/AppContext';

export default function ProposalPage() {
  const { setActiveView } = useApp();

  return (
    <>
      <Hero setActiveView={setActiveView} />
      <ProposalChapters />
    </>
  );
}
