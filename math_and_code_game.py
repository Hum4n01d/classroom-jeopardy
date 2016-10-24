# -*- coding: utf-8 -*-

data = '''Console.log(); - How do you print to the console?
<p></p> - How do you make a paragraph tag?
import module - How do you import a module?
42 - What is 7*6?
#el {color: red;} - How do you change the text color of an element?
/* comment */ - How do you write a multiline comment in Javascript?
<!DOCTYPE html> - How do you define an HTML 5 Doctype
"Hello {}".format(name) - How do you do string interpolation?
13 - What is the square root of 169?
#el {marign: 0 10px;} - How do you add padding only on the sides of an element?
parseInt(); - How do you convert another type to an integer?
<ul></ul> - How do you make an unordered list?
__init__() - What function runs when you create an instance of a class?
697 - What is 41*51/3?
#el {display: flex;} - How do you define a flex box container?
require('module') - How do you import a module?
<label for="name"></label> - How do you make a label that, when clicked, focuses on the input with id name?
An iterable range instance with numbers in the range - What does the range function produce?
4x^2-64 - What is (4(x-2))^2 in expanded form?
#el {background-image: linear-gradient(green, red);} - How do you set an element’s background to a gradient from green to red?
new Prototype() - How do you create an instance of a prototype?
<div contenteditable="true"></div> - How do you make an element editable?
lambda x: x + 1 - What is the syntax of a lambda that adds one to a given number?
46 - What is the square root of 21 rounded to the nearest tenth times 10?
#el {-webkit-backdrop-filter: blur(3px)} - How do you add a macOS Yosemite style background blur to an element?'''

data = data.split('\n')
counter = 1
counter2 = 1
new = []

for i in data:
    parsed = i.split(' - ')

    new_obj = {}
    new_obj['question'] = parsed[0]
    new_obj['answer'] = parsed[1]

    if counter < 5:
        value = '200'
    elif counter < 10:
        value = '400'
    elif counter < 15:
        value = '600'
    elif counter < 20:
        value = '800'
    elif counter < 25:
        value = '1000'

    if counter2 == 1:
        category = 'Javascript'
    elif counter2 == 2:
        category = 'HTML'
    elif counter2 == 3:
        category = 'Python'
    elif counter2 == 4:
        category = 'Math'
    else:
        category = 'CSS'
        counter2 = 0

    new_obj['value'] = value
    new_obj['category'] = category

    new.append(new_obj)

    counter += 1
    counter2 += 1

open('mock.py', 'w').write('data = '+str(new))
