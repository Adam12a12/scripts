// This script is designed to be copied and pasted into the console of the video tab
// It will start the video and set the volume to max, you will need to keep the tab open, prevent the machine from suspending, and wait until the video is finished playing before the browser downloads the video


(async () => {
  const v = [...document.querySelectorAll('video')].sort((a, b) => b.videoWidth * b.videoHeight - a.videoWidth * a.videoHeight)[0];
  if (!v) return console.log('No video element found');
  console.log('Element:', v.videoWidth + 'x' + v.videoHeight, '| duration:', Math.round(v.duration) + 's');

  const capture = v.captureStream || v.mozCaptureStream;
  if (typeof capture !== 'function') return console.log('No capture function on this element');

  v.currentTime = 0;
  v.muted = false;
  v.volume = 1;
  await v.play();

  const stream = capture.call(v, 30);
  const audioTracks = stream.getAudioTracks().length;
  console.log('Tracks:', audioTracks, 'audio |', stream.getVideoTracks().length, 'video');
  if (!audioTracks) {
    stream.getTracks().forEach((t) => t.stop());
    return console.log('No audio track. Aborted, nothing recorded.');
  }

  const mime = ['video/webm;codecs=vp9,opus', 'video/webm;codecs=vp8,opus', 'video/webm']
    .find((m) => MediaRecorder.isTypeSupported(m));
  console.log('Mime:', mime);

  const chunks = [];
  const rec = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 5000000, audioBitsPerSecond: 160000 });
  rec.ondataavailable = (e) => e.data.size && chunks.push(e.data);
  rec.onstop = () => {
    const blob = new Blob(chunks, { type: mime });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'video.webm';
    a.click();
    console.log('Done:', (blob.size / 1048576).toFixed(1), 'MB');
  };

  rec.start(1000);
  v.onended = () => rec.stop();

  window.__rec = rec;
  window.__stop = () => rec.stop();
  window.__status = () => console.log(rec.state, '|', (chunks.reduce((s, c) => s + c.size, 0) / 1048576).toFixed(1), 'MB');
  console.log('Full recording started, length ' + Math.round(v.duration / 60) + ' min');
})();
