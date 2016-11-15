var socket = io.connect('http://' + document.domain + ':' + location.port);

// Flashes
$('.flashes').fadeIn();

$('.flashes').mouseenter(function() {
    $(this).fadeOut();
});

setTimeout(function() {
    $('.flashes').fadeOut();
}, 3000);
