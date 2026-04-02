
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function () {
    const player = document.getElementById('global-audio-player');

    if (!player) {
        console.error("Критическая ошибка: Элемент #global-audio-player не найден в DOM!");
    } else {
        console.log("Плеер инициализирован");
    }

    // ... остальной код из прошлого ответа ...
});
const player = document.getElementById('global-audio-player');
const playPauseBtn = document.getElementById('player-play-pause');
const progressBar = document.getElementById('progress-bar');
const volumeBar = document.getElementById('volume-bar');
const currentTimeEl = document.getElementById('current-time');
const durationTimeEl = document.getElementById('duration-time');

// Функция форматирования времени (секунды -> 0:00)
function formatTime(seconds) {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec < 10 ? '0' + sec : sec}`;
}

let table = $('#music-table').DataTable({
    paging: false,
    select: true,
    scrollX: true,
    scrollCollapse: true,
    searching: true,
    dom: 't',
    autoWidth: false,
    order: [],
    columnDefs: [
        { targets: '_all', className: 'dt-body-left', orderable: true },
        { targets: [12, 13], orderable: false },
    ]
});

// Клик по кнопке Play в таблице
$('#music-table').on('click', '.btn-play-track', function () {
    const btn = $(this);
    const url = btn.data('url');
    const row = btn.closest('tr');

    // Обновляем инфо в плеере
    $('#player-track-title').text(row.find('td:eq(0)').text().trim());
    $('#player-track-artist').text(row.find('td:eq(1)').text().trim());

    if (player.src.endsWith(url)) {
        if (player.paused) player.play();
        else player.pause();
    } else {
        player.src = url;
        player.play();
    }
});

// Клик по главной кнопке Play/Pause в баре
playPauseBtn.addEventListener('click', () => {
    if (player.paused) player.play();
    else player.pause();
});

// Обновление состояния кнопок
player.onplay = () => {
    playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
    $('.btn-play-track i').removeClass('fa-pause').addClass('fa-play');
    // Ищем кнопку в таблице по URL и меняем ей иконку
    $(`.btn-play-track[data-url="${player.getAttribute('src')}"] i`).addClass('fa-pause');
};

player.onpause = () => {
    playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
    $('.btn-play-track i').removeClass('fa-pause').addClass('fa-play');
};

// Обновление прогресс-бара
player.ontimeupdate = () => {
    const per = (player.currentTime / player.duration) * 100;
    progressBar.value = per || 0;
    currentTimeEl.textContent = formatTime(player.currentTime);
    if (!isNaN(player.duration)) {
        durationTimeEl.textContent = formatTime(player.duration);
    }
};

// Перемотка
progressBar.addEventListener('input', () => {
    const time = (progressBar.value / 100) * player.duration;
    player.currentTime = time;
});

// Громкость
volumeBar.addEventListener('input', () => {
    player.volume = volumeBar.value / 100;
});
