import React from 'react';
import { Link } from 'react-router-dom';
import {
  Compass,
  Upload,
  Target,
  FileCheck,
  Rocket,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Code2,
  Brain,
  BarChart3,
  BookOpen
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const steps = [
    {
      num: '01',
      title: 'Upload Resume',
      desc: 'Our AI extracts your existing skills, education, and proficiency levels with confidence scores.',
      icon: Upload,
    },
    {
      num: '02',
      title: 'Choose Target Role',
      desc: 'Select from top industry job roles or paste a custom job description for instant NLP analysis.',
      icon: Target,
    },
    {
      num: '03',
      title: 'Discover Skill Gaps',
      desc: 'Get an empirical Requirement Match Score and prioritized list of your high-impact missing skills.',
      icon: FileCheck,
    },
    {
      num: '04',
      title: 'Build Recommended Projects',
      desc: 'Work on hand-crafted portfolio projects specifically designed to close your target skill gaps.',
      icon: Code2,
    },
    {
      num: '05',
      title: 'Follow Your Roadmap',
      desc: 'Execute your 5-phase personalized learning path and track real-time progress to job readiness.',
      icon: Rocket,
    },
  ];

  const features = [
    {
      title: 'Resume Intelligence',
      desc: 'Parses PDF resumes instantly, detecting technical skills with 95%+ precision confidence.',
      icon: Brain,
    },
    {
      title: 'Skill-Gap Analysis',
      desc: 'Deterministic formula comparing current proficiency vs required role standards.',
      icon: BarChart3,
    },
    {
      title: 'Semantic Skill Matching',
      desc: 'Normalizes aliases (e.g. ReactJS -> React, ML -> Machine Learning) with TF-IDF similarity.',
      icon: Sparkles,
    },
    {
      title: 'Practical Projects',
      desc: 'Filterable library of 35+ real-world projects with step-by-step implementation guides.',
      icon: Code2,
    },
    {
      title: 'Personalized Roadmap',
      desc: 'Multi-phase sequenced learning path validated against your target database skill graph.',
      icon: BookOpen,
    },
    {
      title: 'Progress Tracking',
      desc: 'Real-time dashboard updates, streak monitoring, and high-priority gap countdowns.',
      icon: CheckCircle2,
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Hero Section */}
      <section className="relative pt-20 pb-24 overflow-hidden border-b border-slate-800">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.25),rgba(255,255,255,0))] pointer-events-none" />
        <div className="max-w-6xl mx-auto px-4 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold mb-6 shadow-sm">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Empirical AI Career Acceleration</span>
          </div>
          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
            Build the skills your dream job <span className="bg-gradient-to-r from-indigo-400 via-violet-400 to-purple-400 bg-clip-text text-transparent">actually needs.</span>
          </h1>
          <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto mb-10 leading-relaxed font-normal">
            SkillPath compares your current skills with real job requirements, identifies your gaps, and gives you practical projects and a learning roadmap to close them.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/register"
              className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-8 py-4 rounded-xl shadow-xl shadow-indigo-600/30 transition-all duration-200 hover:scale-105 flex items-center justify-center gap-2 text-base cursor-pointer"
            >
              <span>Analyze My Skills</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <a
              href="#how-it-works"
              className="w-full sm:w-auto bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white font-semibold px-8 py-4 rounded-xl border border-slate-800 transition text-base flex items-center justify-center cursor-pointer"
            >
              Explore How It Works
            </a>
          </div>

          {/* Core Product Loop Pill */}
          <div className="mt-16 pt-8 border-t border-slate-800/80 max-w-4xl mx-auto flex flex-wrap items-center justify-center gap-3 text-xs font-semibold text-slate-400">
            <span className="text-slate-500">CORE LOOP:</span>
            <span className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-indigo-400">JOB</span>
            <span>→</span>
            <span className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-indigo-400">SKILLS</span>
            <span>→</span>
            <span className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-indigo-400">GAP</span>
            <span>→</span>
            <span className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-indigo-400">PROJECT</span>
            <span>→</span>
            <span className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-indigo-400">LEARNING</span>
            <span>→</span>
            <span className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-emerald-400">PROGRESS</span>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-slate-900/50 border-b border-slate-800">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-extrabold text-white mb-4">How SkillPath Works</h2>
            <p className="text-slate-400 text-base">Five actionable steps to transform your raw profile into job offer readiness.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            {steps.map((step, idx) => {
              const Icon = step.icon;
              return (
                <div key={idx} className="bg-slate-900 border border-slate-800 p-6 rounded-2xl relative flex flex-col justify-between hover:border-indigo-500/50 transition duration-200">
                  <div>
                    <span className="text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-md border border-indigo-500/20 inline-block mb-4">
                      {step.num}
                    </span>
                    <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-indigo-400 mb-4 border border-slate-700">
                      <Icon className="w-5 h-5" />
                    </div>
                    <h3 className="text-base font-bold text-slate-100 mb-2">{step.title}</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{step.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Why SkillPath Section */}
      <section className="py-20 border-b border-slate-800">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-extrabold text-white mb-4">Why SkillPath?</h2>
            <p className="text-slate-400 text-base">Built with robust NLP, empirical matching algorithms, and no fake hardcoded outputs.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feat, idx) => {
              const Icon = feat.icon;
              return (
                <div key={idx} className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl hover:border-slate-700 transition">
                  <div className="w-12 h-12 rounded-xl bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mb-5">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-bold text-white mb-2">{feat.title}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{feat.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="py-20 bg-gradient-to-b from-slate-900 to-slate-950 text-center">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white mb-6">Start Building Your Career Path Today</h2>
          <p className="text-slate-400 text-base max-w-xl mx-auto mb-8">
            Upload your resume, select your target role, and discover your personalized project roadmap in seconds.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-8 py-4 rounded-xl shadow-xl shadow-indigo-600/25 transition hover:scale-105 text-base cursor-pointer"
          >
            <span>Start Building Your Career Path</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-slate-950 border-t border-slate-900 text-center text-xs text-slate-500">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Compass className="w-4 h-4 text-indigo-400" />
            <span className="font-bold text-slate-300">SkillPath</span>
            <span>— Turn your career goal into a path you can actually follow.</span>
          </div>
          <p>© {new Date().getFullYear()} SkillPath Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};
