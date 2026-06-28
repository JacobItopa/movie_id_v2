import React from 'react';

interface StreamingLink {
  title: string;
  url: string;
  content: string;
}

interface MovieResultProps {
  title: string;
  year: string;
  streamingLinks: StreamingLink[];
}

export default function MovieResult({ title, year, streamingLinks }: MovieResultProps) {
  return (
    <div className="w-full max-w-2xl mx-auto mt-12 animate-slide-up">
      <div className="glass-panel rounded-2xl p-8 relative overflow-hidden">
        {/* Glow effect */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-[var(--color-primary)] rounded-full blur-[80px] opacity-20 pointer-events-none"></div>
        <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-[var(--color-accent)] rounded-full blur-[80px] opacity-20 pointer-events-none"></div>

        <div className="relative z-10 text-center mb-8">
          <h2 className="text-sm font-semibold tracking-widest text-gray-400 uppercase mb-2">Movie Identified</h2>
          <h3 className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] bg-clip-text text-transparent inline-block">
            {title}
          </h3>
          {year && (
            <p className="text-xl text-gray-300 mt-2 font-medium">{year}</p>
          )}
        </div>

        <div className="relative z-10">
          <h4 className="text-lg font-medium text-white mb-4 flex items-center gap-2">
            <svg className="w-5 h-5 text-[var(--color-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Where to Watch
          </h4>
          
          {streamingLinks.length > 0 ? (
            <div className="space-y-3">
              {streamingLinks.map((link, idx) => (
                <a
                  key={idx}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all duration-200 group"
                >
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-gray-200 group-hover:text-white transition-colors">{link.title}</span>
                    <svg className="w-5 h-5 text-gray-500 group-hover:text-[var(--color-primary)] transition-colors transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </a>
              ))}
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-white/5 border border-white/10 text-center text-gray-400">
              No direct streaming links found. Try a manual search!
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
