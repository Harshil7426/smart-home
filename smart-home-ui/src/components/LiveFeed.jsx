import { useEffect, useState } from 'react';
import axios from 'axios';

const API = "http://localhost:8000";
const ML_STREAM_URL = "http://localhost:5001/video_feed";

export default function LiveFeed() {
    const [lastIntent, setLastIntent] = useState(null);
    const [streamError, setStreamError] = useState(false);

    useEffect(() => {
        const fetchLastIntent = async () => {
            try {
                const res = await axios.get(`${BACKEND_API}/logs`);
                if (res.data.length > 0) {
                    const latest = res.data[res.data.length - 1];
                    // Only show if it happened in the last 10 seconds
                    const diff = (new Date() - new Date(latest.timestamp)) / 1000;
                    if (diff < 10) {
                        setLastIntent(latest.intent);
                    } else {
                        setLastIntent(null);
                    }
                }
            } catch (err) {
                console.error("Error fetching intent:", err);
            }
        };

        const interval = setInterval(fetchLastIntent, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="glass-card">
            <div className="section-title">ML Vision Stream</div>
            <div className="live-feed-container" style={{ background: '#1a1c23' }}>
                {!streamError ? (
                    <img
                        src={ML_STREAM_URL}
                        alt="ML Vision Stream"
                        className="live-feed-video"
                        onError={() => setStreamError(true)}
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                ) : (
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        height: '100%',
                        color: 'var(--text-secondary)',
                        textAlign: 'center',
                        padding: '20px'
                    }}>
                        <span style={{ fontSize: '2rem', marginBottom: '10px' }}>⚠️</span>
                        ML Engine Offline<br />
                        <span style={{ fontSize: '0.8rem' }}>Please ensure `ml_engine.py` is running on port 5001</span>
                        <button
                            onClick={() => setStreamError(false)}
                            style={{
                                marginTop: '15px',
                                background: 'var(--accent-cyan)',
                                border: 'none',
                                padding: '8px 16px',
                                borderRadius: '6px',
                                cursor: 'pointer',
                                fontWeight: '600'
                            }}
                        >
                            Retry Connection
                        </button>
                    </div>
                )}

                <div className="live-feed-overlay">
                    <div className="live-status">
                        <span style={{ width: 8, height: 8, background: '#fff', borderRadius: '50%' }}></span>
                        LIVE STREAM
                    </div>

                    {lastIntent && (
                        <div style={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            background: 'rgba(0, 242, 255, 0.2)',
                            padding: '20px 40px',
                            borderRadius: '12px',
                            border: '2px solid var(--accent-cyan)',
                            backdropFilter: 'blur(10px)',
                            color: 'var(--accent-cyan)',
                            fontWeight: '700',
                            fontSize: '1.2rem',
                            textAlign: 'center',
                            boxShadow: '0 0 30px rgba(0, 242, 255, 0.4)',
                            animation: 'pulse 1s infinite'
                        }}>
                            GESTURE DETECTED<br />
                            <span style={{ fontSize: '1.5rem', color: '#fff' }}>
                                {lastIntent.replace(/_/g, ' ')}
                            </span>
                        </div>
                    )}

                    <div style={{
                        position: 'absolute',
                        bottom: '20px',
                        left: '20px',
                        background: 'rgba(0, 242, 255, 0.1)',
                        padding: '10px 20px',
                        borderRadius: '8px',
                        border: '1px solid var(--accent-cyan)',
                        color: 'var(--accent-cyan)',
                        fontWeight: '600',
                        fontSize: '0.8rem'
                    }}>
                        AI CORE: ACTIVE
                    </div>
                </div>
            </div>
        </div>
    );
}
