import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, User, Stethoscope, AlertTriangle, CheckCircle2, BarChart3 } from 'lucide-react';
import { useDashboard } from '../hooks/useWorkflow';
import ReadinessGauge from '../components/features/dashboard/ReadinessGauge';
import MissingEvidencePanel from '../components/features/dashboard/MissingEvidencePanel';
import EvidenceAccordion from '../components/features/dashboard/EvidenceAccordion';

/* ── Helpers ── */
const RISK_CLASS = {
  LOW:      'risk-low',
  MEDIUM:   'risk-medium',
  HIGH:     'risk-high',
  CRITICAL: 'risk-critical',
};

function RiskBadge({ level = 'CRITICAL' }) {
  return (
    <span className={`risk-badge text-[10.5px] font-semibold px-2 py-0.5 rounded-full ${RISK_CLASS[level] || 'risk-critical'}`}>
      {level}
    </span>
  );
}

/* ── Skeleton ── */
function DashboardSkeleton() {
  return (
    <div className="space-y-4 animate-pulse">
      <div className="skeleton h-16 rounded-lg" />
      <div className="grid grid-cols-3 gap-3">
        {[...Array(3)].map((_, i) => <div key={i} className="skeleton h-32 rounded-lg" />)}
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="skeleton h-72 rounded-lg" />
        <div className="skeleton h-72 rounded-lg" />
      </div>
    </div>
  );
}

/* ── Mock data for demo / no backend ── */
const MOCK = {
  authorization_id: 'demo',
  patient_name: 'John Doe',
  procedure_name: 'MRI Lumbar Spine without contrast',
  readiness_score: 65,
  risk_level: 'HIGH',
  completion_percentage: 71.4,
  matched_evidence: [
    { category: 'DIAGNOSIS', requirement: 'Low Back Pain (M54.5)', status: 'MATCHED', matched_value: 'Patient presents with severe low back pain radiating to left leg.', reason: 'Exact match found in clinical notes.' },
    { category: 'DIAGNOSIS', requirement: 'Radiculopathy / Sciatica (M54.4)', status: 'MATCHED', matched_value: 'Sciatica confirmed via straight leg raise test.', reason: 'Clinical finding confirmed.' },
    { category: 'CONSERVATIVE_TREATMENT', requirement: 'Physical Therapy ≥ 6 weeks', status: 'MATCHED', matched_value: 'Patient completed 8 weeks of PT with minimal improvement.', reason: 'Duration meets payer threshold.' },
    { category: 'CONSERVATIVE_TREATMENT', requirement: 'NSAIDs trial and failure', status: 'MATCHED', matched_value: 'Naproxen 500mg — failed, GI intolerance reported.', reason: 'Step therapy documented.' },
    { category: 'PROVIDER_TYPE', requirement: 'Referral from Primary Care Physician', status: 'MATCHED', matched_value: 'Dr. Sarah Williams, MD — referral dated 2026-06-10.', reason: null },
  ],
  missing_evidence: [
    { category: 'IMAGING', requirement: 'X-Ray Lumbar Spine (within 6 months)', status: 'MISSING', matched_value: null, reason: 'Found X-Ray from 14 months ago — payer requires within 6 months.' },
    { category: 'LAB_RESULT', requirement: 'Recent CBC (within 30 days)', status: 'MISSING', matched_value: null, reason: 'No lab results found in uploaded documentation.' },
  ],
  recommendations: [
    'Upload a recent Lumbar Spine X-Ray (taken within the last 6 months)',
    'Attach a CBC lab result dated within the last 30 days',
  ],
  summary: 'Submission is 65% ready. Two critical items are missing: recent imaging and a CBC lab result. Address these before submission to avoid denial.',
};

