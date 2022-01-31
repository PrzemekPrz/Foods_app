// Script makes buttons visible only on urls /recipe/<id>/

document.addEventListener('DOMContentLoaded', function () {
    const reg = /\/recipe\/list\//;
    const like = document.querySelectorAll('#search');
    if (Boolean(window.location.pathname.match(reg))) {
        like.forEach(function (element) {
            element.style.display = 'block'
        });
    } else {
        like.forEach(function (element) {
            element.style.display = 'none';
        });
    }
});