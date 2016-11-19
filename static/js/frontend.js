var socket = io.connect('https://' + document.domain + ':' + location.port);

// Flashes
$('.flashes').fadeIn();

$('.flashes').mouseenter(function() {
    $(this).fadeOut();
});

setTimeout(function() {
    $('.flashes').fadeOut();
}, 3000);
