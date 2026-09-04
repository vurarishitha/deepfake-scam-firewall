interface ThreatGaugeProps {
  riskScore: number; // 0.0 - 1.0, fused risk from M1's risk_engine.py
  acousticScore?: number; // M2's synthetic_risk
  languageScore?: number; // M1's LLM scam-intent score
}

function riskLabel(score: number): { label: string; color: string } {
  if (score >= 0.8) return { label: 'HIGH RISK', color: 'var(--danger)' };
  if (score >= 0.5) return { label: 'ELEVATED', color: 'var(--warning)' };
  return { label: 'LOW RISK', color: 'var(--safe)' };
}

export default function ThreatGauge({
  riskScore,
  acousticScore,
  languageScore,
}: ThreatGaugeProps) {
  const { label, color } = riskLabel(riskScore);

  return (
    <div className="panel gauge-wrap">
      <div className="panel-label">Fused Risk Score</div>
      <div className="gauge-value" style={{ color }}>
        {riskScore.toFixed(2)}
      </div>
      <div className="gauge-sublabel" style={{ color }}>
        {label}
      </div>

      {(acousticScore !== undefined || languageScore !== undefined) && (
        <div className="risk-breakdown">
          {acousticScore !== undefined && (
            <div className="risk-breakdown-row">
              <span>Acoustic (M2, 40%)</span>
              <span>{acousticScore.toFixed(2)}</span>
            </div>
          )}
          {languageScore !== undefined && (
            <div className="risk-breakdown-row">
              <span>Language (M1, 60%)</span>
              <span>{languageScore.toFixed(2)}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}