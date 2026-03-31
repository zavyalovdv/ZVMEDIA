function exec() {
    console.log("Hello from Django")
    $("#id_author").addClass("form-control")
    setFavoritesListener()

}
function setFavoritesListener() {
    objectsFavorite = document.querySelectorAll('tbody .bi')
    objectsFavorite.forEach((object) => {
        object.addEventListener('click', () => {
            changeFavotites(object)
        })
    })
}


function changeFavotites(object) {
    snippetsFavorites = {
        "noFavorites": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16"><path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z"/></svg>',
        "favorites": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16"><path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/></svg>',
    }
    let currentStatus = $(object).attr("favorites")
    let slug = $(object).attr("slug")
    if (currentStatus == "True") {
        is_favorites = "False"
    } else {
        is_favorites = "True"
    }
    $.ajax({
        data: { 'is_favorites': is_favorites, 'slug': slug },
        url: '/books/changefavorite/',
        success: function (response) {
            if (response.is_taken == true) {
                if (currentStatus == "True") {
                    $(object).replaceWith(snippetsFavorites["noFavorites"])
                } else {
                    $(object).replaceWith(snippetsFavorites["favorites"])
                }
                findChanges = document.querySelectorAll('tbody .bi')
                findChanges.forEach((newobject) => {
                    if (!(newobject.hasAttribute('favorites'))) {
                        object = newobject
                        $(object).attr('slug', slug)
                        $(object).attr('favorites', is_favorites)
                        console.log(currentStatus)
                        setFavoritesListener()
                        if (currentStatus == "True") {
                            showNotify("Удалено из избранного", "error")
                        } else {
                            showNotify("Добавлено в избранное", "success")
                        }
                    }
                })
            }
        },
        error: function (response) {
            console.log(response.responseJSON.errors)
            showNotify("Не добавлено в избранное", "error")
        }
    });
    return false;

    function showNotify(notifyMessage, notifyClass) {
        $.notify(notifyMessage, {
            clickToHide: true,
            autoHide: true,
            autoHideDelay: 1000,
            arrowShow: true,
            arrowSize: 5,
            position: 'bottom right',
            elementPosition: 'bottom right',
            globalPosition: 'bottom right',
            style: 'bootstrap',
            className: notifyClass,
            showAnimation: 'slideDown',
            showDuration: 200,
            hideAnimation: 'slideUp',
            hideDuration: 100,
            gap: 2,
        });
    }
}

// function saveBook(){
//     $.ajax({
//         data: { 'file': file},
//         url: '/books/setpdf/',
//         type: 'post',
//         success: function (response) {
//             if (response.is_taken == true) {
//                 if (currentStatus == "True") {
//                     $(object).replaceWith(snippetsFavorites["noFavorites"])
//                 } else {
//                     $(object).replaceWith(snippetsFavorites["favorites"])
//                 }
//                 findChanges = document.querySelectorAll('tbody .bi')
//                 findChanges.forEach((newobject) => {
//                     if (!(newobject.hasAttribute('favorites'))) {
//                         object = newobject
//                         $(object).attr('slug', slug)
//                         $(object).attr('favorites', is_favorites)
//                         setFavoritesListener()
//                     }
//                 })
//             }
//         },
//         error: function (response) {
//             console.log(response.responseJSON.errors)
//         }
//     });
//     return false;
//   }



$(document).ready(exec())
