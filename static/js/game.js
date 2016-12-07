var defaultTime = 5;
var playerWhoBuzzed;
var someoneBuzzed = false;
var youCanBuzz = false;

// Who starts the game (random)
var whosTurn = Math.floor(Math.random()*2) + 1;

var $currentQuestionEl;
var $timerClone = $('.timer').clone();

var playerOneScore = 0;
var playerTwoScore = 0;

function updateWhosTurn() {
    $('.whos-turn-text').text(whosTurn);

    $('.whos-turn').animate({
        fontSize: '1.75em'
    }, 500, function () {
        $(this).animate({
            fontSize: '1.5em'
        }, 500);
    });
}

function toggleWhosTurn() {
    if (whosTurn == 1) {
        whosTurn = 2
    } else if (whosTurn == 2) {
        whosTurn = 1
    }
    updateWhosTurn();
}

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

    someoneBuzzed = false;

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

function answer(playerNum) {
    playerWhoBuzzed = playerNum;
    someoneBuzzed = true;
    youCanBuzz = false;

    $('.player-num').text(playerNum);
    $('.close').fadeOut();

    $('.timer-instructions').fadeOut(function () {
        $('.timer-content').slideDown(function () {
            startTimer(defaultTime);
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
    var questionText = $el.children('.question-text').text();
    var answer = atob($el.children('.answer').text());
    var category = $el.siblings('.category-title').text();

    question = {
        value: value,
        question: questionText,
        answer: answer,
        category: category
    };

    return question
}

function gameFlash(text, $parentEl, className, length) {
    if (length == undefined) length = 1;
    if ($parentEl == undefined) $parentEl = $('.main-body');

    var $gameFlashText = $('<div>').addClass('game-flash').append($('<p>').addClass('game-flash-text'));
    $('.main-body').append($gameFlashText);

    $gameFlashText.removeClass('correct incorrect no-answer');
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

            $(this).remove();
        });
    });
}

function handleAnswer(question, correct) {
    var noAnswer = correct == 'no_answer';

    var result = 'Error';
    var className;

    if (!noAnswer) {
        var value = parseInt(question.value);

        if (!correct) value = 0 - value;
        if (playerWhoBuzzed == 1) playerOneScore += value;
        else if (playerWhoBuzzed == 2) playerTwoScore += value;
    }

    if (noAnswer) {
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
    if (!someoneBuzzed) closeQuestionModal();
});

socket.on('start buzzing', function (question) {
    $('.question-modal-text').text(question.question);
    $('.question .status').text('');

    $('.timer-instructions').fadeIn(function () {
        youCanBuzz = true;
    });
});

// Buzzing detection
$(document).keydown(function (e) {
    if (youCanBuzz) {
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