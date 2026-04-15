$(document).ready(function () {
    let cookie = getCookie('csrftoken')
    initBooksLibrary();
});

function initBooksLibrary() {
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
    let table = $('#books-table').DataTable({
        paging: false,
        searching: true,
        dom: 't',
        scrollX: true,
        scrollY: 'calc(100vh - 250px)', // Регулируй это число под свой футер/хедер
        scrollCollapse: true,
        autoWidth: false, // Обязательно false
        order: [],
    });

    $('#searchbox').on('keyup input', function () {
        table.search($(this).val()).draw();
    });


    // // Favorites filter toggle
    // let favoritesOnly = false;
    // $('#toggle-favorites').on('click', function () {
    //     favoritesOnly = !favoritesOnly;
    //     $(this).toggleClass('btn-accent', favoritesOnly);
    //     $(this).toggleClass('btn-ghost', !favoritesOnly);
    //     if (favoritesOnly) {
    //         $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
    //             return $(table.row(dataIndex).node()).find('.bi-star-fill').length > 0;
    //         });
    //     } else {
    //         $.fn.dataTable.ext.search.pop();
    //     }
    //     table.draw();
    // });

    // // Fix dropdown position — use fixed positioning relative to button
    // document.addEventListener('shown.bs.dropdown', function (e) {
    //     const menu = e.target.querySelector('.dropdown-menu');
    //     if (!menu) return;
    //     const btn = e.target.querySelector('[data-bs-toggle="dropdown"]');
    //     const rect = btn.getBoundingClientRect();
    //     menu.style.position = 'fixed';
    //     menu.style.top = (rect.top - menu.offsetHeight - 4) + 'px';
    //     menu.style.left = (rect.right - menu.offsetWidth) + 'px';
    //     menu.style.margin = '0';
    // });

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

}