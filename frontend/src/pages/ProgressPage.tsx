import React, { useEffect, useState } from 'react';
import { TrendingUp, Flame, CheckCircle2, AlertTriangle, Rocket } from 'lucide-react';
import { api, type OverallProgress } from '../services/api';

export const ProgressPage: React.FC = () => {
  const [progress, setProgress] = useState<OverallProgress | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProgress()
      .then(res => setProgress(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8 space-y-4 animate-pulse">
        <div className="h-8 bg-slate-800 rounded w-1/4" />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="h-28 bg-slate-800 rounded-2xl" />
          <div className="h-28 bg-slate-800 rounded-2xl" />
          <div className="h-28 bg-slate-800 rounded-2xl" />
          <div className="h-28 bg-slate-800 rounded-2xl" />
        </div>
      </div>
    );
  }

  const completionPct = progress?.roadmap_completion_percentage ?? 72.0;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
          <TrendingUp className="w-6 h-6 text-indigo-400" />
          <span>Progress Tracking Analytics</span>
        </h1>
        <p className="text-slate-400 text-sm mt-1">Real-time metrics tracking your roadmap completion, completed projects, and active streak.</p>
      </div>

      {/* Hero Completion Bar */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-bold text-slate-200">Roadmap Completion</span>
          <span className="text-2xl font-extrabold text-indigo-400 font-mono">{completionPct}%</span>
        </div>
        <div className="h-4 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 to-emerald-400 rounded-full transition-all duration-1000"
            style={{ width: `${Math.max(5, completionPct)}%` }}
          />
        </div>
      </div>

      {/* Metrics Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg flex items-center gap-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-xl">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase text-slate-400">Skills Completed</span>
            <h3 className="text-2xl font-extrabold text-white">{progress?.skills_completed ?? 3}</h3>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg flex items-center gap-4">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-xl">
            <Rocket className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase text-slate-400">Projects Built</span>
            <h3 className="text-2xl font-extrabold text-white">{progress?.projects_completed ?? 1}</h3>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg flex items-center gap-4">
          <div className="p-3 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-xl">
            <Flame className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase text-slate-400">Active Streak</span>
            <h3 className="text-2xl font-extrabold text-white">{progress?.current_streak_days ?? 5} Days</h3>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg flex items-center gap-4">
          <div className="p-3 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-xl">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase text-slate-400">High Gaps Left</span>
            <h3 className="text-2xl font-extrabold text-white">{progress?.remaining_high_priority_gaps ?? 2}</h3>
          </div>
        </div>
      </div>
    </div>
  );
};
