var question;

function update(new_question) {
    $('.question-text').text(new_question.question);
    $('.answer').text(new_question.answer);
    $('.buttons').show();

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

$('.correct').click(function(event) {
    socket.emit('correct', question);

    toggle();
});

$('.incorrect').click(function(event) {
    socket.emit('incorrect', question);
    toggle();
});
