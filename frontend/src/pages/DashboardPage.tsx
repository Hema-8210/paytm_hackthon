import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Target, ArrowRight, AlertTriangle, Rocket, FileText, Map, Briefcase } from 'lucide-react';
import { CircularProgress } from '../components/CircularProgress';
import { api, type User, type SkillGapResponse } from '../services/api';

interface DashboardPageProps {
  user: User;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ user }) => {
  const [gapData, setGapData] = useState<SkillGapResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getSkillGap()
      .then(res => setGapData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8 space-y-6 animate-pulse">
        <div className="h-10 bg-slate-800 rounded-xl w-1/3" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="h-64 bg-slate-800 rounded-2xl" />
          <div className="h-64 bg-slate-800 rounded-2xl lg:col-span-2" />
        </div>
      </div>
    );
  }

  const roleTitle = gapData?.target_role || user.target_role?.title || 'Target Role';
  const matchPct = gapData?.requirement_match_percentage ?? 68.0;

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto space-y-8">
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
            Welcome back, <span className="bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">{user.name}</span> 👋
          </h1>
          <p className="text-slate-400 text-sm mt-1">Here is your real-time skill alignment and career gap breakdown.</p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            to="/resume-analyzer"
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-4 py-2.5 rounded-xl border border-slate-700 transition"
          >
            <FileText className="w-4 h-4 text-indigo-400" />
            <span>Upload Resume</span>
          </Link>
          <Link
            to="/roadmap"
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold px-4 py-2.5 rounded-xl shadow-lg shadow-indigo-600/20 transition"
          >
            <Map className="w-4 h-4" />
            <span>View Roadmap</span>
          </Link>
        </div>
      </div>

      {/* Recommended Next Step Banner */}
      {gapData?.recommended_next_step && (
        <div className="bg-gradient-to-r from-indigo-900/40 via-violet-900/30 to-slate-900 border border-indigo-500/40 p-5 rounded-2xl shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-start gap-3.5">
            <div className="p-2.5 bg-indigo-500/20 rounded-xl text-indigo-400 border border-indigo-500/30 shrink-0 mt-0.5">
              <Rocket className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-400">Recommended Next Action</span>
              <p className="text-sm font-semibold text-slate-100 mt-0.5">{gapData.recommended_next_step}</p>
            </div>
          </div>
          <Link
            to="/roadmap"
            className="whitespace-nowrap bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition flex items-center gap-1.5 cursor-pointer"
          >
            <span>Execute Action</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      )}

      {/* Grid Overview: Role & Circular Score + Skill Bars */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Requirement Match Circular Score Card */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col items-center justify-between">
          <div className="w-full flex items-center justify-between border-b border-slate-800 pb-3 mb-2">
            <div className="flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-indigo-400" />
              <span className="text-xs font-bold uppercase text-slate-400 tracking-wider">Target Role</span>
            </div>
            <Link to="/onboarding" className="text-xs font-semibold text-indigo-400 hover:text-indigo-300">
              Change
            </Link>
          </div>

          <h2 className="text-xl font-bold text-white mb-2 text-center">{roleTitle}</h2>
          
          <CircularProgress percentage={matchPct} size={170} strokeWidth={14} label="Requirement Match" />

          <div className="w-full grid grid-cols-2 gap-2 text-center mt-4 pt-4 border-t border-slate-800 text-xs">
            <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Skills Matched</span>
              <span className="font-bold text-emerald-400 text-base">{gapData?.skills_matched ?? 0}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Skills Missing</span>
              <span className="font-bold text-rose-400 text-base">{gapData?.skills_missing ?? 0}</span>
            </div>
          </div>
        </div>

        {/* Skill Overview Horizontal Bars Chart */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl lg:col-span-2 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <Target className="w-4 h-4 text-indigo-400" />
              <span>Skill Overview Breakdown</span>
            </h2>
            <Link to="/skill-gap" className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
              <span>View Full Matrix</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-4 my-auto">
            {(gapData?.skills || []).slice(0, 5).map((item) => {
              const currentPct = (item.current_level / item.required_level) * 100;
              return (
                <div key={item.name} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-200">{item.name}</span>
                    <span className="text-slate-400 font-mono">
                      {item.current_level}/{item.required_level} ({Math.round(Math.min(100, currentPct))}%)
                    </span>
                  </div>
                  <div className="h-3 bg-slate-950 rounded-full overflow-hidden border border-slate-800 relative">
                    <div
                      className={`h-full transition-all duration-1000 rounded-full ${
                        currentPct >= 100
                          ? 'bg-emerald-500'
                          : currentPct >= 50
                          ? 'bg-amber-400'
                          : 'bg-rose-500'
                      }`}
                      style={{ width: `${Math.min(100, Math.max(5, currentPct))}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span>Legend:</span>
            <div className="flex items-center gap-3 text-[11px]">
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> Matched</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-amber-400" /> Partial</span>
              <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> Gap</span>
            </div>
          </div>
        </div>
      </div>

      {/* Top Skill Gaps Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span>Top Skill Gaps</span>
          </h2>
          <Link to="/projects" className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
            <span>Explore Closing Projects</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {(gapData?.top_gaps || []).map((gap) => (
            <div
              key={gap.name}
              className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg flex flex-col justify-between hover:border-slate-700 transition"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-extrabold text-white">{gap.name}</span>
                  <span
                    className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md border ${
                      gap.priority === 'High'
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                    }`}
                  >
                    {gap.priority} PRIORITY
                  </span>
                </div>
                <div className="text-xs text-slate-400 space-y-1">
                  <p>Category: <span className="text-slate-200">{gap.category}</span></p>
                  <p>Current Level: <span className="font-mono text-slate-200">{gap.current_level}/5</span></p>
                  <p>Required Level: <span className="font-mono text-slate-200">{gap.required_level}/5</span></p>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                <span className="text-[11px] font-semibold text-rose-400">Gap: {gap.gap} Level(s)</span>
                <Link
                  to={`/projects?skill=${encodeURIComponent(gap.name)}`}
                  className="text-xs font-bold text-indigo-400 hover:text-indigo-300"
                >
                  Find Projects →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
