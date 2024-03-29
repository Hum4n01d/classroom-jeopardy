// Buzzing
var default_time = 5;
// var default_time = 0;
var player_buzzed;
var someone_buzzed = false;
var you_can_buzz = false;
var $clone = $('.timer').clone();

var playerOneScore = 0;
var playerTwoScore = 0;

var question;
var $questionEl;
var $elForDisabling;



function closeQuestion() {
    someone_buzzed = false;
    you_can_buzz = false;

    socket.emit('close_question');

    $('.celebration-wrap').hide();
    $('.question').fadeOut();
    $('.question-wrap').slideUp(function () {
        $('.question-question').attr('style', '');
        $('.timer').replaceWith($clone.clone());
        someone_buzzed = false;
    });
}

function start_timer($timer) {
    var current_time = default_time;

    for (i = default_time + 1; i > 0; i--) {
        $timer.text(current_time);

        $timer.animate({
            opacity: 1
        }, 1000, function () {
            $timer.css({
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

        $timer.text('Time\'s Up!');
    });
}

function answer(player_num) {
    if (!you_can_buzz) return false;

    player_buzzed = player_num;
    someone_buzzed = true;
    you_can_buzz = false;

    $('.player-num').text(player_num);

    $('.close').fadeOut();

    $('.timer-content').fadeIn();
    $('.timer-instructions').hide();

    start_timer($('.timer-text'));
}

function handle_answer(question, correct) {
    var value;
    var result;
    var $celebration = $('.celebration');
    var no_answer = correct == 'no_answer';

    if (!no_answer) {
        value = parseInt(question.value);

        if (!correct) value = 0 - value;
        if (player_buzzed == 1) playerOneScore += value;
        else if (player_buzzed == 2) playerTwoScore += value;
    }

    $celebration.removeClass('correct incorrect no-answer');

    if (no_answer) {
        result = 'No answer';
        $celebration.addClass('no-answer');
    } else if (correct) {
        result = 'Correct!';
        $celebration.addClass('correct');
    } else {
        result = 'Incorrect';
        $celebration.addClass('incorrect');
    }

    $('.celebration-wrap').css('display', 'flex');

    $('.question').fadeOut();

    $celebration.text(result).fadeIn();

    $celebration.css('font-size', '5em');

    $celebration.animate({
        fontSize: '6em'
    }, 1000, function () {
        someone_buzzed = false;

        setTimeout(function () {
            closeQuestion();
            $elForDisabling.addClass('disabled');

            setTimeout(function () {
                updateScores();
            }, 500);
        }, 1000);
    });
}

$('.game .board-question').click(function () {
    if ($(this).hasClass('disabled')) return false;


    $elForDisabling = $(this);

    var value = $(this).children('.value').text();
    var question_text = $(this).children('.question-text').text();
    var answer = atob($(this).children('.answer').text());
    var category = $(this).siblings('.category-title').text();


    question = {
        value: value,
        question: question_text,
        answer: answer,
        category: category
    };

    $('.close').fadeIn();

    $('.question-wrap').slideDown(function () {
        you_can_buzz = true;
        socket.emit('new question', question);
    });
    $('.question').fadeIn();

    $questionEl = $('.question .question-text');

    $('.question .question-category').text(question.category)

    $questionEl.text(question.question);
});

$('.question-blanket, .close').click(function () {
    if (!someone_buzzed) closeQuestion();
});

$(document).keydown(function (e) {
    if (you_can_buzz) {
        if (e.which == 90) answer(1);
        if (e.which == 77) answer(2);
    }
});

// Once teacher answers
socket.on('correct', function (question) {
    handle_answer(question, true);
});
socket.on('incorrect', function (question) {
    handle_answer(question, false);
});
socket.on('no_answer', function (question) {
    handle_answer(question, 'no_answer');
});