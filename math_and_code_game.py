import json

data = [
    [
        "Javascript",
        "HTML",
        "Python",
        "Math",
        "CSS"
    ],
    {
    	'question': 'How do you print to the console?',
    	'category': 'Javascript',
    	'answer': 'Console.log();',
    	'value': '200'
    }, {
    	'question': 'How do you make a paragraph tag?',
    	'category': 'HTML',
    	'answer': '<p></p>',
    	'value': '200'
    }, {
    	'question': 'How do you import a module?',
    	'category': 'Python',
    	'answer': 'import module',
    	'value': '200'
    }, {
    	'question': 'What is 7*6?',
    	'category': 'Math',
    	'answer': '42',
    	'value': '200'
    }, {
    	'question': 'How do you change the text color of an element?',
    	'category': 'CSS',
    	'answer': '#el {color: red;}',
    	'value': '400'
    }, {
    	'question': 'How do you write a multiline comment in Javascript?',
    	'category': 'Javascript',
    	'answer': '/* comment */',
    	'value': '400'
    }, {
    	'question': 'How do you define an HTML 5 Doctype',
    	'category': 'HTML',
    	'answer': '<!DOCTYPE html>',
    	'value': '400'
    }, {
    	'question': 'How do you do string interpolation?',
    	'category': 'Python',
    	'answer': '"Hello {}".format(name)',
    	'value': '400'
    }, {
    	'question': 'What is the square root of 169?',
    	'category': 'Math',
    	'answer': '13',
    	'value': '400'
    }, {
    	'question': 'How do you add padding only on the sides of an element?',
    	'category': 'CSS',
    	'answer': '#el {marign: 0 10px;}',
    	'value': '600'
    }, {
    	'question': 'How do you convert another type to an integer?',
    	'category': 'Javascript',
    	'answer': 'parseInt();',
    	'value': '600'
    }, {
    	'question': 'How do you make an unordered list?',
    	'category': 'HTML',
    	'answer': '<ul></ul>',
    	'value': '600'
    }, {
    	'question': 'What function runs when you create an instance of a class?',
    	'category': 'Python',
    	'answer': '__init__()',
    	'value': '600'
    }, {
    	'question': 'What is 41*51/3?',
    	'category': 'Math',
    	'answer': '697',
    	'value': '600'
    }, {
    	'question': 'How do you define a flex box container?',
    	'category': 'CSS',
    	'answer': '#el {display: flex;}',
    	'value': '800'
    }, {
    	'question': 'How do you import a module?',
    	'category': 'Javascript',
    	'answer': "require('module')",
    	'value': '800'
    }, {
    	'question': 'How do you make a label that, when clicked, focuses on the input with id name?',
    	'category': 'HTML',
    	'answer': '<label for="name"></label>',
    	'value': '800'
    }, {
    	'question': 'What does the range function produce?',
    	'category': 'Python',
    	'answer': 'An iterable range instance with numbers in the range',
    	'value': '800'
    }, {
    	'question': 'What is (4(x-2))^2 in expanded form?',
    	'category': 'Math',
    	'answer': '4x^2-64',
    	'value': '800'
    }, {
    	'question': 'How do you set an element\xe2\x80\x99s background to a gradient from green to red?',
    	'category': 'CSS',
    	'answer': '#el {background-image: linear-gradient(green, red);}',
    	'value': '1000'
    }, {
    	'question': 'How do you create an instance of a prototype?',
    	'category': 'Javascript',
    	'answer': 'new Prototype()',
    	'value': '1000'
    }, {
    	'question': 'How do you make an element editable?',
    	'category': 'HTML',
    	'answer': '<div contenteditable="true"></div>',
    	'value': '1000'
    }, {
    	'question': 'What is the syntax of a lambda that adds one to a given number?',
    	'category': 'Python',
    	'answer': 'lambda x: x + 1',
    	'value': '1000'
    }, {
    	'question': 'What is the square root of 21 rounded to the nearest tenth times 10?',
    	'category': 'Math',
    	'answer': '46',
    	'value': '1000'
    }, {
    	'question': 'How do you add a macOS Yosemite style background blur to an element?',
    	'category': 'CSS',
    	'answer': '#el {-webkit-backdrop-filter: blur(3px)}',
    	'value': '1000'
    }
]

javascript = []
python = []
math = []
css = []
html = []

new = []

for question in data[1::]:
    category = question['category'].lower()
    if category == 'javascript':
        javascript.append(question)
    elif category == 'css':
        css.append(question)
    elif category == 'html':
        html.append(question)
    elif category == 'python':
        python.append(question)
    else:
        math.append(question)

name = 'html'
_list = html

new_obj = {
    "name": name,
    "questions": [

    ]
}

for question in _list:
    question2 = question
    del question2['category']
    new_obj['questions'].append(question2)

json.dump(new_obj, open('t.json', 'w'))
# d = [
#     {
#         "category_name": "math",
#         "questions": [
#             {
#                 "title": "test question"
#             },
#             {
#                 "title": "test question 2"
#             }
#         ]
#     }
# ]
