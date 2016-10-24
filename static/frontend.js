function open_modal($el) {
    var question = $el.children('.question').text();
    var value = $el.children('.value').text();
    var answer = $el.children('.answer').text();

    $('.modal').fadeIn();

    $('.modal .value').text('For ' + value + ' points:');
    $('.question').text(question);
    $('.answer').text(answer);
}

$('.clue').click(function() {
    open_modal($(this));
});

$('.blanket, .close').click(function(e) {
    $('.modal').fadeOut();
});

$('.modal form').submit(function(e) {
    e.preventDefault();

    var $el = $(this).parent();

    var correct_answer = $('.modal p.answer').text().toLowerCase();
    var answer = $('.modal input.answer').val().toLowerCase();
//    var correct = answer.toLowerCase() == hex_md5(correct_answer.toLowerCase());

    console.log(correct_answer);
    console.log(answer);

    var correct = answer == correct_answer;

    if (correct) {
        alert('correct');
    } else {
        alert('wrong. the answer is: ' + correct_answer);
    }
});