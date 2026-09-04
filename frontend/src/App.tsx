import { useState, useEffect, useRef } from "react";
import ThreatGauge from "./ThreatGauge";
import Waveform from "./components/Waveform";
import Transcript from "./components/Transcript";
import InterceptOverlay from "./components/InterceptOverlay";
import "./dashboard.css";

interface TelemetryData {
  score: number;
  status: string;
  pitch_std: number;
  timbre_std: number;
  transcript: string;
}

export default function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [telemetry, setTelemetry] = useState<TelemetryData>({
    score: 0,
    status: "SAFE",
    pitch_std: 0,
    timbre_std: 0,
    transcript: "Awaiting live audio stream...",
  });

  const ws = useRef<WebSocket | null>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // 1. Establish WebSocket connection to FastAPI backend
    ws.current = new WebSocket("ws://localhost:8000/ws/stream");

    ws.current.onopen = () => {
      console.log("[WS Connected]: Real-time telemetry feed active.");
      setIsConnected(true);
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("[WS Payload Received from Backend]:", data);

        // Support flexible fallback keys for score mapping
        const resolvedScore = data.score ?? data.threat_score ?? data.composite_risk ?? 0;

        setTelemetry({
          score: resolvedScore,
          status: resolvedScore >= 80 || data.action === "INTERCEPT" ? "INTERCEPT" : "SAFE",
          pitch_std: data.pitch_std ?? data.pitch ?? 0.0,
          timbre_std: data.timbre_std ?? data.timbre ?? 0.0,
          transcript: data.transcript || "Monitoring call...",
        });
      } catch (err) {
        console.error("[WS Parse Error]:", err);
      }
    };

    ws.current.onclose = () => {
      console.log("[WS Disconnected]");
      setIsConnected(false);
    };

    // 2. Initialize Browser Web Speech API for real-time Speech-to-Text
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-US";

      recognition.onresult = (event: any) => {
        let currentTranscript = "";
        // Start from event.resultIndex to prevent duplicate stacking of past history
        for (let i = event.resultIndex; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript + " ";
        }

        const cleanedTranscript = currentTranscript.trim();
        if (cleanedTranscript) {
          console.log("[Cleaned Speech Sent to Backend]:", cleanedTranscript);
        }

        // Send transcript payload over active WebSocket stream
        if (ws.current && ws.current.readyState === WebSocket.OPEN && cleanedTranscript) {
          ws.current.send(JSON.stringify({ transcript: cleanedTranscript }));
        }
      };

      recognition.onerror = (e: any) => console.error("[STT Error]:", e.error);
      recognition.onend = () => {
        // Auto-restart listener if active
        if (isListening) {
          try {
            recognition.start();
          } catch (err) {
            // Ignore if already started
          }
        }
      };

      recognitionRef.current = recognition;
    } else {
      console.warn("Web Speech API is not supported in this browser.");
    }

    return () => {
      ws.current?.close();
      recognitionRef.current?.stop();
    };
  }, []);

  // Handler to toggle live microphone recording
  const toggleListening = () => {
    if (!recognitionRef.current) return;

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        console.error("Error starting speech recognition:", err);
      }
    }
  };

  return (
    <div className="dashboard-container">
      {/* Top Header */}
      <header className="dashboard-header">
        <h1>Deepfake Scam Firewall</h1>
        <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
          <button 
            onClick={toggleListening}
            style={{
              padding: "8px 16px",
              borderRadius: "6px",
              border: "none",
              backgroundColor: isListening ? "#ef4444" : "#10b981",
              color: "#fff",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            {isListening ? "⏹ Stop Listening" : "🎙 Start Mic Stream"}
          </button>
          <div className={`status-badge ${isConnected ? "online" : "offline"}`}>
            {isConnected ? "● WS Connected (8000)" : "○ Disconnected"}
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <main className="dashboard-grid">
        <div className="card gauge-card">
          <ThreatGauge score={telemetry.score} status={telemetry.status} />
        </div>

        <div className="card waveform-card">
          <Waveform 
            pitchStd={telemetry.pitch_std} 
            timbreStd={telemetry.timbre_std} 
          />
        </div>

        <div className="card transcript-card">
          <Transcript text={telemetry.transcript} />
        </div>
      </main>

      {/* Intercept Overlay at 80%+ Risk */}
      {telemetry.score >= 80 && (
        <InterceptOverlay 
          score={telemetry.score} 
          transcript={telemetry.transcript} 
        />
      )}
    </div>
  );
}