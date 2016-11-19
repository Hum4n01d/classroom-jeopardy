// Buzzing
// var default_time = 5;
var default_time = 0;
var someone_buzzed = false;
var $clone = $('.timer').clone();

var teamOneScore = 0;
var teamTwoScore = 0;

var question;
var $questionEl;

function updateScores() {
    $('.score-one').text(teamOneScore);
    $('.score-two').text(teamTwoScore)
}

updateScores();

$('.board-question').click(function() {
    if ($(this).hasClass('disabled')) return false;

    $('.close').fadeIn();

    $questionEl = $(this);

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

    $('.question-wrap').slideDown();

    $('.question h1.question-text').text(question_text);
    $('.question .question-category').text(category);
});

$('.question-blanket, .close').click(function() {
    if (!someone_buzzed) closequestion();
});

function closequestion() {
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

        $('.question-question').hide();
        $timer.text('Time\'s Up!');
    });
}

function answer(team_num) {
    $questionEl.addClass('disabled');

    team_buzzed = team_num;
    someone_buzzed = true;
    $('.player-num').text(team_num);

    socket.emit('new question', question);

    $('.close').fadeOut();

    $('.timer-content').fadeIn();
    $('.timer-instructions').hide();

    start_timer($('.timer-text'));
}

$(document).keypress(function(e) {
    if (!someone_buzzed) {
        if (e.key == 'z') answer(1);
        if (e.key == 'm') answer(2);
    }
});

function handle_answer(question, correct) {
    value = parseInt(question.value);

    if (!correct) value = 0 - value;

    if (team_buzzed == 1) teamOneScore += value;
    else if (team_buzzed == 2) teamTwoScore += value;

    updateScores();
    closequestion();
}

// Once teacher answers
socket.on('correct', function (question) {
    handle_answer(question, true);
});
socket.on('incorrect', function (question) {
    handle_answer(question, false);
});
