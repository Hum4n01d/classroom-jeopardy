function update(question) {
    $('.status').remove();
    $('.question-text').text(question.question);
    $('.answer').text(question.answer);
    $('.buttons').show();
}

socket.on('question', function (question) {
    question = JSON.parse(question);
    update(question);
})
