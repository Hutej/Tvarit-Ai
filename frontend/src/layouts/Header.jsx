import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Sun, Moon } from 'lucide-react';

const META = {
  '/':           { title: 'New Request', sub: 'Upload documentation and select a procedure' },
  '/processing': { title: 'Analyzing', sub: 'AI pipeline running — please wait' },
};

export default function Header() {
  const { pathname } = useLocation();
  const meta = META[pathname] ||
    (pathname.startsWith('/dashboard/') ? { title: 'Authorization Report', sub: 'Prior authorization readiness analysis' } : { title: '', sub: '' });

  // Default to dark theme to preserve original experience
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark');

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return (
    <header className="fixed top-0 right-0 z-30 flex items-center px-5 border-b"
      style={{
        left: 'var(--sidebar-width)',
        height: 'var(--header-height)',
        background: 'hsl(var(--background) / 0.8)',
        borderColor: 'hsl(var(--border))',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        transition: 'background-color 0.15s, border-color 0.15s',
      }}>
      <div>
        <h1 className="text-sm font-semibold" style={{ color: 'hsl(var(--foreground))', letterSpacing: '-0.01em' }}>
          {meta.title}
        </h1>
        {meta.sub && (
          <p className="text-[11.5px] mt-px" style={{ color: 'hsl(var(--muted-foreground))' }}>{meta.sub}</p>
        )}
      </div>

      <div className="ml-auto flex items-center gap-3">
        {/* Theme Toggle Button */}
        <button
          type="button"
          onClick={toggleTheme}
          className="flex items-center justify-center w-7 h-7 rounded-md border transition-colors"
          style={{
            background: 'hsl(var(--card))',
            borderColor: 'hsl(var(--border))',
            color: 'hsl(var(--foreground))',
            cursor: 'pointer',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.background = 'hsl(var(--highlight))';
            e.currentTarget.style.borderColor = 'hsl(var(--border-strong))';
          }}
          onMouseLeave={e => {
            e.currentTarget.style.background = 'hsl(var(--card))';
            e.currentTarget.style.borderColor = 'hsl(var(--border))';
          }}
        >
          {theme === 'dark' ? <Sun size={13} /> : <Moon size={13} />}
        </button>

        {/* API Status Pill */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-[11px] font-medium"
          style={{ background: 'hsl(var(--highlight))', borderColor: 'hsl(var(--border))', color: 'hsl(var(--muted-foreground))' }}>
          <span className="w-1.5 h-1.5 rounded-full" style={{ background: 'hsl(var(--success))', boxShadow: '0 0 5px hsl(var(--success) / 0.6)' }} />
          API Live
        </div>
      </div>
    </header>
  );
}
