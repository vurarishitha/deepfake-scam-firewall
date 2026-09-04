interface InterceptOverlayProps {
  riskScore: number;
  onDismiss: () => void;
}

export default function InterceptOverlay({ riskScore, onDismiss }: InterceptOverlayProps) {
  return (
    <div className="intercept-overlay" role="alertdialog" aria-live="assertive">
      <div className="intercept-title">CALL TERMINATED</div>
      <div className="intercept-reason">
        Fused risk score crossed the 0.80 threshold. This call was automatically
        intercepted based on combined language and voice-authenticity analysis.
      </div>
      <div className="intercept-score">Final risk: {riskScore.toFixed(2)}</div>
      <div className="demo-controls">
        <button onClick={onDismiss}>Reset demo</button>
      </div>
    </div>
  );
}