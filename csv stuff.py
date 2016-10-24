import csv

with open('jeopardy.csv', newline='') as f:
    game_reader = csv.DictReader(f)

    rows = list(game_reader)

    for row in rows:
        print(row['question'])