import { NavLink } from 'react-router-dom';
import { FilePlus, History, Settings, Activity } from 'lucide-react';
import { cn } from '../utils/helpers';

const nav = [
  { to: '/', icon: FilePlus, label: 'New Request', end: true },
  { to: '/history', icon: History, label: 'History', disabled: true },
  { to: '/settings', icon: Settings, label: 'Settings', disabled: true },
];

export default function Sidebar() {
  return (
    <aside
      className="fixed inset-y-0 left-0 z-40 flex flex-col"
      style={{ width: 'var(--sidebar-width)' }}
    >
      <div
        className="absolute inset-0 border-r"
        style={{ background: 'hsl(var(--sidebar-bg))', borderColor: 'hsl(var(--border))' }}
      />

      <div className="relative flex flex-col h-full px-3 py-4 gap-6">
        {/* Logo */}
        <div className="flex items-center gap-2 px-1.5 pt-1">
          <div
            className="flex items-center justify-center w-6 h-6 rounded-md"
            style={{ background: 'hsl(var(--highlight))', border: '1px solid hsl(var(--border-strong))' }}
          >
            <Activity size={12} style={{ color: 'hsl(var(--foreground))' }} strokeWidth={2.5} />
          </div>
          <span className="text-sm font-semibold tracking-tight" style={{ color: 'hsl(var(--foreground))' }}>
            Tvarit<span style={{ color: 'hsl(var(--muted-foreground))' }}> AI</span>
          </span>
        </div>

        {/* Nav */}
        <nav className="flex flex-col gap-0.5 flex-1">
          <p className="px-1.5 mb-1 text-[10px] font-semibold uppercase tracking-[0.1em]"
            style={{ color: 'hsl(var(--muted-foreground))', opacity: 0.55 }}>
            Workspace
          </p>
          {nav.map(({ to, icon: Icon, label, end, disabled }) =>
            disabled ? (
              <div key={to} className="nav-item opacity-30 cursor-not-allowed">
                <Icon size={13} strokeWidth={1.75} />
                <span className="flex-1">{label}</span>
                <span style={{ fontSize: '0.6rem', letterSpacing: '0.08em', color: 'hsl(var(--muted-foreground))' }}>SOON</span>
              </div>
            ) : (
              <NavLink
                key={to} to={to} end={end}
                className={({ isActive }) => cn('nav-item', isActive && 'active')}
              >
                <Icon size={13} strokeWidth={1.75} />
                <span>{label}</span>
              </NavLink>
            )
          )}
        </nav>

        {/* User chip */}
        <div className="border-t pt-3" style={{ borderColor: 'hsl(var(--border))' }}>
          <div className="flex items-center gap-2 px-1.5 py-2 rounded-md"
            style={{ background: 'hsl(var(--highlight))' }}>
            <div className="flex items-center justify-center w-5 h-5 rounded text-[10px] font-bold flex-shrink-0"
              style={{ background: 'hsl(var(--border-strong))', color: 'hsl(var(--foreground))' }}>
              PA
            </div>
            <div className="min-w-0">
              <p className="text-xs font-medium truncate" style={{ color: 'hsl(var(--foreground))' }}>PA Specialist</p>
              <p className="text-[11px] truncate" style={{ color: 'hsl(var(--muted-foreground))' }}>Clinical Review</p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
