var default_time = 5;
var player_who_buzzed;
var someone_buzzed = false;
var you_can_buzz = false;

var $currentQuestionEl;
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

function closeQuestionModal(delay, callback) {
    if (delay == undefined) delay = 0;

    someone_buzzed = false;

    $('.question').fadeOut();

    setTimeout(function () {
        $('.question-wrap').slideUp(function () {
            $('.timer').replaceWith($timerClone.clone());

            if (typeof(callback) == "function") callback();
            socket.emit('close question');
        });
    }, delay*1000);
}

function openQuestionModal(question) {
    $('.close').fadeIn();

    $('.question-wrap').slideDown();
    $('.question').fadeIn();
    $('.question .question-category').text(question.category);
    $('.timer-instructions').hide();

    $('.question-modal-text').text(question.question);
    $('.question .status').text('Waiting for teacher...');

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

    $currentQuestionEl.addClass('disabled');

    function updateTimer() {
        gameFlash(secondsLeft, 'show-timer');
    }

    function timesUp() {
        var $el = $('<h1>').text("Time's Up!");

        $('.timer-content').addClass('times-up').append($el);
    }

    updateTimer();

    var timer = setInterval(function () {
        secondsLeft--;

        updateTimer();

        if (secondsLeft == 0) {
            clearInterval(timer);

            setTimeout(function () {
                timesUp();
            }, 1000);
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

function gameFlash(text, className, length) {
    if (length == undefined) length = 1;

    var $gameFlashText = $('.game-flash-text');

    $gameFlashText.addClass(className);

    $gameFlashText.parent().toggleClass('show '+className);

    $gameFlashText.text(text).show();

    $gameFlashText.animate({
        fontSize: '4em',
        opacity: 1
    }, length*1000/2, function () {
        $gameFlashText.animate({
            fontSize: '3em',
            opacity: 0
        }, length*1000/2, function () {
            $gameFlashText.parent().toggleClass('show '+className);
        });
    });
}

function handleAnswer(question, correct) {
    var no_answer = correct == 'no_answer';

    var result = 'Error';
    var className;

    if (!no_answer) {
        var value = parseInt(question.value);

        if (!correct) value = 0 - value;
        if (player_who_buzzed == 1) playerOneScore += value;
        else if (player_who_buzzed == 2) playerTwoScore += value;
    }

    if (no_answer) {
        result = 'No answer';
        className = ('no-answer');
    } else if (correct) {
        result = 'Correct!';
        className = ('correct');
    } else {
        result = 'Incorrect';
        className = ('incorrect');
    }

    gameFlash(result, className, 3);
    closeQuestionModal(2.5, function () {
        updateScores();
    });
}

updateScores();

$('.game .board-question:not(.disabled)').click(function () {
    var question = getQuestionFromEl($(this));

    $currentQuestionEl = $(this);

    socket.emit('new question', question);

    openQuestionModal(question);
});

$('.question-blanket, .close').click(function () {
    if (!someone_buzzed) closeQuestionModal();
});

socket.on('start buzzing', function (question) {
    $('.question-modal-text').text(question.question);
    $('.question .status').text('');

    $('.timer-instructions').fadeIn(function () {
        you_can_buzz = true;
    });
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
    handleAnswer(question, true);
});
socket.on('incorrect', function (question) {
    handleAnswer(question, false);
});
socket.on('no answer', function (question) {
    handleAnswer(question, 'no_answer');
});