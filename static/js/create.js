$(document).ready(function () {
    var data = localStorage.getItem('json_data');

    if (data) {
        loadJSON(JSON.parse(data));
    }
});

function loadJSON(json_data) {
    var $create_categories = $('.create-board .category');

    $('.title').val(json_data.title);

    var i = 0;

    $create_categories.each(function () {
        var category = json_data.game[i];

        var $questions = $(this).children('.board-question');

        $(this).children('.category-title').val(category.title);

        var question_i = 0;

        $questions.each(function () {
            var question = category.questions[question_i];

            $(this).children('.value').val(question.value);
            $(this).children('.create-question').val(question.question);
            $(this).children('.create-answer').val(question.answer);

            question_i++;
        });

        i++;
    });
}

function generateGameJSON(callback) {
    var $create_category = $('.create-board .category');

    var title = $('.title').val();

    var new_board = {
        title: title,
        game: []
    };

    $create_category.each(function () {
        var category_title = $(this).children('.category-title').val();

        var category_obj = {
            title: category_title,
            questions: []
        };

        $(this).children('.board-question').each(function () {
            var value = $(this).children('.value').val();
            var question_text = $(this).children('.create-question').val();
            var answer = $(this).children('.create-answer').val();

            var question_obj = {
                value: value,
                question: question_text,
                answer: answer
            };

            category_obj.questions.push(question_obj);
        });

        new_board.game.push(category_obj);
    });

    return JSON.stringify(new_board);
}

$('.create-board form').submit(function (e) {
    e.preventDefault();

    var gameJSON = generateGameJSON();

    var $new_form = $('<form>').attr('method', 'POST').addClass('temp_form');

    var $input = $('<input>').attr('name', 'json_data').val(gameJSON);

    $new_form.append($input);

    $('body').append($new_form);
    $new_form[0].submit();

    $('.temp_form').remove();
});

// Save state every 5 seconds
setInterval(function () {
    localStorage.setItem('json_data', generateGameJSON());
}, 5000);

