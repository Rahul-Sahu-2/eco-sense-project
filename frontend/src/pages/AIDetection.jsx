import { useState, useRef, useCallback, useEffect } from 'react';
import { detectWaste, getDetectionTip, getDetectionExplanation, sendChatMessage } from '../api/api';

export default function AIDetection() {
  const [activeTab, setActiveTab] = useState('detection');
  const [detecting, setDetecting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [detectedItems, setDetectedItems] = useState([]);
  const [annotatedImage, setAnnotatedImage] = useState(null);
  const [tip, setTip] = useState('');
  const [tipLoading, setTipLoading] = useState(false);

  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [deepAnalysis, setDeepAnalysis] = useState('');
  const [analysisLoading, setAnalysisLoading] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);

  const startDetection = useCallback(async () => {
    setDetecting(true);
    setProgress(0);
    setDetectedItems([]);
    setAnnotatedImage(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      const allItems = new Map();
      let lastAnnotated = null;
      const startTime = Date.now();
      const DURATION = 7000;

      intervalRef.current = setInterval(async () => {
        const elapsed = Date.now() - startTime;
        const pct = Math.min(100, Math.round((elapsed / DURATION) * 100));
        setProgress(pct);

        if (elapsed >= DURATION) {
          clearInterval(intervalRef.current);
          stream.getTracks().forEach(t => t.stop());
          setDetecting(false);

          const items = Array.from(allItems.values());
          setDetectedItems(items);
          if (lastAnnotated) setAnnotatedImage(lastAnnotated);
          if (items.length > 0) {
            setShowResult(true);
            setTipLoading(true);
            try {
              const tipRes = await getDetectionTip(items.map(i => i.name));
              setTip(tipRes.data.tip);
            } catch { setTip('Could not generate tip.'); }
            setTipLoading(false);
          } else {
            setShowResult(true);
          }
          return;
        }

        const video = videoRef.current;
        const canvas = canvasRef.current;
        if (!video || !canvas) return;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        const dataUrl = canvas.toDataURL('image/jpeg', 0.7);
        const base64 = dataUrl.split(',')[1];

        try {
          const res = await detectWaste(base64);
          const data = res.data;
          if (data.items) data.items.forEach(item => allItems.set(item.name, item));
          if (data.annotated_image) lastAnnotated = `data:image/jpeg;base64,${data.annotated_image}`;
        } catch (err) {
          console.error('Detection error:', err);
        }
      }, 1500);

    } catch (err) {
      console.error('Webcam error:', err);
      setDetecting(false);
    }
  }, []);

  const resetDetection = () => {
    setShowResult(false);
    setDetectedItems([]);
    setAnnotatedImage(null);
    setTip('');
    setProgress(0);
    setDeepAnalysis('');
    setChatHistory([]);
  };

  const handleChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || chatLoading) return;
    const userMsg = chatInput.trim();
    setChatInput('');
    setChatHistory(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatLoading(true);
    try {
      const res = await sendChatMessage(userMsg);
      setChatHistory(prev => [...prev, { role: 'assistant', text: res.data.response }]);
    } catch {
      setChatHistory(prev => [...prev, { role: 'assistant', text: 'Error: Could not get response.' }]);
    }
    setChatLoading(false);
  };

  useEffect(() => {
    if (activeTab === 'chatbot' && detectedItems.length > 0 && !deepAnalysis && !analysisLoading) {
      setAnalysisLoading(true);
      getDetectionExplanation(detectedItems.map(i => i.name))
        .then(res => setDeepAnalysis(res.data.explanation))
        .catch(() => setDeepAnalysis('Could not generate analysis.'))
        .finally(() => setAnalysisLoading(false));
    }
  }, [activeTab, detectedItems, deepAnalysis, analysisLoading]);

  const recyclable = detectedItems.filter(i => i.category === 'recyclable');
  const nonRecyclable = detectedItems.filter(i => i.category === 'non_recyclable');
  const hazardous = detectedItems.filter(i => i.category === 'hazardous');

  return (
    <div>
      {/* Hero */}
      <div className="hero-section">
        <div className="hero-eyebrow"><span className="dot"></span> AI-Powered Detection</div>
        <h1 className="hero-title">
          Smart Waste<br />
          <span className="hero-accent">Classification Engine</span>
        </h1>
        <p className="hero-subtitle">
          Real-time waste detection powered by YOLOv8 computer vision. Identify, classify, and receive AI-generated recycling guidance instantly.
        </p>
      </div>

      {/* Banners */}
      <div className="banner-row">
        <div className="banner-card">
          <img src="https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=600&q=80" alt="" />
          <div className="banner-label">Computer Vision</div>
        </div>
        <div className="banner-card">
          <img src="https://images.unsplash.com/photo-1604187351574-c75ca79f5807?w=600&q=80" alt="" />
          <div className="banner-label">Smart Sorting</div>
        </div>
        <div className="banner-card">
          <img src="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?w=600&q=80" alt="" />
          <div className="banner-label">Eco Impact</div>
        </div>
      </div>

      {/* Pills */}
      <div className="feature-pills">
        <span className="pill green">⚡ Live Detection</span>
        <span className="pill teal">🤖 AI Tips</span>
        <span className="pill amber">♻️ Categorization</span>
        <span className="pill red">☣️ Hazard Alert</span>
      </div>

      {/* Tabs */}
      <div className="tabs-container">
        <div className="tabs-header">
          <button className={`tab-btn${activeTab === 'detection' ? ' active' : ''}`} onClick={() => setActiveTab('detection')}>
            📷 Detection
          </button>
          <button className={`tab-btn${activeTab === 'chatbot' ? ' active' : ''}`} onClick={() => setActiveTab('chatbot')}>
            🤖 Chatbot
          </button>
        </div>

        {/* Detection Tab */}
        {activeTab === 'detection' && (
          <div className="fade-in">
            {showResult ? (
              <div>
                <div className="metrics-row">
                  {[
                    { icon: '🔍', val: detectedItems.length, lbl: 'Detected', cls: '' },
                    { icon: '♻️', val: recyclable.length, lbl: 'Recyclable', cls: 'green' },
                    { icon: '📦', val: nonRecyclable.length, lbl: 'Non-Recyclable', cls: 'blue' },
                    { icon: '⚠️', val: hazardous.length, lbl: 'Hazardous', cls: 'red' },
                  ].map(m => (
                    <div className={`metric-card ${m.cls}`} key={m.lbl}>
                      <span className="metric-icon">{m.icon}</span>
                      <div className="metric-val">{m.val}</div>
                      <div className="metric-lbl">{m.lbl}</div>
                    </div>
                  ))}
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 1fr 1fr', gap: '1.5rem', marginTop: '1rem' }}>
                  <div className="fade-in-d1">
                    <p className="col-label">Detected Frame</p>
                    {annotatedImage ? (
                      <img src={annotatedImage} alt="Detection" style={{ width: '100%', borderRadius: '16px', border: '1px solid rgba(124,58,237,0.15)' }} />
                    ) : (
                      <div className="empty-preview" style={{ height: 200 }}>
                        <div style={{ fontSize: '2rem', marginBottom: '.5rem' }}>📷</div>
                        No frame captured
                      </div>
                    )}
                  </div>

                  <div className="fade-in-d2">
                    <p className="col-label">Classification</p>
                    {detectedItems.length === 0 && <div className="location-warning">No items detected.</div>}
                    {recyclable.length > 0 && (
                      <div className="result-recyclable">
                        <b>✅ Recyclable</b><br />
                        {recyclable.map(i => `• ${i.name.replace(/_/g, ' ')}`).join('\n')}
                      </div>
                    )}
                    {nonRecyclable.length > 0 && (
                      <div className="result-nonrecyclable">
                        <b>📦 Non-Recyclable</b><br />
                        {nonRecyclable.map(i => `• ${i.name.replace(/_/g, ' ')}`).join('\n')}
                      </div>
                    )}
                    {hazardous.length > 0 && (
                      <div className="result-hazardous">
                        <b>⚠️ Hazardous</b><br />
                        {hazardous.map(i => `• ${i.name.replace(/_/g, ' ')}`).join('\n')}
                      </div>
                    )}
                  </div>

                  <div className="fade-in-d3">
                    <p className="col-label">AI Quick Tip</p>
                    <div className="tip-card">
                      <span className="tip-icon">🌿</span>
                      {tipLoading ? (
                        <p><span className="spinner"></span> Generating tip...</p>
                      ) : (
                        <p>{tip || 'No tip available.'}</p>
                      )}
                      <div className="tip-footer">Switch to Chatbot tab for detailed analysis</div>
                    </div>
                  </div>
                </div>

                <div style={{ marginTop: '1.5rem' }}>
                  <button className="btn-primary" onClick={resetDetection}>🔄  Detect Again</button>
                </div>
              </div>
            ) : (
              <div>
                <div className="detection-panel">
                  <div className="banner-row" style={{ marginBottom: '2rem' }}>
                    <div className="banner-card" style={{ height: 150 }}>
                      <img src="https://images.unsplash.com/photo-1567177662154-dfeb4c93b6ae?w=400&q=80" alt="" />
                      <div className="banner-label">Input</div>
                    </div>
                    <div className="banner-card" style={{ height: 150 }}>
                      <img src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80" alt="" />
                      <div className="banner-label">Processing</div>
                    </div>
                    <div className="banner-card" style={{ height: 150 }}>
                      <img src="https://images.unsplash.com/photo-1507146153580-69a1fe6d8aa1?w=400&q=80" alt="" />
                      <div className="banner-label">Output</div>
                    </div>
                  </div>

                  <div className="steps-row">
                    <div className="step-card"><span className="step-num">01</span><div className="step-txt">Allow webcam access</div></div>
                    <span className="step-arrow">→</span>
                    <div className="step-card"><span className="step-num">02</span><div className="step-txt">Show waste to camera</div></div>
                    <span className="step-arrow">→</span>
                    <div className="step-card"><span className="step-num">03</span><div className="step-txt">AI scans in 7 seconds</div></div>
                    <span className="step-arrow">→</span>
                    <div className="step-card"><span className="step-num">04</span><div className="step-txt">Get results & tips</div></div>
                  </div>
                </div>

                {detecting && (
                  <div style={{ marginBottom: '1.5rem' }}>
                    <div className="webcam-container">
                      <video ref={videoRef} autoPlay playsInline muted style={{ width: '100%' }} />
                      <canvas ref={canvasRef} style={{ display: 'none' }} />
                      <div className="webcam-overlay">
                        <span className="status-dot"></span> SCANNING
                      </div>
                    </div>
                    <div className="detect-progress" style={{ marginTop: '.8rem' }}>
                      <div className="dp-top">
                        <span>Scanning...</span>
                        <span>{Math.max(0, 7 - Math.round(progress * 7 / 100))}s remaining</span>
                      </div>
                      <div className="prog-bar-bg">
                        <div className="prog-bar-fill" style={{ width: `${progress}%` }}></div>
                      </div>
                    </div>
                  </div>
                )}

                {!detecting && (
                  <button className="btn-primary" onClick={startDetection}>▶  Start Detection</button>
                )}
              </div>
            )}
          </div>
        )}

        {/* Chatbot Tab */}
        {activeTab === 'chatbot' && (
          <div className="fade-in">
            <div className="chatbot-header">
              <div className="chatbot-avatar">🤖</div>
              <div>
                <div className="chatbot-title">Waste Management Assistant</div>
                <div className="chatbot-status"><span className="status-dot"></span> Online</div>
              </div>
            </div>

            {detectedItems.length > 0 && (
              <div className="detected-banner">
                Auto-analyzing: <b>{detectedItems.map(i => i.name.replace(/_/g, ' ')).join(', ')}</b>
              </div>
            )}

            {analysisLoading && (
              <div className="res-card success"><span className="spinner"></span> Generating analysis...</div>
            )}

            {deepAnalysis && (
              <div style={{ marginBottom: '1.5rem' }}>
                <h3 style={{ fontFamily: 'var(--f-display)', color: 'var(--text-1)', marginBottom: '.8rem', fontWeight: 700 }}>📋 Analysis Report</h3>
                <div className="tip-card"><p style={{ whiteSpace: 'pre-wrap' }}>{deepAnalysis}</p></div>
              </div>
            )}

            <div className="chat-messages">
              {chatHistory.map((msg, i) => (
                <div key={i} className={`chat-bubble ${msg.role}`}><p>{msg.text}</p></div>
              ))}
              {chatLoading && (
                <div className="chat-bubble assistant"><p><span className="spinner"></span> Thinking...</p></div>
              )}
            </div>

            <form className="chat-input-bar" onSubmit={handleChat}>
              <input
                className="chat-input"
                type="text"
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                placeholder="Ask about waste disposal, recycling, hazardous materials..."
                disabled={chatLoading}
              />
              <button className="chat-send-btn" type="submit" disabled={chatLoading || !chatInput.trim()}>Send</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
