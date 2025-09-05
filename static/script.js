// Shared player logic for player.html (and works if audio element exists on other pages)
document.addEventListener('DOMContentLoaded', () => {
  const audio = document.getElementById('audio');
  const seek = document.getElementById('seek');
  const current = document.getElementById('current');
  const total = document.getElementById('total');
  const playBtn = document.getElementById('playBtn');

  if (!audio) return;

  // autoplay if src present
  if (audio.src && audio.src.length > 0) {
    // try to play — browsers may block without user gesture; this keeps behavior same as before
    audio.play().catch(()=>{ /* autoplay blocked, user can press play */ });
  }

  function formatTime(seconds) {
    if (isNaN(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  }

  audio.ontimeupdate = () => {
    if (!isNaN(audio.duration)) {
      if (seek) seek.value = (audio.currentTime / audio.duration) * 100 || 0;
      if (current) current.textContent = formatTime(audio.currentTime);
      if (total) total.textContent = formatTime(audio.duration);
    }
    updatePlayButton();
  };

  if (seek) {
    seek.oninput = () => {
      if (!isNaN(audio.duration)) {
        audio.currentTime = (seek.value / 100) * audio.duration;
      }
    };
  }

  window.togglePlay = function() {
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
    updatePlayButton();
  };

  function updatePlayButton() {
    if (!playBtn) return;
    playBtn.textContent = audio.paused ? "⏵" : "⏸";
  }

  // Initialize button state
  updatePlayButton();
});
