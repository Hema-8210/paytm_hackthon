import React, { useEffect, useState } from 'react';
import { Map, CheckCircle2, Clock, Circle, Sparkles, RefreshCw } from 'lucide-react';
import { api, type Roadmap } from '../services/api';

export const RoadmapPage: React.FC = () => {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    api.getCurrentRoadmap()
      .then(res => setRoadmap(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleRegenerate = async () => {
    setGenerating(true);
    try {
      const res = await api.generateRoadmap(10);
      setRoadmap(res);
    } catch {
      alert('Failed to regenerate roadmap.');
    } finally {
      setGenerating(false);
    }
  };

  const handleStatusToggle = async (stepId: number, currentStatus: string) => {
    if (!roadmap) return;
    const nextStatus = currentStatus === 'completed' ? 'not_started' : currentStatus === 'in_progress' ? 'completed' : 'in_progress';
    
    // Optimistic UI update
    const updatedSteps = roadmap.steps.map(s => s.id === stepId ? { ...s, status: nextStatus as any } : s);
    setRoadmap({ ...roadmap, steps: updatedSteps });

    try {
      await api.updateStepStatus(stepId, nextStatus as any);
    } catch {
      // Revert if error
    }
  };

  if (loading) {
    return (
      <div className="p-8 space-y-4 animate-pulse">
        <div className="h-8 bg-slate-800 rounded w-1/3" />
        <div className="space-y-4">
          <div className="h-32 bg-slate-800 rounded-2xl" />
          <div className="h-32 bg-slate-800 rounded-2xl" />
        </div>
      </div>
    );
  }

  // Group steps by Phase
  const stepsByPhase: Record<number, NonNullable<Roadmap['steps']>> = {};
  if (roadmap?.steps) {
    roadmap.steps.forEach(st => {
      if (!stepsByPhase[st.phase_number]) stepsByPhase[st.phase_number] = [];
      stepsByPhase[st.phase_number].push(st);
    });
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <Map className="w-6 h-6 text-indigo-400" />
            <span>AI Learning Roadmap</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">{roadmap?.title || 'Personalized Career Path'}</p>
        </div>
        <button
          onClick={handleRegenerate}
          disabled={generating}
          className="bg-slate-900 hover:bg-slate-800 text-indigo-400 border border-slate-800 text-xs font-semibold px-4 py-2.5 rounded-xl transition flex items-center gap-2 cursor-pointer disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${generating ? 'animate-spin' : ''}`} />
          <span>Regenerate Roadmap</span>
        </button>
      </div>

      {roadmap?.summary && (
        <div className="bg-indigo-500/10 border border-indigo-500/20 p-4 rounded-2xl text-xs text-indigo-300 flex items-center gap-3">
          <Sparkles className="w-5 h-5 text-indigo-400 shrink-0" />
          <span>{roadmap.summary}</span>
        </div>
      )}

      {/* 5-Phase Interactive Timeline */}
      <div className="space-y-8 relative before:absolute before:inset-0 before:left-6 before:w-0.5 before:bg-slate-800 before:-z-0">
        {Object.entries(stepsByPhase).map(([phaseNumStr, steps]) => {
          const phaseNum = parseInt(phaseNumStr);
          const phaseTitle = steps[0]?.phase_title || `PHASE ${phaseNum}`;

          return (
            <div key={phaseNum} className="relative z-10 space-y-4">
              {/* Phase Header */}
              <div className="flex items-center gap-3 bg-slate-950/80 px-4 py-2 rounded-xl border border-slate-800 w-max">
                <span className="w-6 h-6 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center">
                  {phaseNum}
                </span>
                <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider">{phaseTitle}</span>
              </div>

              {/* Step Cards */}
              <div className="space-y-3 pl-8">
                {steps.map(step => {
                  const isCompleted = step.status === 'completed';
                  const isInProgress = step.status === 'in_progress';

                  return (
                    <div
                      key={step.id}
                      className={`bg-slate-900 border rounded-2xl p-5 shadow-lg transition flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${
                        isCompleted
                          ? 'border-emerald-500/40 bg-emerald-950/10'
                          : isInProgress
                          ? 'border-indigo-500/50 bg-indigo-950/10'
                          : 'border-slate-800'
                      }`}
                    >
                      <div className="space-y-1 max-w-xl">
                        <div className="flex items-center gap-2">
                          <h3 className={`text-sm font-bold ${isCompleted ? 'text-emerald-300 line-through' : 'text-white'}`}>
                            {step.title}
                          </h3>
                          {step.project_title && (
                            <span className="text-[10px] font-bold bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded border border-indigo-500/30">
                              Portfolio Project
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-slate-400 leading-relaxed">{step.description}</p>
                      </div>

                      {/* Status Toggle Button */}
                      <button
                        onClick={() => handleStatusToggle(step.id, step.status)}
                        className={`whitespace-nowrap px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer shrink-0 border ${
                          isCompleted
                            ? 'bg-emerald-600 text-white border-emerald-500 shadow-lg shadow-emerald-600/20'
                            : isInProgress
                            ? 'bg-indigo-600 text-white border-indigo-500 shadow-lg shadow-indigo-600/20'
                            : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-slate-200'
                        }`}
                      >
                        {isCompleted ? (
                          <>
                            <CheckCircle2 className="w-4 h-4" />
                            <span>Completed</span>
                          </>
                        ) : isInProgress ? (
                          <>
                            <Clock className="w-4 h-4 animate-spin" />
                            <span>In Progress</span>
                          </>
                        ) : (
                          <>
                            <Circle className="w-4 h-4" />
                            <span>Mark Started</span>
                          </>
                        )}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
