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
        this.player.onended = () => this.playNext();
    }

    handleTablePlay(e) {
        // e может быть как событием, так и просто элементом
        const btn = this.$(e.currentTarget || e);
        const url = btn.data('url');
        const row = btn.closest('tr');

        // Обновляем текст
        this.updatePlayerInfo(row);

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
        // 1. Главная кнопка в плеере
        this.playPauseBtn.innerHTML = isPlaying ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';

        // 2. Сбрасываем ВСЕ иконки в таблице на Play
        this.$('.btn-play-track i').removeClass('fa-pause').addClass('fa-play');

        // 3. Если что-то играет, находим НУЖНУЮ кнопку
        if (isPlaying && this.player.src) {
            try {
                // Превращаем полный URL плеера в относительный путь (/media/...)
                const urlPath = new URL(this.player.src).pathname;

                // Ищем кнопку через фильтр (это надежнее всего)
                const activeBtn = this.$('.btn-play-track').filter((i, btn) => {
                    // Очищаем атрибут от возможных лишних пробелов
                    return this.$(btn).data('url').trim() === urlPath;
                });

                // Меняем иконку именно у этой кнопки
                activeBtn.find('i').removeClass('fa-play').addClass('fa-pause');

                // Доп. фишка: можно подсветить всю строку
                this.$('tr').removeClass('table-active');
                activeBtn.closest('tr').addClass('table-active');

            } catch (e) {
                console.error("UI Update Error:", e);
            }
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

    playNext() {
        try {
            const currentPath = new URL(this.player.src).pathname;
            const allBtns = this.$('.btn-play-track');

            // Находим индекс текущей кнопки
            let currentIndex = -1;
            allBtns.each((index, btn) => {
                if (this.$(btn).data('url') === currentPath) {
                    currentIndex = index;
                    return false;
                }
            });

            if (currentIndex !== -1 && currentIndex < allBtns.length - 1) {
                const nextBtn = allBtns.eq(currentIndex + 1);

                // ВАЖНО: Передаем саму кнопку в handleTablePlay напрямую
                this.handleTablePlay(nextBtn[0]);
            }
        } catch (e) {
            console.error("Ошибка при переключении трека:", e);
        }
    }

    updatePlayerInfo(row) {
        // Вытаскиваем текст из первой и второй колонок (Track и Artist)
        const title = row.find('td:eq(0)').text().trim();
        const artist = row.find('td:eq(1)').text().trim();

        this.trackTitle.text(title);
        this.trackArtist.text(artist);
    }
}

jQuery(document).ready(function ($) {
    window.app = new MusicApp($);
});