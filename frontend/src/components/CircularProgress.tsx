import React from 'react';

interface CircularProgressProps {
  percentage: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
  sublabel?: string;
}

export const CircularProgress: React.FC<CircularProgressProps> = ({
  percentage,
  size = 180,
  strokeWidth = 14,
  label = 'Requirement Match',
  sublabel = 'Employability Match Index'
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  // Determine color theme based on score
  let colorClass = 'stroke-emerald-400';
  let textClass = 'text-emerald-400';
  if (percentage < 50) {
    colorClass = 'stroke-rose-500';
    textClass = 'text-rose-400';
  } else if (percentage < 75) {
    colorClass = 'stroke-amber-400';
    textClass = 'text-amber-400';
  }

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
        <svg className="transform -rotate-90" width={size} height={size}>
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className="stroke-slate-800"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className={`transition-all duration-1000 ease-out ${colorClass}`}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className={`text-4xl font-extrabold tracking-tight ${textClass}`}>
            {Math.round(percentage)}%
          </span>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mt-1">
            {label}
          </span>
        </div>
      </div>
      {sublabel && <p className="text-xs text-slate-400 mt-2 font-medium">{sublabel}</p>}
    </div>
  );
};
