export default function Transcript({ text }: { text: string }) {
  return (
    <div className="card">
      <h3>Live Transcript & Context</h3>
      <div className="transcript-box">
        <code>{text}</code>
      </div>
    </div>
  );
}