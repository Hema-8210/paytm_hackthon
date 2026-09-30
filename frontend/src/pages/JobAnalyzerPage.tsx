import React, { useState } from 'react';
import { Briefcase, Sparkles, Loader2, CheckCircle2 } from 'lucide-react';
import { api, type JobAnalysis } from '../services/api';

export const JobAnalyzerPage: React.FC = () => {
  const [jobDescription, setJobDescription] = useState(
    'We are looking for a Data Analyst with experience in Python, SQL, Excel, Power BI, statistics and data visualization. Must be proficient in writing SQL queries, joining tables, and building executive dashboards.'
  );
  const [jobTitle, setJobTitle] = useState('Data Analyst');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<JobAnalysis | null>(null);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobDescription.trim()) return;
    setAnalyzing(true);

    try {
      const res = await api.analyzeJobDescription(jobDescription, undefined, jobTitle);
      setAnalysisResult(res);
    } catch {
      alert('Job description analysis failed.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
          <Briefcase className="w-6 h-6 text-indigo-400" />
          <span>Job Description Analyzer</span>
        </h1>
        <p className="text-slate-400 text-sm mt-1">Paste any target job description below to extract structured skill requirements, categories, and importance scores.</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-6">
        <form onSubmit={handleAnalyze} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Target Role Title</label>
            <input
              type="text"
              value={jobTitle}
              onChange={e => setJobTitle(e.target.value)}
              placeholder="e.g. Data Analyst / Senior Backend Engineer"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Paste Job Description Text</label>
            <textarea
              rows={6}
              value={jobDescription}
              onChange={e => setJobDescription(e.target.value)}
              placeholder="Paste raw job post or requirements here..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            disabled={analyzing || !jobDescription.trim()}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 px-6 rounded-xl shadow-lg shadow-indigo-600/20 transition flex items-center justify-center gap-2 text-sm cursor-pointer disabled:opacity-50"
          >
            {analyzing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Running NLP Pipeline...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Analyze Job Requirements</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Analysis Pipeline Output */}
      {analysisResult && (
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" /> Extracted Skill Requirement Profile
              </span>
              <h2 className="text-xl font-bold text-white mt-1">{analysisResult.role}</h2>
            </div>
            <span className="text-xs font-bold text-slate-400 bg-slate-800 px-3 py-1 rounded-full border border-slate-700">
              {analysisResult.total_skills_detected} Skills Detected
            </span>
          </div>

          <div className="space-y-3">
            {analysisResult.skills.map((item) => (
              <div key={item.name} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="font-bold text-sm text-slate-100">{item.name}</span>
                  <div className="text-xs text-slate-400 mt-0.5 space-x-2">
                    <span>Category: <strong className="text-slate-300">{item.category}</strong></span>
                    <span>•</span>
                    <span>Required Level: <strong className="text-indigo-400">{item.required_level}/5</strong></span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-slate-400">
                    Imp: {(item.importance * 100).toFixed(0)}%
                  </span>
                  <span
                    className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md border ${
                      item.frequency === 'High'
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                    }`}
                  >
                    {item.frequency} FREQ
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
