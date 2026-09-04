export interface TranscriptEntry {
  id: string;
  time: string;
  text: string;
  flagged?: boolean; // true if this line contributed to a scam-risk spike
}

interface TranscriptProps {
  entries: TranscriptEntry[];
}

export default function Transcript({ entries }: TranscriptProps) {
  return (
    <div className="panel transcript-panel">
      <div className="panel-label">Live Transcript</div>
      <div className="transcript-list">
        {entries.length === 0 && (
          <div className="transcript-line" style={{ color: 'var(--text-muted)' }}>
            Waiting for audio...
          </div>
        )}
        {entries.map((entry) => (
          <div
            key={entry.id}
            className={`transcript-line${entry.flagged ? ' flagged' : ''}`}
          >
            <span className="transcript-time">{entry.time}</span>
            {entry.text}
          </div>
        ))}
      </div>
    </div>
  );
}