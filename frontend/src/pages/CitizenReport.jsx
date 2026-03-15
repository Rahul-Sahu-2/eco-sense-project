import { useState, useEffect } from 'react';
import { analyzeCitizenImage, submitCitizenReport, getCitizenConfig } from '../api/api';

export default function CitizenReport() {
  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);
  const [locError, setLocError] = useState('');
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [aiResult, setAiResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [name, setName] = useState('');
  const [wallet, setWallet] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState(null);

  // Load wallet from localStorage or .env config on mount
  useEffect(() => {
    const initWallet = async () => {
      const savedWallet = localStorage.getItem('user_wallet');
      if (savedWallet) {
        setWallet(savedWallet);
      } else {
        try {
          const res = await getCitizenConfig();
          if (res.data.default_wallet) {
            setWallet(res.data.default_wallet);
          }
        } catch (err) {
          console.error('Failed to fetch default wallet:', err);
        }
      }
    };
    
    initWallet();
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => { setLat(pos.coords.latitude); setLon(pos.coords.longitude); },
        () => setLocError('Allow location permission in your browser.'),
        { enableHighAccuracy: true }
      );
    } else {
      setLocError('Geolocation not supported.');
    }
  }, []);

  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        const selectedWallet = accounts[0];
        setWallet(selectedWallet);
        localStorage.setItem('user_wallet', selectedWallet);
      } catch (err) {
        console.error('Wallet connection failed:', err);
        alert('Failed to connect wallet. Please try again.');
      }
    } else {
      alert('MetaMask not found. Please install the MetaMask extension.');
    }
  };

  const handleFile = async (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setAiResult(null);
    setSubmitResult(null);
    setAnalyzing(true);
    try {
      const res = await analyzeCitizenImage(selected);
      setAiResult(res.data);
    } catch {
      setAiResult({ error: 'Analysis failed' });
    }
    setAnalyzing(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name) return alert('Enter your name');
    if (lat === null) return alert('Location not captured');
    if (!file) return alert('Upload an image');
    if (!aiResult || aiResult.error) return alert('AI result missing');
    if (!aiResult.is_waste) return alert('Image is not verified as waste');
    if (aiResult.waste_percent < 70) return alert('Waste confidence too low (min 70%)');

    try {
      const res = await submitCitizenReport({ name, waste_type: aiResult.waste_type, waste_percent: aiResult.waste_percent, lat, lon, wallet });
      setSubmitResult(res.data);
    } catch {
      setSubmitResult({ error: 'Submission failed' });
    }
    setSubmitting(false);
  };

  return (
    <div>
      {/* Hero */}
      <div className="hero-section">
        <div className="hero-eyebrow"><span className="dot"></span> Citizen Reporting</div>
        <h1 className="hero-title">
          Report Waste<br />
          <span className="hero-accent">& Earn Rewards</span>
        </h1>
        <p className="hero-subtitle">Upload a garbage photo, let AI verify it, and earn blockchain tokens as a reward for keeping Earth clean.</p>
      </div>

      {/* Step 1 */}
      <div className="citizen-step">
        <h3>Step 1 — Capture Location</h3>
        {lat !== null && lon !== null ? (
          <div className="location-success">✅ Location captured: {lat.toFixed(6)}, {lon.toFixed(6)}</div>
        ) : (
          <div className="location-warning">⏳ {locError || 'Detecting location...'}</div>
        )}
      </div>

      {/* Step 2 */}
      <div className="citizen-step">
        <h3>Step 2 — Upload Waste Photo</h3>
        <div className="analysis-grid">
          <div>
            <label className="file-upload" htmlFor="citizen-upload">
              <input id="citizen-upload" type="file" accept="image/*" onChange={handleFile} />
              <div style={{ fontSize: '2.5rem', marginBottom: '.5rem' }}>📸</div>
              <div style={{ fontWeight: 600 }}>{file ? file.name : 'Click to upload image'}</div>
              <div style={{ fontSize: '.75rem', marginTop: '.3rem', opacity: .5 }}>JPG, JPEG, PNG</div>
            </label>
            {preview && (
              <img src={preview} alt="Preview" style={{ marginTop: '1rem', width: '100%', borderRadius: '16px', border: '1px solid rgba(124,58,237,0.15)' }} />
            )}
          </div>

          <div>
            {analyzing && (
              <div className="res-card success"><span className="spinner"></span> AI analyzing image...</div>
            )}
            {aiResult && !aiResult.error && (
              <div className="fade-in">
                <div style={{ marginBottom: '1rem' }}>
                  <div className="conf-row"><span className="conf-label">Waste Confidence</span><span className="conf-value">{aiResult.waste_percent}%</span></div>
                  <div className="conf-bar-bg"><div className="conf-bar-fill waste" style={{ width: `${aiResult.waste_percent}%` }}></div></div>
                  <div className="conf-row"><span className="conf-label">Non-Waste</span><span className="conf-value">{aiResult.non_waste_percent}%</span></div>
                  <div className="conf-bar-bg"><div className="conf-bar-fill non-waste" style={{ width: `${aiResult.non_waste_percent}%` }}></div></div>
                </div>
                <div style={{ fontSize: '.9rem', color: 'var(--text-2)', lineHeight: 1.8 }}>
                  <div><b>Type:</b> {aiResult.waste_type}</div>
                  <div><b>Verified:</b> {aiResult.is_waste ? '✅ Waste Confirmed' : '❌ Not Waste'}</div>
                </div>
                <div style={{ marginTop: '1rem' }}>
                  <div className="prog-bar-bg" style={{ height: '8px', borderRadius: '4px' }}>
                    <div className="prog-bar-fill" style={{ width: `${aiResult.waste_percent}%`, borderRadius: '4px' }}></div>
                  </div>
                </div>
              </div>
            )}
            {aiResult && aiResult.error && (
              <div className="res-card error">
                <div className="res-title">❌ Analysis Failed</div>
                <p style={{ color: '#fca5a5' }}>{aiResult.error}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Step 3 */}
      <div className="citizen-step">
        <h3>Step 3 — Submit Report</h3>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '500px' }}>
          <div>
            <label className="input-label">Your Name</label>
            <input className="input-field" type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Enter your name" />
          </div>
          <div>
            <label className="input-label" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              Polygon Wallet
              <button type="button" onClick={connectWallet} className="auth-toggle" style={{ fontSize: '0.75rem', color: 'var(--accent-3)' }}>
                {wallet ? '🔄 Reconnect MetaMask' : '🦊 Connect MetaMask'}
              </button>
            </label>
            <input className="input-field" type="text" value={wallet} onChange={e => setWallet(e.target.value)} placeholder="0x..." />
          </div>
          <button className="btn-primary" type="submit" disabled={submitting} style={{ marginTop: '.5rem' }}>
            {submitting ? <><span className="spinner"></span> Submitting...</> : '📤 Submit Report'}
          </button>
        </form>

        {submitResult && !submitResult.error && (
          <div className="res-card success" style={{ maxWidth: 500 }}>
            <div className="res-title">✅ Report Submitted!</div>
            <hr className="res-divider" />
            <div style={{ fontSize: '.9rem', color: '#b9f6ca' }}>
              <div>Tokens earned: <span className="token-badge">🎁 {submitResult.tokens_earned}</span></div>
              {submitResult.tx_hash && submitResult.tx_hash.startsWith('0x') && (
                <div className="tx-box" style={{ marginTop: '.8rem' }}>{submitResult.tx_hash}</div>
              )}
            </div>
          </div>
        )}
        {submitResult && submitResult.error && (
          <div className="res-card error" style={{ maxWidth: 500 }}>
            <div className="res-title">❌ Failed</div>
            <p style={{ color: '#fca5a5' }}>{submitResult.error}</p>
          </div>
        )}
      </div>
    </div>
  );
}
