var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

// Flashes
var $flashes = $('.flashes');

$flashes.fadeIn();

$flashes.mouseenter(function() {
    $(this).fadeOut();
});

setTimeout(function() {
    $flashes.fadeOut();
}, 3000);

$('.delete-board').click(function (e) {
    e.preventDefault();

    if (confirm('Are you sure you want to delete this board?')) {
        window.location = $(this).attr('href');
    }
});