import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { getAdminReports, getAdminStats, downloadReportsCSV } from '../api/api';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

function createColorIcon(color) {
  const hue = color === 'red' ? 0 : color === 'orange' ? 30 : 120;
  return new L.Icon({
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41],
    className: `marker-hue-${hue}`,
  });
}

function wasteColor(w) { return w > 80 ? '#ef4444' : w > 50 ? '#f59e0b' : '#22c55e'; }
function wasteLabel(w) { return w > 80 ? 'High' : w > 50 ? 'Medium' : 'Low'; }

export default function AdminPanel() {
  const [reports, setReports] = useState([]);
  const [stats, setStats] = useState({ total: 0, high: 0, medium: 0, low: 0, avg_waste: 0 });
  const [loading, setLoading] = useState(true);
  const currentUser = localStorage.getItem('user') || 'Admin';

  useEffect(() => {
    const load = async () => {
      try {
        const [r, s] = await Promise.all([getAdminReports(), getAdminStats()]);
        setReports(r.data.reports || []);
        setStats(s.data);
      } catch (err) { console.error('Failed to load:', err); }
      setLoading(false);
    };
    load();
  }, []);

  const markerStyle = `
    .marker-hue-0 { filter: hue-rotate(-40deg) saturate(2) brightness(1.1); }
    .marker-hue-30 { filter: hue-rotate(-10deg) saturate(1.5); }
    .marker-hue-120 { filter: hue-rotate(80deg) saturate(1.5); }
    .leaflet-container { background: #f8fafc; border-radius: 20px; }
  `;

  return (
    <div className="admin-page fade-in">
      <style>{markerStyle}</style>

      {/* Header Section */}
      <div className="admin-header glass-card">
        <div className="header-left">
          <div className="status-badge">
            <span className="dot pulse"></span>
            LIVE MONITORING
          </div>
          <h1>Satellite Command Center</h1>
          <p>Real-time waste detection and urban hygiene analytics</p>
        </div>
        <div className="header-right">
          <div className="user-profile">
            <div className="user-info">
              <span className="user-name">{currentUser}</span>
              <span className="user-role">Authorized Access</span>
            </div>
            <div className="user-avatar">{currentUser[0]}</div>
          </div>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="metrics-row">
        <div className="metric-card blue">
          <span className="metric-icon">📊</span>
          <div className="metric-val">{stats.total}</div>
          <div className="metric-lbl">Total Reports</div>
        </div>
        <div className="metric-card red">
          <span className="metric-icon">🚨</span>
          <div className="metric-val">{stats.high}</div>
          <div className="metric-lbl">High Priority</div>
        </div>
        <div className="metric-card amber">
          <span className="metric-icon">⚠️</span>
          <div className="metric-val">{stats.medium}</div>
          <div className="metric-lbl">Medium Alert</div>
        </div>
        <div className="metric-card green">
          <span className="metric-icon">✅</span>
          <div className="metric-val">{stats.low}</div>
          <div className="metric-lbl">Clear Zones</div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="admin-main-grid">
        {/* Sidebar: Reports List */}
        <div className="admin-sidebar glass-card">
          <div className="sidebar-title">
            <span>Recent Incidents</span>
            <a href={downloadReportsCSV()} download className="csv-link">
              Export CSV
            </a>
          </div>

          <div className="reports-list-container">
            {loading ? (
              <div className="loading-state">
                <span className="spinner"></span>
                <p>Syncing data...</p>
              </div>
            ) : reports.length === 0 ? (
              <div className="empty-state">No active incidents detected.</div>
            ) : (
              reports.map((r, i) => {
                const w = r.waste_percent || 0;
                const clr = wasteColor(w);
                return (
                  <div className="incident-item" key={i}>
                    <div className="incident-marker" style={{ background: clr }}></div>
                    <div className="incident-details">
                      <div className="incident-name">{r.name || `Unit ${i + 1}`}</div>
                      <div className="incident-loc">
                        {r.lat ? Number(r.lat).toFixed(4) : '—'}, {r.lon ? Number(r.lon).toFixed(4) : '—'}
                      </div>
                    </div>
                    <div className="incident-badge" style={{ color: clr, background: `${clr}15` }}>
                      {w}%
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Center: Map Display */}
        <div className="admin-map-container glass-card">
          <MapContainer 
            center={[23.2599, 77.4126]} 
            zoom={12} 
            style={{ height: '100%', minHeight: 600 }}
            scrollWheelZoom={true}
          >
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://carto.com/">CARTO</a>'
            />
            {reports.filter(r => r.lat && r.lon).map((r, i) => {
              const w = r.waste_percent || 0;
              const color = w > 80 ? 'red' : w > 50 ? 'orange' : 'green';
              return (
                <Marker key={i} position={[Number(r.lat), Number(r.lon)]} icon={createColorIcon(color)}>
                  <Popup>
                    <div className="map-popup">
                      <h3>Waste Report</h3>
                      <div className="popup-row"><span>Unit:</span> {r.name || '—'}</div>
                      <div className="popup-row"><span>Impact:</span> {w}%</div>
                      <div className="popup-row"><span>Type:</span> {r.waste_type || '—'}</div>
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </div>
      </div>

      <style>{`
        .admin-page {
          padding-top: 1rem;
        }

        .admin-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
          padding: 2rem 2.5rem;
        }

        .header-left h1 {
          font-family: var(--f-display);
          font-size: 2.2rem;
          font-weight: 800;
          margin: 0.5rem 0;
          color: #fff;
        }

        .header-left p {
          color: var(--text-3);
          font-size: 0.95rem;
        }

        .status-badge {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          font-size: 0.65rem;
          font-weight: 700;
          letter-spacing: 2px;
          color: var(--accent-3);
          background: rgba(6,182,212,0.1);
          padding: 0.4rem 1rem;
          border-radius: var(--r-full);
        }

        .dot.pulse {
          width: 8px;
          height: 8px;
          background: var(--accent-3);
          border-radius: 50%;
          box-shadow: 0 0 10px var(--accent-3);
          animation: statusPulse 2s infinite;
        }

        @keyframes statusPulse {
          0% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.4); opacity: 0.5; }
          100% { transform: scale(1); opacity: 1; }
        }

        .user-profile {
          display: flex;
          align-items: center;
          gap: 15px;
          background: rgba(255,255,255,0.03);
          padding: 0.6rem 1.2rem;
          border-radius: var(--r-xl);
          border: 1px solid var(--border-1);
        }

        .user-info {
          text-align: right;
        }

        .user-name {
          display: block;
          font-weight: 700;
          font-size: 0.95rem;
          color: #fff;
        }

        .user-role {
          font-size: 0.7rem;
          color: var(--text-4);
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .user-avatar {
          width: 42px;
          height: 42px;
          background: var(--grad-aurora);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 800;
          color: #fff;
          font-size: 1.2rem;
        }

        .admin-main-grid {
          display: grid;
          grid-template-columns: 350px 1fr;
          gap: 1.5rem;
          min-height: 600px;
        }

        .admin-sidebar {
          display: flex;
          flex-direction: column;
          padding: 1.8rem;
        }

        .sidebar-title {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-family: var(--f-display);
          font-weight: 700;
          font-size: 1.1rem;
          margin-bottom: 2rem;
          color: #fff;
        }

        .csv-link {
          font-size: 0.75rem;
          color: var(--accent-3);
          text-decoration: none;
          font-weight: 600;
        }

        .reports-list-container {
          flex: 1;
          overflow-y: auto;
          margin-right: -10px;
          padding-right: 10px;
        }

        .incident-item {
          display: flex;
          align-items: center;
          gap: 15px;
          padding: 1rem;
          background: rgba(255,255,255,0.02);
          border: 1px solid var(--border-1);
          border-radius: var(--r-lg);
          margin-bottom: 0.8rem;
          transition: all 0.2s;
          cursor: pointer;
        }

        .incident-item:hover {
          background: rgba(255,255,255,0.05);
          border-color: var(--border-glow);
          transform: translateX(5px);
        }

        .incident-marker {
          width: 8px;
          height: 35px;
          border-radius: var(--r-full);
          flex-shrink: 0;
        }

        .incident-details {
          flex: 1;
        }

        .incident-name {
          font-size: 0.95rem;
          font-weight: 600;
          color: #fff;
          margin-bottom: 2px;
        }

        .incident-loc {
          font-size: 0.75rem;
          color: var(--text-4);
          font-family: var(--f-mono);
        }

        .incident-badge {
          padding: 0.35rem 0.6rem;
          border-radius: 8px;
          font-size: 0.75rem;
          font-weight: 800;
        }

        .admin-map-container {
          padding: 1rem;
          overflow: hidden;
        }

        .map-popup h3 {
          margin: 0 0 10px;
          font-family: var(--f-display);
          font-size: 1rem;
          color: #1e293b;
        }

        .popup-row {
          font-size: 0.85rem;
          color: #475569;
          margin-bottom: 4px;
        }

        .popup-row span {
          font-weight: 600;
          color: #1e293b;
        }

        .loading-state, .empty-state {
          text-align: center;
          padding: 3rem 1rem;
          color: var(--text-4);
        }

        @media (max-width: 1200px) {
          .admin-main-grid { grid-template-columns: 1fr; }
          .admin-sidebar { order: 2; height: 500px; }
          .admin-map-container { order: 1; }
        }
      `}</style>
    </div>
  );
}
