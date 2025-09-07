document.addEventListener('DOMContentLoaded', () => {
  // Player controls (used by player.html)
  const audio = document.getElementById('audio');
  const seek = document.getElementById('seek');
  const playBtn = document.getElementById('playBtn');

  if (audio) {
    audio.ontimeupdate = () => {
      if (!isNaN(audio.duration) && seek) {
        seek.value = (audio.currentTime / audio.duration) * 100 || 0;
      }
      updatePlayButton();
    };
  }

  window.togglePlay = function() {
    if (!audio) return;
    if (audio.paused) audio.play().catch(()=>{});
    else audio.pause();
    updatePlayButton();
  };

  window.rewind = function() { if (audio) audio.currentTime = Math.max(0, audio.currentTime - 10); };
  window.forward = function() { if (audio) audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 10); };
  if (seek && audio) {
    seek.addEventListener('input', () => {
      if (!isNaN(audio.duration)) audio.currentTime = (seek.value / 100) * audio.duration;
    });
  }

  function updatePlayButton() { if (!playBtn || !audio) return; playBtn.textContent = audio.paused ? "⏵" : "⏸"; }

  // Join Room modal logic
  const joinBtn = document.getElementById('joinRoomBtn');
  const modal = document.getElementById('joinModal');
  const closeModalBtn = document.getElementById('closeModal');
  const confirmJoin = document.getElementById('confirmJoin');

  window.openJoinModal = function() {
    if (modal) modal.classList.add('show');
  };
  window.closeJoinModal = function() {
    if (modal) modal.classList.remove('show');
  };

  if (joinBtn) joinBtn.addEventListener('click', (e)=>{ e.preventDefault(); openJoinModal(); });
  if (closeModalBtn) closeModalBtn.addEventListener('click', (e)=>{ e.preventDefault(); closeJoinModal(); });
  if (confirmJoin) confirmJoin.addEventListener('click', (e)=>{ 
    e.preventDefault();
    // For demo, simply close and navigate to /player?join=1 (or trigger WebApp join if needed)
    closeJoinModal();
    // Optionally open player and set live param
    window.location.href = "/player?join=1";
  });

  // If Telegram WebApp available, try to read user and set album/avatar/title
  try {
    if (window.Telegram && window.Telegram.WebApp) {
      const tg = window.Telegram.WebApp;
      const user = tg.initDataUnsafe && tg.initDataUnsafe.user;
      if (user) {
        // if on profile page, it'll update from server-side JS.
        // On home, if user has photo, show it as album thumb
        const avatar = user.photo_url || user.photo;
        if (avatar && document.getElementById('main-thumb')) {
          document.getElementById('main-thumb').src = avatar;
        }
        const name = user.username || user.first_name;
        if (name && document.getElementById('pageTitle')) {
          document.getElementById('pageTitle').textContent = name + " Room";
        }
      }
    }
  } catch(e){}
});
