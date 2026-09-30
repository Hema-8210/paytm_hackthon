import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { CareerAssistantWidget } from './components/CareerAssistantWidget';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { OnboardingPage } from './pages/OnboardingPage';
import { DashboardPage } from './pages/DashboardPage';
import { ResumeAnalyzerPage } from './pages/ResumeAnalyzerPage';
import { JobAnalyzerPage } from './pages/JobAnalyzerPage';
import { SkillGapPage } from './pages/SkillGapPage';
import { ProjectLibraryPage } from './pages/ProjectLibraryPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { ProgressPage } from './pages/ProgressPage';
import { api, type User } from './services/api';

const AppLayout: React.FC<{ user: User | null; onLogout: () => void }> = ({ user, onLogout }) => {
  const location = useLocation();
  const isDashboardRoute = [
    '/dashboard',
    '/resume-analyzer',
    '/job-analyzer',
    '/skill-gap',
    '/projects',
    '/roadmap',
    '/progress'
  ].includes(location.pathname);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar user={user} onLogout={onLogout} />
      {isDashboardRoute && user ? (
        <div className="flex-1 flex">
          <Sidebar />
          <main className="flex-1 overflow-x-hidden">
            <Routes>
              <Route path="/dashboard" element={<DashboardPage user={user} />} />
              <Route path="/resume-analyzer" element={<ResumeAnalyzerPage />} />
              <Route path="/job-analyzer" element={<JobAnalyzerPage />} />
              <Route path="/skill-gap" element={<SkillGapPage />} />
              <Route path="/projects" element={<ProjectLibraryPage />} />
              <Route path="/roadmap" element={<RoadmapPage />} />
              <Route path="/progress" element={<ProgressPage />} />
            </Routes>
          </main>
        </div>
      ) : (
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage onLoginSuccess={(token) => { localStorage.setItem('skillpath_token', token); window.location.href = '/dashboard'; }} />} />
            <Route path="/register" element={<RegisterPage onRegisterSuccess={(token) => { localStorage.setItem('skillpath_token', token); window.location.href = '/onboarding'; }} />} />
            <Route path="/onboarding" element={<OnboardingPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      )}
      {/* Floating AI Assistant Widget for logged-in users */}
      {user && <CareerAssistantWidget />}
    </div>
  );
};

export function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUser = async () => {
    const token = localStorage.getItem('skillpath_token');
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      const me = await api.getMe();
      setUser(me);
    } catch {
      localStorage.removeItem('skillpath_token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('skillpath_token');
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400 font-sans text-sm">
        Loading SkillPath Platform...
      </div>
    );
  }

  return (
    <BrowserRouter>
      <AppLayout user={user} onLogout={handleLogout} />
    </BrowserRouter>
  );
}

export default App;
