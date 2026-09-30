import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Target, Search, Plus, Check, ArrowRight, BookOpen, GraduationCap, Briefcase } from 'lucide-react';
import { api, type TargetRole } from '../services/api';

const DEFAULT_POPULAR_SKILLS = [
  'Python', 'Java', 'C', 'C++', 'JavaScript', 'TypeScript', 'React', 'Node.js',
  'FastAPI', 'SQL', 'MongoDB', 'PostgreSQL', 'Git', 'Docker', 'AWS',
  'Machine Learning', 'Data Analysis', 'Power BI', 'Tableau', 'Microsoft Excel',
  'HTML5', 'CSS3', 'Tailwind CSS', 'PyTorch', 'Cybersecurity', 'UI/UX Design'
];

export const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const [education, setEducation] = useState('B.Tech');
  const [college, setCollege] = useState('');
  const [branch, setBranch] = useState('Computer Science');
  const [graduationYear, setGraduationYear] = useState<number>(2026);
  const [experienceLevel, setExperienceLevel] = useState('Beginner');
  
  const [roles, setRoles] = useState<TargetRole[]>([]);
  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);
  const [customRoleTitle, setCustomRoleTitle] = useState('');

  const [selectedSkills, setSelectedSkills] = useState<Array<{ name: string; proficiency_level: number }>>([
    { name: 'Python', proficiency_level: 3 },
    { name: 'SQL', proficiency_level: 2 }
  ]);
  const [skillSearch, setSkillSearch] = useState('');
  const [customSkillInput, setCustomSkillInput] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getTargetRoles()
      .then(res => {
        setRoles(res);
        if (res.length > 0) setSelectedRoleId(res[0].id);
      })
      .catch(() => {});
  }, []);

  const toggleSkill = (skillName: string) => {
    if (selectedSkills.some(s => s.name.toLowerCase() === skillName.toLowerCase())) {
      setSelectedSkills(selectedSkills.filter(s => s.name.toLowerCase() !== skillName.toLowerCase()));
    } else {
      setSelectedSkills([...selectedSkills, { name: skillName, proficiency_level: 3 }]);
    }
  };

  const addCustomSkill = () => {
    if (!customSkillInput.trim()) return;
    if (!selectedSkills.some(s => s.name.toLowerCase() === customSkillInput.trim().toLowerCase())) {
      setSelectedSkills([...selectedSkills, { name: customSkillInput.trim(), proficiency_level: 3 }]);
    }
    setCustomSkillInput('');
  };

  const handleProficiencyChange = (skillName: string, level: number) => {
    setSelectedSkills(selectedSkills.map(s => s.name === skillName ? { ...s, proficiency_level: level } : s));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.completeOnboarding({
        education,
        college,
        branch,
        graduation_year: graduationYear,
        experience_level: experienceLevel,
        target_role_id: selectedRoleId,
        target_role_title: customRoleTitle || undefined,
        skills: selectedSkills
      });
      navigate('/dashboard');
    } catch {
      alert('Failed to save profile onboarding details.');
    } finally {
      setLoading(false);
    }
  };

  const filteredSkills = DEFAULT_POPULAR_SKILLS.filter(s =>
    s.toLowerCase().includes(skillSearch.toLowerCase())
  );

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="text-center mb-10">
        <div className="inline-flex p-3 bg-indigo-600/10 border border-indigo-500/20 rounded-2xl text-indigo-400 mb-3">
          <Target className="w-8 h-8" />
        </div>
        <h1 className="text-3xl font-extrabold text-white">Setup Your Career Profile</h1>
        <p className="text-slate-400 text-sm mt-1">Tell us about your background and target role so SkillPath can build your personalized gap matrix.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Step 1: Academic & Experience Profile */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-indigo-400" />
            <span>Academic & Experience Background</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Education Degree</label>
              <input
                type="text"
                value={education}
                onChange={e => setEducation(e.target.value)}
                placeholder="e.g. B.Tech / B.S. CS"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">College / University</label>
              <input
                type="text"
                value={college}
                onChange={e => setCollege(e.target.value)}
                placeholder="State Technological University"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Branch / Major</label>
              <input
                type="text"
                value={branch}
                onChange={e => setBranch(e.target.value)}
                placeholder="Computer Science & Engineering"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Graduation Year</label>
              <input
                type="number"
                value={graduationYear}
                onChange={e => setGraduationYear(parseInt(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Current Experience Level</label>
            <div className="grid grid-cols-3 gap-3">
              {['Beginner', 'Intermediate', 'Advanced'].map(lvl => (
                <button
                  type="button"
                  key={lvl}
                  onClick={() => setExperienceLevel(lvl)}
                  className={`py-2.5 rounded-xl border text-xs font-semibold transition cursor-pointer ${
                    experienceLevel === lvl
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow-md'
                      : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-slate-200'
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Step 2: Target Role Selection */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-indigo-400" />
            <span>Target Career Role</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 max-h-60 overflow-y-auto pr-1">
            {roles.map(r => (
              <button
                type="button"
                key={r.id}
                onClick={() => {
                  setSelectedRoleId(r.id);
                  setCustomRoleTitle('');
                }}
                className={`p-3 rounded-xl border text-left text-xs font-semibold transition cursor-pointer flex items-center justify-between ${
                  selectedRoleId === r.id && !customRoleTitle
                    ? 'bg-indigo-600/20 border-indigo-500 text-indigo-300'
                    : 'bg-slate-950 text-slate-300 border-slate-800 hover:border-slate-700'
                }`}
              >
                <span>{r.title}</span>
                {selectedRoleId === r.id && !customRoleTitle && <Check className="w-4 h-4 text-indigo-400" />}
              </button>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-slate-800">
            <label className="block text-xs font-semibold text-slate-300 mb-1">Or enter custom target role title:</label>
            <input
              type="text"
              value={customRoleTitle}
              onChange={e => setCustomRoleTitle(e.target.value)}
              placeholder="e.g. AI Robotics Systems Engineer"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        {/* Step 3: Searchable Skill Chips */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
          <h2 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-indigo-400" />
            <span>Select Your Existing Skills</span>
          </h2>
          <p className="text-xs text-slate-400 mb-4">Click chips to select skills you currently know. You can also upload a resume later to auto-extract skills.</p>

          <div className="relative mb-4">
            <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
            <input
              type="text"
              value={skillSearch}
              onChange={e => setSkillSearch(e.target.value)}
              placeholder="Search skills (e.g. Python, SQL, React)..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto mb-4 p-1">
            {filteredSkills.map(sk => {
              const isSelected = selectedSkills.some(s => s.name.toLowerCase() === sk.toLowerCase());
              return (
                <button
                  type="button"
                  key={sk}
                  onClick={() => toggleSkill(sk)}
                  className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition cursor-pointer flex items-center gap-1.5 ${
                    isSelected
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow-md'
                      : 'bg-slate-950 text-slate-300 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <span>{sk}</span>
                  {isSelected && <Check className="w-3.5 h-3.5" />}
                </button>
              );
            })}
          </div>

          {/* Add custom skill input */}
          <div className="flex items-center gap-2 pt-2 border-t border-slate-800">
            <input
              type="text"
              value={customSkillInput}
              onChange={e => setCustomSkillInput(e.target.value)}
              placeholder="Add custom skill..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
            />
            <button
              type="button"
              onClick={addCustomSkill}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-1 cursor-pointer border border-slate-700"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add</span>
            </button>
          </div>

          {/* Proficiency rating for selected skills */}
          {selectedSkills.length > 0 && (
            <div className="mt-6 pt-4 border-t border-slate-800">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Rate Your Selected Proficiency (1-5 Level)</h3>
              <div className="space-y-2.5">
                {selectedSkills.map(sk => (
                  <div key={sk.name} className="flex items-center justify-between bg-slate-950 p-2.5 rounded-xl border border-slate-800/80">
                    <span className="text-xs font-semibold text-slate-200">{sk.name}</span>
                    <div className="flex items-center gap-1">
                      {[1, 2, 3, 4, 5].map(lvl => (
                        <button
                          type="button"
                          key={lvl}
                          onClick={() => handleProficiencyChange(sk.name, lvl)}
                          className={`w-6 h-6 rounded-md text-xs font-bold transition cursor-pointer ${
                            sk.proficiency_level >= lvl
                              ? 'bg-indigo-600 text-white'
                              : 'bg-slate-800 text-slate-500'
                          }`}
                        >
                          {lvl}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-4 px-6 rounded-xl shadow-xl shadow-indigo-600/25 transition flex items-center justify-center gap-2 text-base cursor-pointer disabled:opacity-50"
        >
          {loading ? <span>Saving Profile...</span> : <><span>Save Profile & View Dashboard</span><ArrowRight className="w-5 h-5" /></>}
        </button>
      </form>
    </div>
  );
};
