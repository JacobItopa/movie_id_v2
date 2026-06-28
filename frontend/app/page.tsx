"use client";

import React, { useState } from 'react';
import MovieResult from '../components/MovieResult';

export default function Home() {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/identify-movie`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to identify movie');
      }

      setResult({
        title: data.title,
        year: data.year,
        streamingLinks: data.streaming_links || [],
      });
    } catch (err: any) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen relative flex flex-col items-center justify-center p-6 sm:p-12">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[20%] left-[20%] w-[500px] h-[500px] bg-[var(--color-primary)] rounded-full mix-blend-screen filter blur-[150px] opacity-10 animate-pulse-glow"></div>
        <div className="absolute bottom-[20%] right-[20%] w-[600px] h-[600px] bg-[var(--color-accent)] rounded-full mix-blend-screen filter blur-[150px] opacity-10"></div>
      </div>

      <div className="relative z-10 w-full max-w-3xl flex flex-col items-center text-center">
        <div className="mb-12 animate-slide-up" style={{ animationDelay: '0.1s' }}>

          <h1 className="text-5xl sm:text-7xl font-black mb-6 tracking-tight">
            Find that <br className="hidden sm:block" />
            <span className="bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] bg-clip-text text-transparent">
              Movie Name
            </span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto font-light leading-relaxed">
            Saw a cool movie Shorts but nobody dropped the title? Paste the link below, and find exactly the title and where you can stream it.
          </p>
        </div>

        <div className="w-full max-w-2xl animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <form onSubmit={handleSubmit} className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
            <div className="relative flex items-center glass-panel rounded-2xl p-2 bg-[#1e2128]/90">
              <div className="pl-4 pr-2 text-gray-500">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                </svg>
              </div>
              <input
                type="url"
                required
                placeholder="https://youtube.com/shorts/..."
                className="flex-1 bg-transparent border-none text-white px-4 py-4 text-lg focus:outline-none focus:ring-0 placeholder-gray-500 w-full"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading}
                className="ml-2 bg-[var(--color-primary)] hover:bg-indigo-500 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[140px]"
              >
                {isLoading ? (
                  <div className="spinner w-6 h-6 border-2 border-white/20 border-t-white"></div>
                ) : (
                  'Identify'
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-6 p-4 glass-panel border border-red-500/30 rounded-xl text-red-400 text-center animate-slide-up bg-red-500/5">
              <p className="flex items-center justify-center gap-2">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {error}
              </p>
            </div>
          )}
        </div>

        {/* Loading States */}
        {isLoading && (
          <div className="mt-16 w-full max-w-md mx-auto text-center animate-slide-up">
            <div className="glass-panel p-8 rounded-2xl">
              <div className="spinner mx-auto mb-6 w-12 h-12 border-4"></div>
              <p className="text-xl font-medium text-white mb-2">Analyzing Video...</p>
              <p className="text-sm text-gray-400">Our AI is watching the clip to identify the exact movie and actors. This usually takes just a few seconds.</p>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !isLoading && (
          <MovieResult
            title={result.title}
            year={result.year}
            streamingLinks={result.streamingLinks}
          />
        )}
      </div>
    </main>
  );
}
