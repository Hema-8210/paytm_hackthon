import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, CheckCircle2, AlertCircle, Sparkles, Loader2, ShieldCheck } from 'lucide-react';
import { api, type ResumeAnalysis } from '../services/api';

export const ResumeAnalyzerPage: React.FC = () => {
  const navigate = useNavigate();
  const [dragOver, setDragOver] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [stepMessage, setStepMessage] = useState('Uploading...');
  const [analysisResult, setAnalysisResult] = useState<ResumeAnalysis | null>(null);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (!selected.name.toLowerCase().endsWith('.pdf')) {
        setError('Please upload a valid PDF document.');
        return;
      }
      if (selected.size > 10 * 1024 * 1024) {
        setError('File size exceeds maximum limit of 10 MB.');
        return;
      }
      setError('');
      processUpload(selected);
    }
  };

  const processUpload = async (pdfFile: File) => {
    setAnalyzing(true);
    setError('');
    
    // Simulate step notifications
    setStepMessage('Uploading resume...');
    setTimeout(() => setStepMessage('Extracting text with PyMuPDF...'), 600);
    setTimeout(() => setStepMessage('Detecting skills with NLP...'), 1200);
    setTimeout(() => setStepMessage('Analyzing profile confidence...'), 1800);

    try {
      const result = await api.uploadResume(pdfFile);
      setAnalysisResult(result);
    } catch (err: any) {
      setError(err.message || 'Unable to analyze resume. Please upload a valid PDF under 10 MB.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleConfirmSkills = async () => {
    if (!analysisResult) return;
    setSaving(true);
    try {
      await api.confirmResumeSkills(
        analysisResult.extracted_skills.map(s => ({
          name: s.name,
          proficiency_level: s.proficiency_level
        }))
      );
      navigate('/dashboard');
    } catch {
      alert('Failed to save extracted skills.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
          <FileText className="w-6 h-6 text-indigo-400" />
          <span>Resume Analyzer</span>
        </h1>
        <p className="text-slate-400 text-sm mt-1">Upload your PDF resume to extract skills, education, and experience confidence scores.</p>
      </div>

      {!analysisResult ? (
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl text-center space-y-6">
          {error && (
            <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-xs flex items-center gap-3">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Drag & Drop Area */}
          <div
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                const dropped = e.dataTransfer.files[0];
                processUpload(dropped);
              }
            }}
            className={`border-2 border-dashed rounded-2xl p-10 transition cursor-pointer ${
              dragOver ? 'border-indigo-500 bg-indigo-500/10' : 'border-slate-800 bg-slate-950/50 hover:border-slate-700'
            }`}
          >
            <div className="w-16 h-16 rounded-2xl bg-indigo-600/10 text-indigo-400 border border-indigo-500/20 flex items-center justify-center mx-auto mb-4">
              <Upload className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-white">Upload Resume</h3>
            <p className="text-xs text-slate-400 mt-1">Drag and drop your resume file here or click to browse</p>
            <div className="mt-4 inline-flex items-center gap-3 text-xs text-slate-500 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
              <span>Accepted: <strong className="text-slate-300">PDF</strong></span>
              <span>•</span>
              <span>Maximum size: <strong className="text-slate-300">10 MB</strong></span>
            </div>

            <input
              type="file"
              accept=".pdf"
              id="resume-input"
              className="hidden"
              onChange={handleFileChange}
            />
            <div className="mt-6">
              <label
                htmlFor="resume-input"
                className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs px-6 py-3 rounded-xl shadow-lg shadow-indigo-600/20 transition cursor-pointer inline-flex items-center gap-2"
              >
                <span>Select PDF File</span>
              </label>
            </div>
          </div>

          {analyzing && (
            <div className="p-6 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
              <Loader2 className="w-8 h-8 text-indigo-400 animate-spin mx-auto" />
              <p className="text-sm font-semibold text-slate-200">{stepMessage}</p>
            </div>
          )}
        </div>
      ) : (
        /* Extracted Profile Review Screen */
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" /> Extracted Profile Analysis
              </span>
              <h2 className="text-xl font-bold text-white mt-1">{analysisResult.file_name}</h2>
            </div>
            <button
              onClick={() => setAnalysisResult(null)}
              className="text-xs font-semibold text-slate-400 hover:text-slate-200 cursor-pointer"
            >
              Upload Different PDF
            </button>
          </div>

          {/* Extracted Skills with Confidence Scores */}
          <div>
            <h3 className="text-sm font-bold text-slate-200 mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>Extracted Skills with Confidence Ratings</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {analysisResult.extracted_skills.map((sk) => {
                const confPct = Math.round(sk.confidence * 100);
                return (
                  <div key={sk.name} className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 flex items-center justify-between">
                    <div>
                      <span className="font-bold text-sm text-slate-100">{sk.name}</span>
                      <span className="block text-[11px] text-slate-400">{sk.category} • Level {sk.proficiency_level}/5</span>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-extrabold text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-md border border-indigo-500/20">
                        {confPct}% Confidence
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Action Confirm Button */}
          <div className="pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
            <button
              onClick={handleConfirmSkills}
              disabled={saving}
              className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-6 py-3 rounded-xl shadow-lg shadow-emerald-600/20 transition flex items-center gap-2 text-sm cursor-pointer disabled:opacity-50"
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Confirm & Save to Profile</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
