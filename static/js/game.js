socket.on('question', function (q) {
    console.log('got a question for the teacher:'+q)
})

var scoreOne = 0;
var scoreTwo = 0;
var question;

function updateScores() {
    $('.score-one').text(scoreOne)
    $('.score-two').text(scoreTwo)
}

updateScores()

$('.board .question').click(function() {
    var question_text = $(this).children('.question-text').text();
    var answer = atob($(this).children('.answer').text());
    var category = $(this).siblings('.category-title').text();

    question = {
        question: question_text,
        answer: answer,
        category: category
    }

    $('.modal-wrap').slideDown();

    $('.modal .question').text(question_text);
    $('.modal .question-category').text(category);
});

$('.modal-blanket, .close').click(function() {
    $('.modal-wrap').slideUp(function() {
        $('.modal-question').attr('style', '');
        $('.timer').replaceWith($clone.clone());
        someone_buzzed = false;
    });
});

// Buzzing
var default_time = 0;
var someone_buzzed = false;
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
        $timer.animate({
            fontSize: '5em'
        });
        $timer.text('Time\'s Up!');
    });
}

function answer(player_num) {
    someone_buzzed = true;
    $('.player-num').text(player_num);
    console.log(socket);
    socket.emit('new question', question)
    start_timer();
}

$(document).keypress(function(e) {
    if (!someone_buzzed) {
        if (e.key == 'z') answer(1);
        if (e.key == 'm') answer(2);
    }
});
