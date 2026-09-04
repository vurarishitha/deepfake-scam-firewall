export default function InterceptOverlay({ score }: { score?: number }) {
  // Safely handle undefined/null scores to prevent toFixed crashes
  const safeScore = Number(score ?? 0);

  return (
    <div className="overlay-backdrop">
      <div className="overlay-modal">
        <h2>⚠️ POTENTIAL DEEPFAKE SCAM DETECTED</h2>
        <p>Threat Score reached {safeScore.toFixed(0)}%. Synthetic audio patterns confirmed by M2 metrics.</p>
        <button onClick={() => window.location.reload()}>Dismiss Alert</button>
      </div>
    </div>
  );
}