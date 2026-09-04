import { useEffect, useRef } from "react";
import { ShieldAlert, PhoneOff, RotateCcw } from "lucide-react";
import "./InterceptOverlay.css";

interface InterceptOverlayProps {
  isActive: boolean;
  riskScore: number;
  reason: string;
  onReset: () => void;
}

export default function InterceptOverlay({
  isActive,
  riskScore,
  reason,
  onReset,
}: InterceptOverlayProps) {
  const audioCtxRef = useRef<AudioContext | null>(null);
  const hasPlayedRef = useRef(false);

  useEffect(() => {
    if (!isActive) {
      hasPlayedRef.current = false;
      return;
    }
    if (hasPlayedRef.current) return;
    hasPlayedRef.current = true;

    try {
      const ctx = audioCtxRef.current ?? new AudioContext();
      audioCtxRef.current = ctx;

      const playTone = (freq: number, startTime: number, duration: number) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "square";
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0, startTime);
        gain.gain.linearRampToValueAtTime(0.15, startTime + 0.02);
        gain.gain.linearRampToValueAtTime(0, startTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + duration);
      };

      const now = ctx.currentTime;
      playTone(880, now, 0.18);
      playTone(660, now + 0.22, 0.18);
      playTone(880, now + 0.44, 0.18);
      playTone(660, now + 0.66, 0.18);
    } catch {
      // Audio is a nice-to-have; never block the visual interception on it.
    }

    return () => {
      audioCtxRef.current?.close().catch(() => {});
      audioCtxRef.current = null;
    };
  }, [isActive]);

  if (!isActive) return null;

  const riskPercent = Math.round(riskScore * 100);

  return (
    <div
      className="intercept-overlay"
      role="alertdialog"
      aria-live="assertive"
      aria-labelledby="intercept-title"
      aria-describedby="intercept-desc"
    >
      <div className="intercept-overlay__panel">
        <ShieldAlert className="intercept-overlay__icon" size={56} strokeWidth={1.5} aria-hidden="true" />
        <h2 id="intercept-title" className="intercept-overlay__title">Call terminated</h2>
        <p id="intercept-desc" className="intercept-overlay__desc">
          Scam risk reached {riskPercent}%, above the 80% interception threshold.
        </p>
        {reason && (
          <div className="intercept-overlay__reason">
            <span className="intercept-overlay__reason-label">Flagged for</span>
            <span className="intercept-overlay__reason-text">{reason}</span>
          </div>
        )}
        <div className="intercept-overlay__lock">
          <PhoneOff size={18} strokeWidth={1.75} aria-hidden="true" />
          <span>Call locked — audio blocked</span>
        </div>
        <button type="button" className="intercept-overlay__reset" onClick={onReset}>
          <RotateCcw size={16} strokeWidth={1.75} aria-hidden="true" />
          Reset for next call
        </button>
      </div>
    </div>
  );
}