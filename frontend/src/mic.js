/**
 * mic.js — WebRTC mic capture for live audio streaming
 * Owned by M2 (Audio & Signal Lead)
 *
 * Captures live microphone audio, chunks it every ~2 seconds,
 * and sends each chunk to a callback (which M3 will wire to the
 * WebSocket connection feeding M1's backend).
 */

export function startMicRecording(onAudioChunk, onError) {
  return new Promise((resolve, reject) => {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        const mediaRecorder = new MediaRecorder(stream);
        const CHUNK_INTERVAL_MS = 2000; // ~2 seconds per chunk, per guide

        mediaRecorder.ondataavailable = (event) => {
          if (event.data && event.data.size > 0) {
            // Hand the raw audio blob off to whatever callback
            // the frontend/backend integration wires in here.
            onAudioChunk(event.data);
          }
        };

        mediaRecorder.onerror = (event) => {
          console.error("MediaRecorder error:", event.error);
          if (onError) onError(event.error);
        };

        // start(timeslice) automatically fires ondataavailable every
        // CHUNK_INTERVAL_MS instead of only at the end of recording.
        mediaRecorder.start(CHUNK_INTERVAL_MS);

        console.log("Mic recording started, chunking every 2s.");

        // Return controls so the caller (App.tsx / M3's UI) can stop it later,
        // and expose the raw stream so other components (e.g. Waveform.tsx)
        // can read live audio levels from it.
        resolve({
          stop: () => {
            mediaRecorder.stop();
            stream.getTracks().forEach((track) => track.stop());
            console.log("Mic recording stopped.");
          },
          mediaRecorder,
          stream,
        });
      })
      .catch((err) => {
        console.error("Could not access microphone:", err);
        if (onError) onError(err);
        reject(err);
      });
  });
}

/**
 * Example usage (in App.tsx or wherever M3 wires this in):
 *
 * import { startMicRecording } from './mic';
 *
 * startMicRecording(
 *   (audioBlob) => {
 *     // send audioBlob over the WebSocket to M1's backend here
 *     websocket.send(audioBlob);
 *   },
 *   (error) => {
 *     // show an error state in the UI, e.g. "mic access denied"
 *   }
 * ).then((recorderControls) => {
 *   // recorderControls.stream is available here