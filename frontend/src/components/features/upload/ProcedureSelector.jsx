import { useState } from 'react';
import { Check, ChevronDown, Search } from 'lucide-react';
import { PROCEDURES } from '../../../constants/index';
import { cn } from '../../../utils/helpers';

export default function ProcedureSelector({ value, onChange }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');

  const selected = PROCEDURES.find((p) => p.value === value);
  const filtered = query.trim()
    ? PROCEDURES.filter(p => p.label.toLowerCase().includes(query.toLowerCase()) || p.value.includes(query))
    : PROCEDURES;

  const pick = (p) => { onChange(p); setOpen(false); setQuery(''); };

  return (
    <div className="relative">
      <button type="button" onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-md border text-left transition-all duration-100"
        style={{
          background: 'hsl(var(--input))',
          borderColor: open ? 'hsl(var(--border-strong))' : 'hsl(var(--border))',
          boxShadow: open ? '0 0 0 1px hsl(var(--border-strong))' : 'none',
        }}>
        <div className="flex-1 min-w-0">
          {selected ? (
            <>
              <p className="text-sm font-medium truncate" style={{ color: 'hsl(var(--foreground))' }}>{selected.label}</p>
              <p className="text-[11px]" style={{ color: 'hsl(var(--muted-foreground))' }}>CPT {selected.value}</p>
            </>
          ) : (
            <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Search by name or CPT code…</p>
          )}
        </div>
        <ChevronDown size={13} className={cn('flex-shrink-0 transition-transform duration-150', open && 'rotate-180')}
          style={{ color: 'hsl(var(--muted-foreground))' }} />
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute z-20 w-full mt-1 rounded-md border overflow-hidden"
            style={{ background: 'hsl(var(--popover))', borderColor: 'hsl(var(--border-strong))', boxShadow: '0 20px 60px hsl(0 0% 0% / 0.6)' }}>
            <div className="flex items-center gap-2 px-3 py-2 border-b" style={{ borderColor: 'hsl(var(--border))' }}>
              <Search size={12} style={{ color: 'hsl(var(--muted-foreground))' }} />
              <input autoFocus type="text" placeholder="Search…" value={query}
                onChange={e => setQuery(e.target.value)}
                className="flex-1 bg-transparent text-sm outline-none"
                style={{ color: 'hsl(var(--foreground))' }} />
            </div>
            <ul className="max-h-48 overflow-y-auto py-0.5">
              {filtered.length === 0 ? (
                <li className="py-6 text-center text-xs" style={{ color: 'hsl(var(--muted-foreground))' }}>No results</li>
              ) : filtered.map(p => (
                <li key={p.value}>
                  <button type="button" onClick={() => pick(p)}
                    className="w-full flex items-center gap-3 px-3 py-2 text-left text-xs transition-colors"
                    style={{ background: p.value === value ? 'hsl(var(--highlight))' : 'transparent' }}
                    onMouseEnter={e => { if (p.value !== value) e.currentTarget.style.background = 'hsl(var(--muted))'; }}
                    onMouseLeave={e => { if (p.value !== value) e.currentTarget.style.background = 'transparent'; }}>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate" style={{ color: 'hsl(var(--foreground))' }}>{p.label}</p>
                      <p style={{ color: 'hsl(var(--muted-foreground))' }}>CPT {p.value}</p>
                    </div>
                    {p.value === value && <Check size={12} style={{ color: 'hsl(var(--foreground))' }} />}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
