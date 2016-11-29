var default_time = 5;
var player_who_buzzed;
var someone_buzzed = false;
var you_can_buzz = false;
var $timerClone = $('.timer').clone();

var playerOneScore = 0;
var playerTwoScore = 0;

function updateScores() {
    $('.score-one').text(playerOneScore);
    $('.score-two').text(playerTwoScore);

    if (playerOneScore == 0 && playerTwoScore == 0) {
        $('.scores').fadeIn();
    } else {
        $('.score-one, .score-two').animate({
            fontSize: '1.5em'
        }, 500, function () {
            $(this).animate({
                fontSize: '1em'
            }, 500);
        });
    }
}

function closeQuestionModal() {
    $('.question').fadeOut();
    $('.question-wrap').slideUp(function () {
        $('.timer').replaceWith($timerClone.clone());
    });

    socket.emit('close question');
}

function openQuestionModal(question) {
    $('.close').fadeIn();

    $('.question-wrap').slideDown();
    $('.question').fadeIn();
    $('.question .question-category').text(question.category);
    $('.timer-instructions').hide();

    $('.question-modal-text').text('Waiting for teacher...');
}

function answer(player_num) {
    player_who_buzzed = player_num;
    someone_buzzed = true;
    you_can_buzz = false;

    $('.player-num').text(player_num);
    $('.close').fadeOut();

    $('.timer-instructions').fadeOut(function () {
        $('.timer-content').slideDown(function () {
            startTimer(default_time);
        });
    });
}

function startTimer(seconds) {
    var secondsLeft = seconds;
    var $timer = $('.game-flash-text');

    var timer = setInterval(function () {
        secondsLeft--;

        gameFlash(secondsLeft);

        if (secondsLeft == -1) {
            clearInterval(timer);
            gameFlash("Time's Up!");
        }
    }, 1000);
}

function getQuestionFromEl($el) {
    var value = $el.children('.value').text();
    var question_text = $el.children('.question-text').text();
    var answer = atob($el.children('.answer').text());
    var category = $el.siblings('.category-title').text();
    question = {
        value: value,
        question: question_text,
        answer: answer,
        category: category
    };

    return question
}

function gameFlash(text) {
    var $gameFlashText = $('.game-flash-text');

    $gameFlashText.parent().toggleClass('show');

    $gameFlashText.text(text).show();

    $gameFlashText.animate({
        fontSize: '4em',
        opacity: 1
    }, 500, function () {
        $gameFlashText.animate({
            fontSize: '3em',
            opacity: 0
        }, 500, function () {
            $gameFlashText.parent().toggleClass('show');
        });
    });
}

updateScores();

$('.game .board-question:not(.disabled)').click(function () {
    var question = getQuestionFromEl($(this));

    socket.emit('new question', question);

    openQuestionModal(question);
});

$('.question-blanket, .close').click(function () {
    if (!someone_buzzed) closeQuestionModal();
});

socket.on('start buzzing', function (question) {
    $('.question-modal-text').text(question.question);
    $('.timer-instructions').fadeIn();
    you_can_buzz = true;
});

// Buzzing detection
$(document).keydown(function (e) {
    if (you_can_buzz) {
        if (e.which == 90) answer(1);
        if (e.which == 77) answer(2);
    }
});

// After buzzing
socket.on('correct', function (question) {
    handle_answer(question, true);
});
socket.on('incorrect', function (question) {
    handle_answer(question, false);
});
socket.on('no answer', function (question) {
    handle_answer(question, 'no_answer');
});