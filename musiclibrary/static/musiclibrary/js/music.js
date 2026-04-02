class MusicApp {
    constructor($jq) {
        // Передаем конкретный экземпляр jQuery
        this.$ = $jq;

        this.player = document.getElementById('global-audio-player');
        this.playPauseBtn = document.getElementById('player-play-pause');
        this.progressBar = document.getElementById('progress-bar');
        this.volumeBar = document.getElementById('volume-bar');
        this.currentTimeEl = document.getElementById('current-time');
        this.durationTimeEl = document.getElementById('duration-time');

        this.trackTitle = this.$('#player-track-title');
        this.trackArtist = this.$('#player-track-artist');

        this.init();
    }

    init() {
        if (!this.player) return;
        this.initDataTable();
        this.bindEvents();
    }

    initDataTable() {
        // Вызываем DataTable через проверенный экземпляр
        this.table = this.$('#music-table').DataTable({
            paging: false,
            select: true,
            scrollX: true,
            dom: 't',
            order: [],
            columnDefs: [{ targets: '_all', className: 'dt-body-left' }]
        });
    }

    bindEvents() {
        // Делегируем события через $jq
        this.$(document).on('click', '.btn-play-track', (e) => this.handleTablePlay(e));

        this.playPauseBtn.addEventListener('click', () => this.togglePlay());
        this.player.ontimeupdate = () => this.updateProgress();
        this.progressBar.addEventListener('input', () => this.seek());
        this.volumeBar.addEventListener('input', () => this.setVolume());

        this.player.onplay = () => this.updateUI(true);
        this.player.onpause = () => this.updateUI(false);
    }

    handleTablePlay(e) {
        const btn = this.$(e.currentTarget);
        const url = btn.data('url');
        // ... остальной код
        this.currentTrackUrl = url; // Запоминаем, что мы включили

        if (this.player.src.endsWith(url)) {
            this.togglePlay();
        } else {
            this.player.src = url;
            this.player.play();
        }
    }

    togglePlay() {
        if (this.player.paused) this.player.play();
        else this.player.pause();
    }

    updateProgress() {
        const per = (this.player.currentTime / this.player.duration) * 100;
        this.progressBar.value = per || 0;
        this.currentTimeEl.textContent = this.formatTime(this.player.currentTime);
        if (!isNaN(this.player.duration)) {
            this.durationTimeEl.textContent = this.formatTime(this.player.duration);
        }
    }


    updateUI(isPlaying) {
        this.playPauseBtn.innerHTML = isPlaying ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';
        this.$('.btn-play-track i').removeClass('fa-pause').addClass('fa-play');

        if (isPlaying && this.currentTrackUrl) {
            // Ищем по сохраненному относительному пути
            this.$(`.btn-play-track[data-url="${this.currentTrackUrl}"] i`)
                .removeClass('fa-play')
                .addClass('fa-pause');
        }
    }

    seek() {
        this.player.currentTime = (this.progressBar.value / 100) * this.player.duration;
    }

    setVolume() {
        this.player.volume = this.volumeBar.value / 100;
    }

    formatTime(seconds) {
        const min = Math.floor(seconds / 60);
        const sec = Math.floor(seconds % 60);
        return `${min}:${sec < 10 ? '0' + sec : sec}`;
    }
}

jQuery(document).ready(function ($) {
    window.app = new MusicApp($);
});