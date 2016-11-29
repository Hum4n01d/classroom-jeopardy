var question;

function update(new_question) {
    $('.question-text').text(new_question.question);
    $('.answer').text(new_question.answer);
    $('.buttons').show();

    $('.allow-buzzing').show()
    $('.after-buzz').hide();

    $('.question').slideDown();
    $('.no-messages').hide();
}

function toggle() {
    $('.question').slideToggle(function () {
       $('.no-messages').fadeToggle();
    });
}

socket.on('question', function (new_question) {
    question = JSON.parse(new_question);
    update(question);
});

socket.on('close question', function () {
    $('.question').slideUp();
    $('.no-messages').fadeIn();
});

$('.correct').click(function(event) {
    socket.emit('correct', question);

    toggle();
});

$('.incorrect').click(function(event) {
    socket.emit('incorrect', question);
    toggle();
});

$('.no-answer').click(function(event) {
    socket.emit('no answer', question);
    toggle();
});

$('.allow-buzzing').click(function () {
    socket.emit('start buzzing', question);

    $('.allow-buzzing').fadeOut(function () {
        $('.after-buzz').fadeIn();
    });
});