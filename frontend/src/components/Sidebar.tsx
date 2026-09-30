import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  Briefcase,
  Target,
  FolderGit2,
  Map,
  TrendingUp,
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const links = [
    { to: '/dashboard', label: 'Overview', icon: LayoutDashboard },
    { to: '/resume-analyzer', label: 'Resume Analyzer', icon: FileText },
    { to: '/job-analyzer', label: 'Job Analyzer', icon: Briefcase },
    { to: '/skill-gap', label: 'Skill Gap Matrix', icon: Target },
    { to: '/projects', label: 'Project Library', icon: FolderGit2 },
    { to: '/roadmap', label: 'Learning Roadmap', icon: Map },
    { to: '/progress', label: 'Progress Tracking', icon: TrendingUp },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 shrink-0 hidden md:flex flex-col min-h-[calc(100vh-4rem)] p-4 space-y-1">
      <div className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-500">
        Career Platform
      </div>
      {links.map((link) => {
        const Icon = link.icon;
        return (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-150 ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20 font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`
            }
          >
            <Icon className="w-4 h-4" />
            <span>{link.label}</span>
          </NavLink>
        );
      })}
    </aside>
  );
};
