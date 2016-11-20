// Buzzing
var default_time = 5;
// var default_time = 0;
var someone_buzzed = false;
var $clone = $('.timer').clone();

var playerOneScore = 0;
var playerTwoScore = 0;

var question;
var $questionEl;

function updateScores() {
    $('.score-one').text(playerOneScore);
    $('.score-two').text(playerTwoScore)
}

updateScores();

function renderQuestion(question) {
    $('.close').fadeIn();

    $('.question-wrap').slideDown();
    $('.question').fadeIn();

    var $question_el = $('.question .question-text');

    $('.question .question-category').text(question.category)

    if ($question_el.is('input')) {
        console.log('its an input. val: '+question.question);
        $question_el.val(question.question);
    } else {
        $question_el.text(question.question);
    }
}

function closeQuestion() {
    someone_buzzed = false;
    $('.question-wrap').slideUp(function() {
        $('.question-question').attr('style', '');
        $('.timer').replaceWith($clone.clone());
        someone_buzzed = false;
    });
}

function start_timer($timer) {
    var current_time = default_time;

    for (i = default_time+1; i > 0; i--) {
        $timer.text(current_time);

        $timer.animate({
            opacity: 1
        }, 1000, function() {
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
    $questionEl.addClass('disabled');

    player_buzzed = player_num;
    someone_buzzed = true;
    $('.player-num').text(player_num);

    socket.emit('new question', question);

    $('.close').fadeOut();

    $('.timer-content').fadeIn();
    $('.timer-instructions').hide();

    start_timer($('.timer-text'));
}


$('.game .board-question').click(function() {
    if ($(this).hasClass('disabled')) return false;

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

    renderQuestion(question);
});

$('.question-blanket, .close').click(function() {
    if (!someone_buzzed) closeQuestion();
});

// Detect keypresses. For some reason jQuery didn't work in safari
var listener = new window.keypress.Listener();

listener.simple_combo("z", function() {
    if (!someone_buzzed) answer(1)
});
listener.simple_combo("m", function() {
    if (!someone_buzzed) answer(2)
});

function handle_answer(question, correct) {
    value = parseInt(question.value);

    if (!correct) value = 0 - value;

    if (player_buzzed == 1) playerOneScore += value;
    else if (player_buzzed == 2) playerTwoScore += value;

    updateScores();

    var result;
    var $celebration = $('.celebration');
    $celebration.removeClass('correct incorrect');

    if (correct) {
        result = 'Correct!';
        $celebration.addClass('correct');
    }  else {
        result = 'Incorrect';
        $celebration.addClass('incorrect');
    }

    $('.celebration-wrap').css('display', 'flex');

    $('.question').slideUp();

    $celebration.text(result).fadeIn();

    $celebration.animate({
        fontSize: '6em'
    }, 1000, function () {
        someone_buzzed = false;
        $('.celebration-wrap').hide();
        closeQuestion();
        $('.question-wrap').delay(2000).slideUp();
    });
}

// Once teacher answers
socket.on('correct', function (question) {
    handle_answer(question, true);
});
socket.on('incorrect', function (question) {
    handle_answer(question, false);
});


// Create
$('.create-board .board-question').click(function () {
    // document.write('test')
    question = {
        value: $(this).children('.value').val(),
        question: 'Question text',
        answer: 'Question answer',
        category: $(this).siblings('.category-title').val()
    };
    renderQuestion(question);
});