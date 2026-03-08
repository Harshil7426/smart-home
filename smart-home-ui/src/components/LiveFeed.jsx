import { useEffect, useRef, useState } from 'react';
import axios from 'axios';

const API = "https://smart-home-4b7r.onrender.com";

export default function LiveFeed() {
    const videoRef = useRef(null);
    const [lastIntent, setLastIntent] = useState(null);

    useEffect(() => {
        async function setupCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            } catch (err) {
                console.error("Error accessing camera:", err);
            }
        }
        setupCamera();

        const fetchLastIntent = async () => {
            try {
                const res = await axios.get(`${API}/logs`);
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

        return () => {
            clearInterval(interval);
            if (videoRef.current && videoRef.current.srcObject) {
                const tracks = videoRef.current.srcObject.getTracks();
                tracks.forEach(track => track.stop());
            }
        };
    }, []);

    return (
        <div className="glass-card">
            <div className="section-title">Live Vision Feed</div>
            <div className="live-feed-container">
                <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="live-feed-video"
                />
                <div className="live-feed-overlay">
                    <div className="live-status">
                        <span style={{ width: 8, height: 8, background: '#fff', borderRadius: '50%' }}></span>
                        LIVE
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
                        background: 'rgba(255, 255, 255, 0.05)',
                        padding: '10px 20px',
                        borderRadius: '8px',
                        border: '1px solid var(--glass-border)',
                        color: 'var(--text-secondary)',
                        fontWeight: '600',
                        fontSize: '0.8rem'
                    }}>
                        AI CORE: OPTIMIZED
                    </div>
                </div>
            </div>
        </div>
    );
}
