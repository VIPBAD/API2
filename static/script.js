document.addEventListener('DOMContentLoaded', () => {
  const audio = document.getElementById('audio');
  const seek = document.getElementById('seek');
  const playBtn = document.getElementById('playBtn');

  if (audio) {
    audio.onloadedmetadata = () => { updateSeek(); };
    audio.ontimeupdate = () => {
      if (!isNaN(audio.duration) && seek) {
        seek.value = (audio.currentTime / audio.duration) * 100 || 0;
      }
      updatePlayButton();
    };
  }

  window.togglePlay = function() {
    if (!audio) return;
    if (audio.paused) {
      audio.play().catch(()=>{});
    } else {
      audio.pause();
    }
    updatePlayButton();
  };

  window.rewind = function() {
    if (!audio) return;
    audio.currentTime = Math.max(0, audio.currentTime - 10);
  };

  window.forward = function() {
    if (!audio) return;
    audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 10);
  };

  if (seek && audio) {
    seek.addEventListener('input', () => {
      if (!isNaN(audio.duration)) {
        audio.currentTime = (seek.value / 100) * audio.duration;
      }
    });
  }

  function updatePlayButton() {
    if (!playBtn || !audio) return;
    playBtn.textContent = audio.paused ? "⏵" : "⏸";
  }
});
