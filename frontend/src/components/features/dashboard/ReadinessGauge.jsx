import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const getColor = (score) => {
  if (score >= 90) return 'hsl(142 69% 43%)';
  if (score >= 70) return 'hsl(38 92% 50%)';
  if (score >= 50) return 'hsl(25 95% 53%)';
  return 'hsl(0 72% 51%)';
};

const getLabel = (score) => {
  if (score >= 90) return { text: 'Ready', color: 'hsl(142 69% 52%)' };
  if (score >= 70) return { text: 'Near Ready', color: 'hsl(38 92% 58%)' };
  if (score >= 50) return { text: 'Incomplete', color: 'hsl(25 95% 62%)' };
  return { text: 'Critical', color: 'hsl(0 72% 62%)' };
};

export default function ReadinessGauge({ score = 0 }) {
  const color = getColor(score);
  const label = getLabel(score);
  const data = [
    { value: score },
    { value: 100 - score },
  ];

  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative" style={{ width: 140, height: 78 }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="100%"
              startAngle={180}
              endAngle={0}
              innerRadius={50}
              outerRadius={68}
              dataKey="value"
              stroke="none"
              strokeWidth={0}
            >
              <Cell fill={color} />
              <Cell fill="hsl(var(--border-strong))" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        {/* Score overlay */}
        <div className="absolute inset-x-0 bottom-0 flex flex-col items-center" style={{ bottom: -2 }}>
          <span className="text-2xl font-bold tabular-nums" style={{ color: 'hsl(var(--foreground))', letterSpacing: '-0.03em' }}>
            {score}
          </span>
        </div>
      </div>
      <div className="flex items-center gap-1.5 mt-1">
        <span className="text-[11px] font-semibold" style={{ color: label.color }}>{label.text}</span>
        <span className="text-[11px]" style={{ color: 'hsl(var(--muted-foreground))' }}>/ 100</span>
      </div>
    </div>
  );
}
