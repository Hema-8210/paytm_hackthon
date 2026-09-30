const API_BASE_URL = '/api';

export interface UserSkill {
  id: number;
  skill_id: number;
  skill_name: string;
  category: string;
  proficiency_level: number;
  source: string;
  confidence: number;
}

export interface TargetRole {
  id: number;
  title: string;
  description?: string;
  category: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  education?: string;
  college?: string;
  branch?: string;
  graduation_year?: number;
  experience_level?: string;
  target_role_id?: number;
  target_role?: TargetRole;
  skills: UserSkill[];
  created_at: string;
}

export interface SkillGapItem {
  skill_id: number;
  name: string;
  category: string;
  current_level: number;
  required_level: number;
  gap: number;
  importance: number;
  priority: 'High' | 'Medium' | 'Low';
  priority_score: number;
}

export interface SkillGapResponse {
  target_role: string;
  requirement_match_percentage: number;
  total_required_skills: number;
  skills_matched: number;
  skills_missing: number;
  skills: SkillGapItem[];
  top_gaps: SkillGapItem[];
  recommended_next_step: string;
}

export interface ProjectSkill {
  skill_id: number;
  skill_name: string;
  importance: number;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  estimated_hours: number;
  category: string;
  prerequisites?: string;
  expected_outcome?: string;
  portfolio_value?: string;
  implementation_steps?: string[];
  skills: ProjectSkill[];
  why_recommended?: string;
  addressed_gaps_count?: number;
}

export interface RoadmapStep {
  id: number;
  phase_number: number;
  phase_title: string;
  title: string;
  description?: string;
  order_index: number;
  status: 'not_started' | 'in_progress' | 'completed';
  skill_id?: number;
  skill_name?: string;
  project_id?: number;
  project_title?: string;
}

export interface Roadmap {
  id: number;
  title: string;
  summary?: string;
  target_role_title: string;
  created_at: string;
  steps: RoadmapStep[];
}

export interface OverallProgress {
  roadmap_completion_percentage: number;
  skills_completed: number;
  skills_in_progress: number;
  projects_completed: number;
  current_streak_days: number;
  remaining_high_priority_gaps: number;
}

export interface SkillItem {
  id: number;
  name: string;
  category: string;
  description?: string;
}

export interface ExtractedSkill {
  skill_id?: number;
  name: string;
  category: string;
  confidence: number;
  proficiency_level: number;
}

export interface ResumeAnalysis {
  resume_id: number;
  file_name: string;
  extracted_text_preview: string;
  sections: Record<string, string>;
  extracted_skills: ExtractedSkill[];
}

export interface RequiredSkillItem {
  skill_id?: number;
  name: string;
  category: string;
  required_level: number;
  importance: number;
  frequency: string;
}

export interface JobAnalysis {
  role: string;
  total_skills_detected: number;
  skills: RequiredSkillItem[];
}

// Helper to get auth header
const getAuthHeaders = () => {
  const token = localStorage.getItem('skillpath_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

// API Methods
export const api = {
  // Auth
  async register(data: { name: string; email: string; password: string }) {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Registration failed');
    }
    return res.json();
  },

  async login(data: { email: string; password: string }) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Login failed');
    }
    return res.json();
  },

  async getMe(): Promise<User> {
    const res = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Unauthorized');
    return res.json();
  },

  // Onboarding & Profile
  async completeOnboarding(data: any): Promise<User> {
    const res = await fetch(`${API_BASE_URL}/users/onboarding`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Onboarding failed');
    }
    return res.json();
  },

  // Skills & Roles
  async getSkills(search?: string, category?: string): Promise<SkillItem[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (category) params.append('category', category);
    const res = await fetch(`${API_BASE_URL}/skills?${params.toString()}`, {
      headers: getAuthHeaders(),
    });
    return res.json();
  },

  async getTargetRoles(): Promise<TargetRole[]> {
    const res = await fetch(`${API_BASE_URL}/jobs/roles`, {
      headers: getAuthHeaders(),
    });
    return res.json();
  },

  async analyzeJobDescription(job_description: string, target_role_id?: number, job_title?: string): Promise<JobAnalysis> {
    const res = await fetch(`${API_BASE_URL}/jobs/analyze`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ job_description, target_role_id, job_title }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Job analysis failed');
    }
    return res.json();
  },

  // Resume Upload
  async uploadResume(file: File): Promise<ResumeAnalysis> {
    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('skillpath_token');
    
    const res = await fetch(`${API_BASE_URL}/resume/upload`, {
      method: 'POST',
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Resume upload failed');
    }
    return res.json();
  },

  async confirmResumeSkills(skills: Array<{ name: string; proficiency_level: number }>): Promise<User> {
    const res = await fetch(`${API_BASE_URL}/resume/confirm-skills`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ skills }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Confirming skills failed');
    }
    return res.json();
  },

  // Skill Gap Analysis
  async getSkillGap(): Promise<SkillGapResponse> {
    const res = await fetch(`${API_BASE_URL}/skill-gap`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Skill gap analysis failed');
    }
    return res.json();
  },

  // Projects
  async getProjects(category?: string, difficulty?: string, search?: string): Promise<Project[]> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (difficulty) params.append('difficulty', difficulty);
    if (search) params.append('search', search);
    const res = await fetch(`${API_BASE_URL}/projects?${params.toString()}`, {
      headers: getAuthHeaders(),
    });
    return res.json();
  },

  async getRecommendedProjects(): Promise<Project[]> {
    const res = await fetch(`${API_BASE_URL}/projects/recommendations`, {
      headers: getAuthHeaders(),
    });
    return res.json();
  },

  async getProjectById(id: number): Promise<Project> {
    const res = await fetch(`${API_BASE_URL}/projects/${id}`, {
      headers: getAuthHeaders(),
    });
    return res.json();
  },

  // Roadmaps
  async getCurrentRoadmap(): Promise<Roadmap> {
    const res = await fetch(`${API_BASE_URL}/roadmaps/current`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Failed to fetch roadmap');
    }
    return res.json();
  },

  async generateRoadmap(weekly_hours: number = 10): Promise<Roadmap> {
    const res = await fetch(`${API_BASE_URL}/roadmaps/generate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ weekly_hours }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Failed to generate roadmap');
    }
    return res.json();
  },

  async updateStepStatus(step_id: number, status: 'not_started' | 'in_progress' | 'completed') {
    const res = await fetch(`${API_BASE_URL}/roadmaps/steps/${step_id}/status`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ status }),
    });
    return res.json();
  },

  // Progress
  async getProgress(): Promise<OverallProgress> {
    const res = await fetch(`${API_BASE_URL}/progress`, {
      headers: getAuthHeaders(),
    });
    return res.json();
  },

  async updateSkillProgress(skill_id: number, progress_percentage: number, status: string) {
    const res = await fetch(`${API_BASE_URL}/progress/${skill_id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ progress_percentage, status }),
    });
    return res.json();
  },

  // AI Assistant Chat
  async sendAssistantMessage(messages: Array<{ role: string; content: string }>): Promise<{ reply: string }> {
    const res = await fetch(`${API_BASE_URL}/assistant/chat`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ messages }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Assistant chat failed');
    }
    return res.json();
  },
};
