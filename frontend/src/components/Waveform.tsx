import { useEffect, useState } from 'react';

interface WaveformProps {
  isDanger?: boolean; // true once risk crosses threshold, tints bars red
  barCount?: number;
}

export default function Waveform({ isDanger = false, barCount = 48 }: WaveformProps) {
  const [heights, setHeights] = useState<number[]>(
    Array.from({ length: barCount }, () => 8)
  );

  useEffect(() => {
    // Placeholder animation until wired to real mic/wavesurfer.js data.
    const interval = setInterval(() => {
      setHeights((prev) =>
        prev.map(() => 6 + Math.random() * (isDanger ? 74 : 54))
      );
    }, 120);
    return () => clearInterval(interval);
  }, [isDanger]);

  return (
    <div className="panel waveform-panel">
      <div className="panel-label">Live Audio</div>
      <div className="waveform-bars">
        {heights.map((h, i) => (
          <div
            key={i}
            className={`waveform-bar${isDanger ? ' danger' : ''}`}
            style={{ height: `${h}px` }}
          />
        ))}
      </div>
    </div>
  );
}