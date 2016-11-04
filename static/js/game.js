$('.board .question').click(function() {
    var question = $(this).children('.question-text').text();
    var category = $(this).siblings('.category-title').text();
    var $els = $('.modal, .modal-blanket');

    $els.show();
    $els.addClass('in');

    $('.modal .question').text(question);
    $('.modal .question-category').text(category);
});

$('.modal-blanket').click(function() {
    $('.modal, .modal-blanket').removeClass('in');
});

// Buzzing
var default_time = 2;
var someone_buzzed = false;

function start_timer() {
    var current_time = default_time;
    var $timer = $('.timer-text');

    $('.timer').show();

    for (i = default_time+1; i > 0; i--) {
        $timer.text(current_time);

        $timer.animate({
            // fontSize: '6em',
            opacity: 1
        }, 1000, function() {
            $timer.css({
                // fontSize: '4em',
                opacity: 0
            });

            current_time--;
            $timer.text(current_time);
        });
    }

    $timer.promise().done(function () {
        $timer.animate({
            opacity: 1
        }, 500);
        // $('.timer > *:not(".timer-text")').fadeOut();
        $timer.text('Time\'s Up!');
    });
}

function answer(player_num) {
    someone_buzzed = true;
    $('.player-num').text(player_num);
    start_timer();
}

$(document).keypress(function(e) {
    if (!someone_buzzed) {
        if (e.key == 'z') answer(1);
        if (e.key == 'm') answer(2);
    }
});
