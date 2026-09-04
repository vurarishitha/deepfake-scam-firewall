import { useState } from 'react';
import ThreatGauge from './components/ThreatGauge';
import Waveform from './components/Waveform';
import Transcript, { TranscriptEntry } from './components/Transcript';
import InterceptOverlay from './components/InterceptOverlay';
import './dashboard.css';

// Mock conversation used to validate the UI before M1's live WebSocket exists.
const MOCK_SCRIPT: { text: string; risk: number; flagged?: boolean }[] = [
  { text: 'Hello, this is calling from your bank.', risk: 0.12 },
  { text: 'We noticed unusual activity on your account.', risk: 0.28 },
  { text: 'I need to verify your identity first.', risk: 0.35 },
  { text: 'Can you confirm the one-time code we just sent you?', risk: 0.71, flagged: true },
  { text: 'Please read out the 6-digit code now, it is urgent.', risk: 0.91, flagged: true },
];

function App() {
  const [entries, setEntries] = useState<TranscriptEntry[]>([]);
  const [riskScore, setRiskScore] = useState(0);
  const [acousticScore, setAcousticScore] = useState(0.1);
  const [languageScore, setLanguageScore] = useState(0.1);
  const [intercepted, setIntercepted] = useState(false);
  const [running, setRunning] = useState(false);

  const runDemo = () => {
    if (running) return;
    setRunning(true);
    setEntries([]);
    setRiskScore(0);
    setIntercepted(false);

    MOCK_SCRIPT.forEach((line, i) => {
      setTimeout(() => {
        const time = new Date().toLocaleTimeString('en-US', { hour12: false });
        setEntries((prev) => [
          ...prev,
          { id: `${i}`, time, text: line.text, flagged: line.flagged },
        ]);
        setRiskScore(line.risk);
        setLanguageScore(Math.min(1, line.risk + 0.08));
        setAcousticScore(Math.max(0, line.risk - 0.15));

        if (line.risk >= 0.8) {
          setIntercepted(true);
          setRunning(false);
        } else if (i === MOCK_SCRIPT.length - 1) {
          setRunning(false);
        }
      }, i * 1400);
    });
  };

  const resetDemo = () => {
    setIntercepted(false);
    setEntries([]);
    setRiskScore(0);
    setAcousticScore(0.1);
    setLanguageScore(0.1);
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Scam Defense Firewall</h1>
        <div className="call-status">
          {intercepted ? 'CALL TERMINATED' : running ? 'CALL IN PROGRESS' : 'IDLE'}
        </div>
      </div>

      <ThreatGauge
        riskScore={riskScore}
        acousticScore={acousticScore}
        languageScore={languageScore}
      />

      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <Waveform isDanger={riskScore >= 0.8} />
        <Transcript entries={entries} />
      </div>

      <div className="demo-controls">
        <button onClick={runDemo} disabled={running}>
          {running ? 'Running mock call...' : 'Run mock call (demo data)'}
        </button>
      </div>

      {intercepted && (
        <InterceptOverlay riskScore={riskScore} onDismiss={resetDemo} />
      )}
    </div>
  );
}

export default App;
