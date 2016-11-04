// Flashes
$('.flashes').fadeIn();

$('.flashes').mouseenter(function() {
    $(this).fadeOut();
});

setTimeout(function() {
    $('.flashes').fadeOut();
}, 3000);
