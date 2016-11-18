var teamOneScore = 0;
var teamTwoScore = 0;

var question;
var $questionEl;

function updateScores() {
    $('.score-one').text(teamOneScore)
    $('.score-two').text(teamTwoScore)
}

updateScores()

$('.board .question').click(function() {
    if ($(this).hasClass('disabled')) return false

    $questionEl = $(this)

    var value = $(this).children('.value').text();
    var question_text = $(this).children('.question-text').text();
    var answer = atob($(this).children('.answer').text());
    var category = $(this).siblings('.category-title').text();

    question = {
        value: value,
        question: question_text,
        answer: answer,
        category: category
    }

    $('.modal-wrap').slideDown();

    $('.modal .question').text(question_text);
    $('.modal .question-category').text(category);
});

$('.modal-blanket, .close').click(function() {
    closeModal();
});

function closeModal() {
    someone_buzzed = false;
    $('.modal-wrap').slideUp(function() {
        $('.modal-question').attr('style', '');
        $('.timer').replaceWith($clone.clone());
        someone_buzzed = false;
    });
}

// Buzzing
var default_time = 5;
var someone_buzzed = false;
var team_that_buzzed;
var $clone = $('.timer').clone();

function start_timer() {
    var current_time = default_time;
    var $timer = $('.timer-text');

    $('.timer-content').fadeIn();
    $('.timer-instructions').hide();

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

        $('.modal-question').hide();
        $timer.text('Time\'s Up!');
    });
}

function answer(team_num) {
    $questionEl.addClass('disabled')

    team_buzzed = team_num;
    someone_buzzed = true;
    $('.player-num').text(team_num);

    socket.emit('new question', question)
    start_timer();
}

$(document).keypress(function(e) {
    if (!someone_buzzed) {
        if (e.key == 'z') answer(1);
        if (e.key == 'm') answer(2);
    }
});

function handle_answer(question, correct) {
    value = parseInt(question.value);

    if (!correct) value = 0 - value

    if (team_buzzed == 1) teamOneScore += value;
    else if (team_buzzed == 2) teamTwoScore += value;

    updateScores();
    closeModal();
}

// Once teacher answers
socket.on('correct', function (question) {
    handle_answer(question, true);
})
socket.on('incorrect', function (question) {
    handle_answer(question, false);
})
