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
