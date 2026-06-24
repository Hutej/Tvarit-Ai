import { AlertTriangle, CheckCircle2, FileX2, ChevronRight } from 'lucide-react';
import { EVIDENCE_CATEGORY_LABELS } from '../../../constants/index';

const categoryIcon = {
  IMAGING: '🩻',
  DIAGNOSIS: '🏥',
  LAB_RESULT: '🧪',
  MEDICATION: '💊',
  CONSERVATIVE_TREATMENT: '🩹',
  CLINICAL_FINDING: '📋',
  DOCUMENT: '📄',
  PROVIDER_TYPE: '👨‍⚕️',
  INSURANCE: '🛡️',
};

export default function MissingEvidencePanel({ items = [], recommendations = [] }) {
  if (items.length === 0 && recommendations.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-10 text-center gap-3">
        <CheckCircle2 size={28} style={{ color: 'hsl(var(--success))' }} />
        <div>
          <p className="text-sm font-semibold" style={{ color: 'hsl(var(--foreground))' }}>No Gaps Detected</p>
          <p className="text-xs mt-0.5" style={{ color: 'hsl(var(--muted-foreground))' }}>All required evidence is present</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Next Best Actions */}
      {recommendations.length > 0 && (
        <div>
          <p className="text-[10.5px] font-semibold uppercase tracking-[0.1em] mb-2"
            style={{ color: 'hsl(var(--muted-foreground))' }}>
            Next Best Actions
          </p>
          <ol className="flex flex-col gap-1.5">
            {recommendations.map((rec, i) => (
              <li key={i}
                className="flex items-start gap-2.5 px-3 py-2.5 rounded-md border text-xs"
                style={{ background: 'hsl(var(--surface-1))', borderColor: 'hsl(var(--border))' }}>
                <span className="flex-shrink-0 flex items-center justify-center w-4 h-4 rounded text-[10px] font-bold mt-px"
                  style={{ background: 'hsl(var(--highlight))', color: 'hsl(var(--muted-foreground))' }}>
                  {i + 1}
                </span>
                <span style={{ color: 'hsl(var(--foreground))', lineHeight: 1.5 }}>{rec}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Missing Evidence */}
      {items.length > 0 && (
        <div>
          <p className="text-[10.5px] font-semibold uppercase tracking-[0.1em] mb-2"
            style={{ color: 'hsl(var(--muted-foreground))' }}>
            Missing Evidence — {items.length} gap{items.length !== 1 ? 's' : ''}
          </p>
          <div className="flex flex-col gap-1.5">
            {items.map((item, i) => (
              <div key={i}
                className="flex items-start gap-3 px-3 py-2.5 rounded-md border text-xs"
                style={{
                  background: 'hsl(var(--danger-muted, 0 72% 51% / 0.06))',
                  borderColor: 'hsl(0 72% 51% / 0.18)',
                }}>
                <div className="flex-shrink-0 mt-0.5">
                  <FileX2 size={13} style={{ color: 'hsl(0 72% 62%)' }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5 mb-0.5">
                    <span className="text-[10px]">{categoryIcon[item.category] || '📌'}</span>
                    <span className="text-[10px] font-semibold uppercase tracking-wide"
                      style={{ color: 'hsl(0 72% 62%)' }}>
                      {EVIDENCE_CATEGORY_LABELS[item.category] || item.category}
                    </span>
                  </div>
                  <p className="font-medium" style={{ color: 'hsl(var(--foreground))' }}>{item.requirement}</p>
                  {item.reason && (
                    <p className="mt-0.5 text-[11px]" style={{ color: 'hsl(var(--muted-foreground))' }}>{item.reason}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
