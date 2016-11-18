var question;

function update(new_question) {
    $('.no-messages').hide();
    $('.question-text').text(new_question.question);
    $('.answer').text(new_question.answer);
    $('.buttons').show();
    $('.question').slideDown();
}

socket.on('question', function (new_question) {
    question = JSON.parse(new_question);
    update(question);
})

$('.correct').click(function(event) {
    socket.emit('correct', question)
    $('.question').fadeOut();
    $('.no-messages').fadeIn();
});

$('.incorrect').click(function(event) {
    socket.emit('incorrect', question)
    $('.question').fadeOut();
    $('.no-messages').fadeIn();
});