/* ── Main component ── */
export default function DashboardPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isDemo = id === 'demo';

  const { data: apiData, isLoading, isError, error } = useDashboard(isDemo ? null : id);
  const data = isDemo ? MOCK : apiData;

  if (isLoading) return (
    <div className="max-w-5xl mx-auto pt-2 pb-12"><DashboardSkeleton /></div>
  );

  if (isError) return (
    <div className="max-w-5xl mx-auto pt-2 pb-12">
      <div className="surface p-8 text-center space-y-4">
        <AlertTriangle size={28} style={{ color: 'hsl(var(--warning))', margin: '0 auto' }} />
        <div>
          <p className="text-sm font-semibold" style={{ color: 'hsl(var(--foreground))' }}>Failed to load dashboard</p>
          <p className="text-xs mt-1" style={{ color: 'hsl(var(--muted-foreground))' }}>
            {error?.userMessage || 'Could not retrieve authorization data.'}
          </p>
        </div>
        <button onClick={() => navigate('/')}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-md border text-xs font-medium"
          style={{ background: 'hsl(var(--highlight))', borderColor: 'hsl(var(--border))', color: 'hsl(var(--foreground))' }}>
          <ArrowLeft size={12} /> New Request
        </button>
      </div>
    </div>
  );

  if (!data) return null;

  const totalEvidence = (data.matched_evidence?.length || 0) + (data.missing_evidence?.length || 0);
  const matchedCount = data.matched_evidence?.length || 0;
  const missingCount = data.missing_evidence?.length || 0;

  return (
    <div className="max-w-5xl mx-auto pt-1 pb-12">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="space-y-4"
      >
        {/* ── Patient Header Bar ── */}
        <div className="surface flex items-center gap-4 px-4 py-3">
          <button onClick={() => navigate('/')}
            className="flex-shrink-0 flex items-center justify-center w-7 h-7 rounded-md border transition-colors"
            style={{ background: 'hsl(var(--muted))', borderColor: 'hsl(var(--border))' }}
            onMouseEnter={e => e.currentTarget.style.background = 'hsl(var(--highlight))'}
            onMouseLeave={e => e.currentTarget.style.background = 'hsl(var(--muted))'}>
            <ArrowLeft size={12} style={{ color: 'hsl(var(--muted-foreground))' }} />
          </button>

          <div className="flex items-center gap-2 flex-1 min-w-0">
            <div className="flex items-center gap-1.5">
              <User size={12} style={{ color: 'hsl(var(--muted-foreground))' }} />
              <span className="text-sm font-semibold" style={{ color: 'hsl(var(--foreground))' }}>{data.patient_name}</span>
            </div>
            <span style={{ color: 'hsl(var(--border-strong))' }}>·</span>
            <div className="flex items-center gap-1.5 min-w-0">
              <Stethoscope size={12} style={{ color: 'hsl(var(--muted-foreground))' }} />
              <span className="text-xs truncate" style={{ color: 'hsl(var(--muted-foreground))' }}>{data.procedure_name}</span>
            </div>
          </div>

          <RiskBadge level={data.risk_level} />
        </div>

        {/* ── Summary Cards Row ── */}
        <div className="grid grid-cols-3 gap-3">
          {/* Readiness Gauge */}
          <div className="surface p-4 flex flex-col items-center gap-1">
            <p className="text-[10.5px] font-semibold uppercase tracking-[0.1em] w-full"
              style={{ color: 'hsl(var(--muted-foreground))' }}>
              Readiness Score
            </p>
            <div className="flex-1 flex items-center justify-center py-1">
              <ReadinessGauge score={data.readiness_score} />
            </div>
          </div>

          {/* Risk Level */}
          <div className="surface p-4 flex flex-col gap-3">
            <p className="text-[10.5px] font-semibold uppercase tracking-[0.1em]"
              style={{ color: 'hsl(var(--muted-foreground))' }}>
              Risk Level
            </p>
            <div className="flex-1 flex flex-col justify-center gap-2">
              <RiskBadge level={data.risk_level} />
              <p className="text-xs leading-relaxed" style={{ color: 'hsl(var(--muted-foreground))' }}>
                {data.summary}
              </p>
            </div>
          </div>

          {/* Evidence completion */}
          <div className="surface p-4 flex flex-col gap-3">
            <p className="text-[10.5px] font-semibold uppercase tracking-[0.1em]"
              style={{ color: 'hsl(var(--muted-foreground))' }}>
              Criteria Coverage
            </p>
            <div className="flex-1 flex flex-col justify-center gap-3">
              {/* Progress bar */}
              <div>
                <div className="flex justify-between mb-1.5">
                  <span className="text-[11px]" style={{ color: 'hsl(var(--muted-foreground))' }}>Completion</span>
                  <span className="text-[11px] font-semibold tabular-nums" style={{ color: 'hsl(var(--foreground))' }}>
                    {data.completion_percentage?.toFixed(1)}%
                  </span>
                </div>
                <div className="h-1.5 rounded-full overflow-hidden" style={{ background: 'hsl(var(--muted))' }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{
                      background: data.completion_percentage >= 90 ? 'hsl(var(--success))'
                        : data.completion_percentage >= 70 ? 'hsl(var(--warning))'
                        : 'hsl(var(--danger))',
                    }}
                    initial={{ width: 0 }}
                    animate={{ width: `${data.completion_percentage}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}
                  />
                </div>
              </div>

              {/* Stats row */}
              <div className="grid grid-cols-2 gap-2">
                <div className="flex flex-col gap-0.5 px-2 py-1.5 rounded-md"
                  style={{ background: 'hsl(var(--success) / 0.08)' }}>
                  <div className="flex items-center gap-1">
                    <CheckCircle2 size={11} style={{ color: 'hsl(var(--success))' }} />
                    <span className="text-[10px] font-medium" style={{ color: 'hsl(var(--success))' }}>Matched</span>
                  </div>
                  <span className="text-lg font-bold tabular-nums" style={{ color: 'hsl(var(--foreground))' }}>{matchedCount}</span>
                </div>
                <div className="flex flex-col gap-0.5 px-2 py-1.5 rounded-md"
                  style={{ background: 'hsl(var(--danger) / 0.08)' }}>
                  <div className="flex items-center gap-1">
                    <AlertTriangle size={11} style={{ color: 'hsl(0 72% 62%)' }} />
                    <span className="text-[10px] font-medium" style={{ color: 'hsl(0 72% 62%)' }}>Missing</span>
                  </div>
                  <span className="text-lg font-bold tabular-nums" style={{ color: 'hsl(var(--foreground))' }}>{missingCount}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* ── Evidence Grid ── */}
        <div className="grid grid-cols-2 gap-3">
          {/* Left — Gaps + Actions */}
          <div className="surface flex flex-col">
            <div className="px-4 py-3 border-b" style={{ borderColor: 'hsl(var(--border))' }}>
              <div className="flex items-center gap-2">
                <AlertTriangle size={13} style={{ color: 'hsl(0 72% 62%)' }} />
                <span className="text-xs font-semibold" style={{ color: 'hsl(var(--foreground))' }}>Gaps & Actions</span>
                {missingCount > 0 && (
                  <span className="ml-auto text-[10px] font-semibold px-1.5 py-0.5 rounded"
                    style={{ background: 'hsl(var(--danger) / 0.12)', color: 'hsl(0 72% 62%)' }}>
                    {missingCount} missing
                  </span>
                )}
              </div>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              <MissingEvidencePanel
                items={data.missing_evidence || []}
                recommendations={data.recommendations || []}
              />
            </div>
          </div>

          {/* Right — Matched Evidence */}
          <div className="surface flex flex-col">
            <div className="px-4 py-3 border-b" style={{ borderColor: 'hsl(var(--border))' }}>
              <div className="flex items-center gap-2">
                <CheckCircle2 size={13} style={{ color: 'hsl(var(--success))' }} />
                <span className="text-xs font-semibold" style={{ color: 'hsl(var(--foreground))' }}>Matched Evidence</span>
                {matchedCount > 0 && (
                  <span className="ml-auto text-[10px] font-semibold px-1.5 py-0.5 rounded"
                    style={{ background: 'hsl(var(--success) / 0.12)', color: 'hsl(var(--success))' }}>
                    {matchedCount} verified
                  </span>
                )}
              </div>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              <EvidenceAccordion items={data.matched_evidence || []} />
            </div>
          </div>
        </div>

        {/* ── Footer meta ── */}
        <div className="flex items-center gap-2 px-1">
          <BarChart3 size={11} style={{ color: 'hsl(var(--muted-foreground))' }} />
          <p className="text-[11px]" style={{ color: 'hsl(var(--muted-foreground))' }}>
            {totalEvidence} criteria evaluated · Authorization ID:{' '}
            <span className="font-mono">{String(data.authorization_id).slice(0, 8)}…</span>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
