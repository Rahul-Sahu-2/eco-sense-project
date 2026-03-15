import { NavLink, useNavigate } from 'react-router-dom';

export default function Sidebar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/auth');
  };

  const navItems = [
    { to: '/',           icon: '🔬', label: 'AI Detection' },
    { to: '/report',     icon: '📤', label: 'Report & Earn' },
    { to: '/admin',      icon: '📊', label: 'Dashboard' },
  ];

  const stats = [
    { icon: '🎯', val: '92%',     lbl: 'Accuracy' },
    { icon: '📦', val: '15+',     lbl: 'Classes' },
    { icon: '⚡', val: 'Live',    lbl: 'Detection' },
    { icon: '💎', val: 'Polygon', lbl: 'Network' },
  ];

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="logo-box">♻️</div>
        <div>
          <div className="logo-text">EcoSense</div>
          <div className="logo-sub">AI · Blockchain · Green</div>
        </div>
      </div>

      {/* Navigation */}
      <p className="sidebar-label">Menu</p>
      <nav className="sidebar-nav">
        {navItems.map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
        
        {!token ? (
          <NavLink to="/auth" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
            <span className="nav-icon">🔑</span>
            Login
          </NavLink>
        ) : (
          <button onClick={handleLogout} className="nav-link" style={{ width: '100%', textAlign: 'left', border: 'none', background: 'none' }}>
            <span className="nav-icon">🚪</span>
            Logout
          </button>
        )}
      </nav>

      <hr className="sidebar-divider" />

      {/* Stats */}
      <p className="sidebar-label">System</p>
      <div className="sidebar-stats">
        {stats.map(s => (
          <div className="stat-item" key={s.lbl}>
            <span className="stat-icon">{s.icon}</span>
            <div>
              <div className="stat-val">{s.val}</div>
              <div className="stat-lbl">{s.lbl}</div>
            </div>
          </div>
        ))}
      </div>

      <hr className="sidebar-divider" />
      <p className="sidebar-footer">YOLOv8 · Groq · Polygon</p>
    </aside>
  );
}
