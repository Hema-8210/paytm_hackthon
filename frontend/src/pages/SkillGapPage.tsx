import React, { useEffect, useState } from 'react';
import { Target, ExternalLink, X, BookOpen, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { api, type SkillGapResponse, type SkillGapItem } from '../services/api';

export const SkillGapPage: React.FC = () => {
  const [gapData, setGapData] = useState<SkillGapResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'strong' | 'gaps' | 'high'>('all');
  const [selectedSkill, setSelectedSkill] = useState<SkillGapItem | null>(null);

  useEffect(() => {
    api.getSkillGap()
      .then(res => setGapData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8 space-y-4 animate-pulse">
        <div className="h-8 bg-slate-800 rounded w-1/4" />
        <div className="h-96 bg-slate-800 rounded-2xl" />
      </div>
    );
  }

  const allSkills = gapData?.skills || [];

  const filteredSkills = allSkills.filter(item => {
    if (activeTab === 'strong') return item.gap === 0;
    if (activeTab === 'gaps') return item.gap > 0;
    if (activeTab === 'high') return item.priority === 'High' && item.gap > 0;
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
          <Target className="w-6 h-6 text-indigo-400" />
          <span>Detailed Skill Gap Matrix</span>
        </h1>
        <p className="text-slate-400 text-sm mt-1">Comparing your current proficiency against authoritative requirement benchmarks for <strong className="text-slate-200">{gapData?.target_role}</strong>.</p>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-3 overflow-x-auto">
        {[
          { id: 'all', label: `All Skills (${allSkills.length})` },
          { id: 'strong', label: `Strong Skills (${allSkills.filter(s => s.gap === 0).length})` },
          { id: 'gaps', label: `Skill Gaps (${allSkills.filter(s => s.gap > 0).length})` },
          { id: 'high', label: `High Priority (${allSkills.filter(s => s.priority === 'High' && s.gap > 0).length})` }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`whitespace-nowrap px-4 py-2 rounded-xl text-xs font-bold transition cursor-pointer border ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white border-indigo-500 shadow-md'
                : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Skill Matrix Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-950 border-b border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                <th className="p-4">Skill Name</th>
                <th className="p-4">Category</th>
                <th className="p-4 text-center">Your Level</th>
                <th className="p-4 text-center">Required Level</th>
                <th className="p-4 text-center">Gap</th>
                <th className="p-4 text-center">Priority</th>
                <th className="p-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {filteredSkills.map(item => (
                <tr
                  key={item.name}
                  onClick={() => setSelectedSkill(item)}
                  className="hover:bg-slate-800/40 transition cursor-pointer"
                >
                  <td className="p-4 font-bold text-slate-100 flex items-center gap-2">
                    {item.gap === 0 ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                    )}
                    <span>{item.name}</span>
                  </td>
                  <td className="p-4 text-slate-400">{item.category}</td>
                  <td className="p-4 text-center">
                    <span className="font-mono bg-slate-950 px-2 py-1 rounded border border-slate-800 text-slate-200">
                      {item.current_level} / 5
                    </span>
                  </td>
                  <td className="p-4 text-center">
                    <span className="font-mono bg-slate-950 px-2 py-1 rounded border border-slate-800 text-indigo-300">
                      {item.required_level} / 5
                    </span>
                  </td>
                  <td className="p-4 text-center">
                    <span className={`font-mono font-bold ${item.gap > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {item.gap > 0 ? `-${item.gap}` : '0'}
                    </span>
                  </td>
                  <td className="p-4 text-center">
                    <span
                      className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${
                        item.priority === 'High'
                          ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                          : item.priority === 'Medium'
                          ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}
                    >
                      {item.priority}
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    <button className="text-xs font-semibold text-indigo-400 hover:text-indigo-300">
                      View Details →
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Skill Detail Drawer / Modal */}
      {selectedSkill && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 w-full max-w-lg rounded-2xl shadow-2xl p-6 relative space-y-5">
            <button
              onClick={() => setSelectedSkill(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-200"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3">
              <div className="p-3 bg-indigo-600/20 text-indigo-400 rounded-xl border border-indigo-500/30">
                <BookOpen className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">{selectedSkill.name}</h2>
                <p className="text-xs text-slate-400">{selectedSkill.category} • Priority: {selectedSkill.priority}</p>
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Current Proficiency:</span>
                <span className="font-bold text-slate-200">{selectedSkill.current_level} / 5</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Target Role Requirement:</span>
                <span className="font-bold text-indigo-400">{selectedSkill.required_level} / 5</span>
              </div>
              <div className="flex justify-between border-t border-slate-800 pt-2">
                <span className="text-slate-400">Level Gap:</span>
                <span className="font-bold text-rose-400">{selectedSkill.gap} Level(s)</span>
              </div>
            </div>

            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Curated Learning Resources</h3>
              <div className="space-y-2 text-xs">
                <a
                  href={`https://www.google.com/search?q=${encodeURIComponent(selectedSkill.name + ' tutorial beginner')}`}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-between p-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-slate-200 transition"
                >
                  <span>{selectedSkill.name} Fundamentals Guide</span>
                  <ExternalLink className="w-3.5 h-3.5 text-indigo-400" />
                </a>
              </div>
            </div>

            <button
              onClick={() => setSelectedSkill(null)}
              className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-2.5 rounded-xl text-xs transition cursor-pointer"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
