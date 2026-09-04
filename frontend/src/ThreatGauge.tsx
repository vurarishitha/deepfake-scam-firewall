interface ThreatGaugeProps {
  score?: number;
  pitchStd?: number;
  timbreStd?: number;
}

export default function ThreatGauge({ score = 0, pitchStd = 0, timbreStd = 0 }: ThreatGaugeProps) {
  const isDanger = score > 60;

  return (
    <div className="card threat-card">
      <h3>Threat Level</h3>
      <div className={`score-display ${isDanger ? "danger" : "safe"}`}>
        {score}%
      </div>
      <div className={`status-badge ${isDanger ? "badge-danger" : "badge-safe"}`}>
        {isDanger ? "CRITICAL: SCAM DETECTED" : "LOW RISK / SAFE"}
      </div>

      <div className="m2-metrics">
        <h4>M2 Librosa Telemetry</h4>
        <div className="metric-row">
          <span>Pitch Std Dev:</span>
          <strong>{Number(pitchStd ?? 0).toFixed(2)}</strong>
        </div>
        <div className="metric-row">
          <span>Timbre Std Dev:</span>
          <strong>{Number(timbreStd ?? 0).toFixed(2)}</strong>
        </div>
      </div>
    </div>
  );
}