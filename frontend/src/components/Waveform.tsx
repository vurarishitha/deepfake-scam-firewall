import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from "recharts";
import { useState, useEffect } from "react";

interface WaveformProps {
  score: number;
  pitchStd: number;
}

interface Point {
  time: string;
  score: number;
  pitch: number;
}

export default function Waveform({ score, pitchStd }: WaveformProps) {
  const [data, setData] = useState<Point[]>([]);

  useEffect(() => {
    setData((prev) => [
      ...prev.slice(-14),
      {
        time: new Date().toLocaleTimeString().split(" ")[0],
        score: score,
        pitch: pitchStd * 10,
      },
    ]);
  }, [score, pitchStd]);

  return (
    <div className="card">
      <h3>Real-time Signal Telemetry</h3>
      <div style={{ height: "200px", marginTop: "1rem" }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <XAxis dataKey="time" stroke="#64748b" />
            <YAxis domain={[0, 100]} stroke="#64748b" />
            <Line type="monotone" dataKey="score" stroke="#ef4444" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="pitch" stroke="#38bdf8" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}