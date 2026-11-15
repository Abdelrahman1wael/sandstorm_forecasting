import React, { useState } from 'react';
import videoData from '../data/videoMetadata.json';
import { Play, Pause, ChevronLeft, ChevronRight, Video, FileText, CheckCircle2, Volume2, Download } from 'lucide-react';

export default function VideoStudio() {
  const [currentSceneIdx, setCurrentSceneIdx] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const scenes = videoData.scenes || [];
  const currentScene = scenes[currentSceneIdx] || scenes[0];

  const handleNext = () => {
    if (currentSceneIdx < scenes.length - 1) {
      setCurrentSceneIdx(currentSceneIdx + 1);
    }
  };

  const handlePrev = () => {
    if (currentSceneIdx > 0) {
      setCurrentSceneIdx(currentSceneIdx - 1);
    }
  };

  return (
    <section className="container" style={{ padding: '2rem 0 3.5rem' }}>
      
      <div className="section-head" style={{ marginBottom: '2rem' }}>
        <span className="section-tag">Multimedia Presentation Studio</span>
        <h2 className="section-title">Official Academic Video Presentation (10 Scenes • ~8.5 Min)</h2>
        <p className="section-desc">
          Interactive slide-by-slide academic presentation with synchronized English voiceover scripts, empirical takeaway bullets, and high-resolution conceptual diagrams.
        </p>
      </div>

      {/* Main Video & Scene Inspector Frame */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        
        {/* Left: Visual Scene Card */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <span className="stat-badge" style={{ background: 'rgba(56,189,248,0.15)', color: '#38bdf8' }}>
                {currentScene.tag}
              </span>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8', fontFamily: 'var(--font-mono)' }}>
                Scene {currentScene.id} of {scenes.length} • {currentScene.time}
              </span>
            </div>

            <h3 style={{ fontSize: '1.25rem', color: '#f8fafc', marginBottom: '1rem', fontWeight: 800 }}>
              {currentScene.title}
            </h3>

            {/* Visual Image / Slide Canvas */}
            <div style={{ position: 'relative', width: '100%', height: 260, borderRadius: 10, overflow: 'hidden', border: '1px solid var(--border-subtle)', marginBottom: '1rem', background: '#050811' }}>
              <img 
                src={currentScene.image_url} 
                alt={currentScene.title}
                style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.85 }} 
              />
              <div style={{ position: 'absolute', bottom: 0, insetInline: 0, background: 'linear-gradient(to top, rgba(7,11,20,0.95), transparent)', padding: '1rem 0.85rem 0.5rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#cbd5e1', fontStyle: 'italic' }}>
                  {currentScene.image_caption}
                </span>
              </div>
            </div>
          </div>

          {/* Scrubber & Player Controls */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '0.75rem', borderTop: '1px solid var(--border-subtle)' }}>
            <button 
              onClick={handlePrev}
              disabled={currentSceneIdx === 0}
              className="btn btn-secondary" 
              style={{ padding: '0.45rem 0.75rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: 4 }}
            >
              <ChevronLeft size={16} /> Prev Scene
            </button>

            <button 
              onClick={() => setIsPlaying(!isPlaying)}
              className="btn btn-primary"
              style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: 6 }}
            >
              {isPlaying ? <Pause size={16} /> : <Play size={16} />}
              <span>{isPlaying ? 'Pause Narration' : 'Play Narration'}</span>
            </button>

            <button 
              onClick={handleNext}
              disabled={currentSceneIdx === scenes.length - 1}
              className="btn btn-secondary" 
              style={{ padding: '0.45rem 0.75rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: 4 }}
            >
              Next Scene <ChevronRight size={16} />
            </button>
          </div>
        </div>

        {/* Right: Voiceover Transcript & Key Takeaways */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          <div>
            <h4 style={{ fontSize: '1rem', color: '#38bdf8', marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: 6 }}>
              <Volume2 size={17} /> Spoken Voiceover Script (English Neural Narration)
            </h4>
            <div style={{ background: 'rgba(5,8,17,0.7)', padding: '1rem', borderRadius: 8, fontSize: '0.88rem', color: '#f8fafc', lineHeight: 1.6, borderLeft: '3px solid #38bdf8', maxHeight: 160, overflowY: 'auto' }}>
              "{currentScene.voiceover}"
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: '1rem', color: 'var(--accent-amber)', marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: 6 }}>
              <FileText size={17} /> Core Takeaways & Empirical Arguments
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {currentScene.key_points.map((pt, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 8, fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                  <CheckCircle2 size={15} color="#34d399" style={{ flexShrink: 0, marginTop: 2 }} />
                  <span>{pt}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Tags */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginTop: 'auto' }}>
            {currentScene.tags.map((tag, i) => (
              <span key={i} className="stat-badge" style={{ background: 'rgba(255,255,255,0.05)', color: '#cbd5e1', fontSize: '0.7rem' }}>
                #{tag}
              </span>
            ))}
          </div>

        </div>

      </div>

      {/* 10-Scene Thumbnail Scrubber Bar */}
      <div className="glass-panel" style={{ padding: '1rem' }}>
        <div style={{ fontSize: '0.82rem', color: '#94a3b8', marginBottom: '0.75rem', fontWeight: 600 }}>
          Presentation Navigation Track (Select Any Scene):
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(90px, 1fr))', gap: '0.5rem' }}>
          {scenes.map((s, idx) => (
            <button
              key={s.id}
              onClick={() => setCurrentSceneIdx(idx)}
              style={{
                background: currentSceneIdx === idx ? 'rgba(56,189,248,0.2)' : 'rgba(15,23,42,0.6)',
                border: currentSceneIdx === idx ? '2px solid #38bdf8' : '1px solid var(--border-subtle)',
                borderRadius: 6,
                padding: '0.5rem 0.25rem',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'var(--transition)'
              }}
            >
              <div style={{ fontSize: '0.72rem', fontWeight: 700, color: currentSceneIdx === idx ? '#38bdf8' : '#f8fafc' }}>
                Scene {s.id}
              </div>
              <div style={{ fontSize: '0.65rem', color: '#94a3b8' }}>
                {s.time}
              </div>
            </button>
          ))}
        </div>
      </div>

    </section>
  );
}
