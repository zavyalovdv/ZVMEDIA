jQuery(document).ready(initBooksLibrary)

function initBooksLibrary() {
    let cookie = getCookie('csrftoken')
    initBookTable()
}

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


function initBookTable() {
    let table = new DataTable('#books-table', {
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

    // Make table body scrollable within container
    $('.dt-scroll-body, .dataTables_scrollBody').css({
        'max-height': 'calc(100vh - ' + (60 + 100) + 'px)',
        'overflow-y': 'auto'
    });

    $('#searchbox').on('keyup input', function () {
        table.search($(this).val()).draw();
    });



    // Favorites filter toggle
    let favoritesOnly = false;
    $('#toggle-favorites').on('click', function () {
        favoritesOnly = !favoritesOnly;
        $(this).toggleClass('btn-accent', favoritesOnly);
        $(this).toggleClass('btn-ghost', !favoritesOnly);
        if (favoritesOnly) {
            $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
                return $(table.row(dataIndex).node()).find('.bi-star-fill').length > 0;
            });
        } else {
            $.fn.dataTable.ext.search.pop();
        }
        table.draw();
    });

    // Fix dropdown position — use fixed positioning relative to button
    document.addEventListener('shown.bs.dropdown', function (e) {
        const menu = e.target.querySelector('.dropdown-menu');
        if (!menu) return;
        const btn = e.target.querySelector('[data-bs-toggle="dropdown"]');
        const rect = btn.getBoundingClientRect();
        menu.style.position = 'fixed';
        menu.style.top = (rect.top - menu.offsetHeight - 4) + 'px';
        menu.style.left = (rect.right - menu.offsetWidth) + 'px';
        menu.style.margin = '0';
    });
}

async function deleteBook(slug) {
    if (!confirm('Реально удалить книгу? Восстановить не получится.')) return;

    const response = await fetch(`/books/removebook/${slug}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
    });

    if (response.redirected) {
        // Если Django ответил redirect("books"), браузер перейдет туда
        window.location.href = response.url;
    } else {
        const data = await response.json();
        if (data.state === false) {
            alert('Ошибка при удалении');
        }
    }
}

