import { useState } from 'react';
import { CheckCircle2, ChevronDown } from 'lucide-react';
import { cn } from '../../../utils/helpers';
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

function groupByCategory(items) {
  return items.reduce((acc, item) => {
    const key = item.category;
    if (!acc[key]) acc[key] = [];
    acc[key].push(item);
    return acc;
  }, {});
}

function AccordionItem({ category, items, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  const label = EVIDENCE_CATEGORY_LABELS[category] || category;
  const icon = categoryIcon[category] || '📌';

  return (
    <div className="border rounded-md overflow-hidden" style={{ borderColor: 'hsl(var(--border))' }}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center gap-2.5 px-3 py-2.5 text-left transition-colors"
        style={{ background: open ? 'hsl(var(--surface-1))' : 'hsl(var(--card))' }}
        onMouseEnter={e => { if (!open) e.currentTarget.style.background = 'hsl(var(--muted))'; }}
        onMouseLeave={e => { if (!open) e.currentTarget.style.background = 'hsl(var(--card))'; }}
      >
        <span className="text-sm">{icon}</span>
        <span className="flex-1 text-xs font-semibold" style={{ color: 'hsl(var(--foreground))' }}>
          {label}
        </span>
        <span className="text-[10px] font-medium px-1.5 py-0.5 rounded"
          style={{ background: 'hsl(var(--success) / 0.12)', color: 'hsl(var(--success))' }}>
          {items.length}
        </span>
        <ChevronDown
          size={13}
          className={cn('transition-transform duration-200', open && 'rotate-180')}
          style={{ color: 'hsl(var(--muted-foreground))' }}
        />
      </button>

      {open && (
        <div className="border-t" style={{ borderColor: 'hsl(var(--border))' }}>
          {items.map((item, i) => (
            <div
              key={i}
              className={cn('flex items-start gap-3 px-3 py-2.5 text-xs', i > 0 && 'border-t')}
              style={{ borderColor: 'hsl(var(--border))' }}
            >
              <CheckCircle2
                size={13}
                className="flex-shrink-0 mt-0.5"
                style={{ color: 'hsl(var(--success))' }}
              />
              <div className="flex-1 min-w-0">
                <p className="font-medium" style={{ color: 'hsl(var(--foreground))' }}>
                  {item.requirement}
                </p>
                {item.matched_value && (
                  <p className="mt-1 text-[11px] leading-relaxed px-2 py-1.5 rounded"
                    style={{
                      background: 'hsl(var(--muted))',
                      color: 'hsl(var(--muted-foreground))',
                      fontStyle: 'italic',
                    }}>
                    "{item.matched_value}"
                  </p>
                )}
                {item.reason && !item.matched_value && (
                  <p className="mt-0.5 text-[11px]" style={{ color: 'hsl(var(--muted-foreground))' }}>
                    {item.reason}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function EvidenceAccordion({ items = [] }) {
  if (items.length === 0) {
    return (
      <div className="py-8 text-center text-xs" style={{ color: 'hsl(var(--muted-foreground))' }}>
        No matched evidence to display
      </div>
    );
  }

  const grouped = groupByCategory(items);
  const categories = Object.keys(grouped);

  return (
    <div className="flex flex-col gap-1.5">
      {categories.map((cat, i) => (
        <AccordionItem
          key={cat}
          category={cat}
          items={grouped[cat]}
          defaultOpen={i === 0}
        />
      ))}
    </div>
  );
}
