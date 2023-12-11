from flask import Flask, render_template, request
import csv
import random

app = Flask(__name__)

def load_champion_data():
    champion_data = []
    with open('Champion.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Remove BOM from key if present
            row = {key.lstrip('\ufeff'): value for key, value in row.items()}
            champion_data.append(row)
    return champion_data

def get_champions_by_lane(champion_data, target_lane):
    return [champion for champion in champion_data if target_lane in champion['Lane'].split(',')]

@app.route('/', methods=['GET', 'POST'])
def random_champion():
    champion_data = load_champion_data()
    
    if request.method == 'POST':
        target_lane = request.form.get('lane')
        if target_lane:
            champions_in_lane = get_champions_by_lane(champion_data, target_lane)
            if not champions_in_lane:
                return render_template('random_champion.html', error_message="No champions found for the specified lane.")
            random_champion = random.choice(champions_in_lane)
        else:
            random_champion = random.choice(champion_data)
    else:
        random_champion = random.choice(champion_data)

    return render_template('random_champion.html', random_champion=random_champion)

if __name__ == '__main__':
    app.run(debug=True)
