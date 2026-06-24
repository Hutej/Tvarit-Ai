import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function MainLayout() {
  return (
    <div className="min-h-screen" style={{ background: 'hsl(var(--background))' }}>
      <Sidebar />
      <Header />
      <main
        className="flex flex-col min-h-screen"
        style={{
          marginLeft: 'var(--sidebar-width)',
          paddingTop: 'var(--header-height)',
        }}
      >
        <div className="flex-1 p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
