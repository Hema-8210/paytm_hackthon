import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { FolderGit2, Search, Clock, Sparkles, Plus, X, Rocket } from 'lucide-react';
import { api, type Project } from '../services/api';

export const ProjectLibraryPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const skillParam = searchParams.get('skill') || '';

  const [projects, setProjects] = useState<Project[]>([]);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState('');
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  useEffect(() => {
    api.getRecommendedProjects()
      .then(res => setProjects(res))
      .catch(() => api.getProjects().then(res => setProjects(res)));
  }, []);

  const categories = ['Web Development', 'Data Science', 'AI/ML', 'Cybersecurity', 'Cloud/DevOps'];
  const difficulties = ['Beginner', 'Intermediate', 'Advanced'];

  const filteredProjects = projects.filter(p => {
    const matchesSearch = p.title.toLowerCase().includes(search.toLowerCase()) || p.description.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = categoryFilter ? p.category === categoryFilter : true;
    const matchesDifficulty = difficultyFilter ? p.difficulty === difficultyFilter : true;
    const matchesSkill = skillParam ? p.skills.some(s => s.skill_name.toLowerCase().includes(skillParam.toLowerCase())) : true;
    return matchesSearch && matchesCategory && matchesDifficulty && matchesSkill;
  });

  const handleAddToRoadmap = async () => {
    try {
      await api.generateRoadmap(10);
      navigate('/roadmap');
    } catch {
      alert('Failed to update roadmap with project.');
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
          <FolderGit2 className="w-6 h-6 text-indigo-400" />
          <span>Project Recommendation Library</span>
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          {skillParam
            ? `Showing projects specifically targeting your missing skill: ${skillParam}`
            : 'Explore practical portfolio projects recommended to close your current skill gaps.'}
        </p>
      </div>

      {/* Filter Bar */}
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-lg flex flex-col md:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search projects..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>
        <select
          value={categoryFilter}
          onChange={e => setCategoryFilter(e.target.value)}
          className="bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-indigo-500 w-full md:w-auto"
        >
          <option value="">All Categories</option>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <select
          value={difficultyFilter}
          onChange={e => setDifficultyFilter(e.target.value)}
          className="bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:border-indigo-500 w-full md:w-auto"
        >
          <option value="">All Difficulties</option>
          {difficulties.map(d => <option key={d} value={d}>{d}</option>)}
        </select>
      </div>

      {/* Project Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.map(proj => (
          <div
            key={proj.id}
            className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between hover:border-slate-700 transition"
          >
            <div>
              {proj.why_recommended && (
                <div className="mb-3 px-2.5 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-lg text-[11px] font-bold flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span className="truncate">{proj.why_recommended}</span>
                </div>
              )}
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-slate-800 px-2.5 py-0.5 rounded border border-slate-700">
                  {proj.category}
                </span>
                <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" /> {proj.estimated_hours}h
                </span>
              </div>
              <h3 className="text-base font-bold text-white mb-2">{proj.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-4 line-clamp-3">{proj.description}</p>

              {/* Skills Developed */}
              <div className="flex flex-wrap gap-1.5 mb-4">
                {proj.skills.map(s => (
                  <span key={s.skill_name} className="text-[11px] font-semibold bg-slate-950 text-slate-300 px-2 py-0.5 rounded border border-slate-800">
                    {s.skill_name}
                  </span>
                ))}
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
              <button
                onClick={() => setSelectedProject(proj)}
                className="text-xs font-bold text-indigo-400 hover:text-indigo-300 cursor-pointer"
              >
                View Steps →
              </button>
              <button
                onClick={handleAddToRoadmap}
                className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-3 py-1.5 rounded-xl shadow transition cursor-pointer flex items-center gap-1"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add to Roadmap</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Project Implementation Modal */}
      {selectedProject && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl p-6 relative space-y-6 max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setSelectedProject(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-200"
            >
              <X className="w-5 h-5" />
            </button>

            <div>
              <span className="text-xs font-bold uppercase text-indigo-400 tracking-wider">{selectedProject.category} • {selectedProject.difficulty}</span>
              <h2 className="text-2xl font-bold text-white mt-1">{selectedProject.title}</h2>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">{selectedProject.description}</p>
            </div>

            {selectedProject.portfolio_value && (
              <div className="bg-indigo-500/10 border border-indigo-500/20 p-3.5 rounded-xl text-xs text-indigo-300">
                <strong>Portfolio Value:</strong> {selectedProject.portfolio_value}
              </div>
            )}

            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Step-by-Step Implementation Guide</h3>
              <div className="space-y-2 text-xs">
                {(selectedProject.implementation_steps || []).map((step, idx) => (
                  <div key={idx} className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-start gap-3">
                    <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center shrink-0 mt-0.5">
                      {idx + 1}
                    </span>
                    <span className="text-slate-200 font-medium leading-relaxed">{step}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
              <button
                onClick={() => setSelectedProject(null)}
                className="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-4 py-2.5 rounded-xl text-xs transition cursor-pointer"
              >
                Close
              </button>
              <button
                onClick={() => {
                  setSelectedProject(null);
                  handleAddToRoadmap();
                }}
                className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-5 py-2.5 rounded-xl shadow-lg transition text-xs flex items-center gap-1.5 cursor-pointer"
              >
                <Rocket className="w-4 h-4" />
                <span>Add to My Roadmap</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
