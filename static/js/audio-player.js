let audioElement = document.getElementById('audio-element');
let audioPlayerBar = document.getElementById('audio-player-bar');
let audioPlayBtn = document.getElementById('audio-play');
let audioPrevBtn = document.getElementById('audio-prev');
let audioNextBtn = document.getElementById('audio-next');
let audioSeek = document.getElementById('audio-seek');
let audioProgress = document.getElementById('audio-progress');
let audioVolume = document.getElementById('audio-volume');
let audioCurrent = document.getElementById('audio-current');
let audioDuration = document.getElementById('audio-duration');
let audioTitle = document.getElementById('audio-title');
let audioArtist = document.getElementById('audio-artist');

let playlist = [];
let currentIndex = -1;
let isPlaying = false;

// Build playlist
document.querySelectorAll('.audio-item').forEach(function(item, index) {
    playlist.push({
        element: item,
        src: item.dataset.src,
        title: item.dataset.title,
        artist: item.dataset.artist
    });
    item.addEventListener('click', function() { playTrack(index); });
});

function playTrack(index) {
    if (index < 0 || index >= playlist.length) return;
    currentIndex = index;
    const track = playlist[index];

    audioElement.src = track.src;
    audioTitle.textContent = track.title;
    audioArtist.textContent = track.artist;

    // Update active state
    playlist.forEach(function(t) { t.element.classList.remove('playing'); });
    track.element.classList.add('playing');

    audioPlayerBar.style.display = 'block';
    audioElement.play();
    isPlaying = true;
    updatePlayButton();
}

function togglePlay() {
    if (currentIndex === -1) {
        if (playlist.length > 0) playTrack(0);
        return;
    }
    if (isPlaying) {
        audioElement.pause();
        isPlaying = false;
    } else {
        audioElement.play();
        isPlaying = true;
    }
    updatePlayButton();
}

function updatePlayButton() {
    audioPlayBtn.innerHTML = isPlaying ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';
}

function prevTrack() {
    if (currentIndex > 0) playTrack(currentIndex - 1);
}

function nextTrack() {
    if (currentIndex < playlist.length - 1) playTrack(currentIndex + 1);
}

function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return mins + ':' + (secs < 10 ? '0' : '') + secs;
}

// Event listeners
if (audioPlayBtn) audioPlayBtn.addEventListener('click', togglePlay);
if (audioPrevBtn) audioPrevBtn.addEventListener('click', prevTrack);
if (audioNextBtn) audioNextBtn.addEventListener('click', nextTrack);

if (audioElement) {
    audioElement.addEventListener('timeupdate', function() {
        const progress = (audioElement.currentTime / audioElement.duration) * 100;
        audioSeek.value = progress;
        audioProgress.style.width = progress + '%';
        audioCurrent.textContent = formatTime(audioElement.currentTime);
    });

    audioElement.addEventListener('loadedmetadata', function() {
        audioDuration.textContent = formatTime(audioElement.duration);
    });

    audioElement.addEventListener('ended', function() {
        nextTrack();
    });
}

if (audioSeek) {
    audioSeek.addEventListener('input', function() {
        const time = (audioSeek.value / 100) * audioElement.duration;
        audioElement.currentTime = time;
    });
}

if (audioVolume) {
    audioVolume.addEventListener('input', function() {
        audioElement.volume = audioVolume.value / 100;
    });
    audioElement.volume = 0.8;
}
