import { useState } from 'react';
import InterceptOverlay from './components/InterceptOverlay';
import './App.css';

function App() {
  const [fusedRisk, setFusedRisk] = useState(0.9);
  const [latestReason, setLatestReason] = useState('Caller requested OTP code');

  return (
    <div>
      <h1>Deepfake & Scam Defense Firewall</h1>

      <InterceptOverlay
        isActive={fusedRisk > 0.8}
        riskScore={fusedRisk}
        reason={latestReason}
        onReset={() => setFusedRisk(0)}
      />
    </div>
  );
}

export default App;