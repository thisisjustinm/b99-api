import glob
import os
from random import randint
from flask import Flask, render_template, request
import json


app = Flask(__name__, template_folder='./templates')
files = glob.glob("src/1/*.txt")
char_list = [i[6:-4] for i in files]


def read_txt(season, name):
    try:
        lines = []
        file_name = f"src/{season}/{name}.txt"
        file = open(file_name, "r")
        for line in file:
            lines.append(line)
        file.close()
        return lines
    except FileNotFoundError:
        return False


@app.route('/')
def hello():
    return render_template('index.html', char_list=char_list)


@app.route('/name/<name>')
def get_name(name):
    if request.args.get('season'):
        quote_list = read_txt(request.args.get('season'), name.lower())
        if not quote_list:
            return 'Sadly, this season is not released yet.'
        else:
            return quote_list[randint(0, len(quote_list) - 1)]
    else:
        quote_list = read_txt(randint(1, 7), name.lower())
        return quote_list[randint(0, len(quote_list) - 1)]


@app.route('/season/<season>')
def get_season(season):
    if request.args.get('name'):
        quote_list = read_txt(season, request.args.get('name').lower())
        if not quote_list:
            return 'Sadly, this season is not released yet.'
        else:
            return quote_list[randint(0, len(quote_list) - 1)]
    else:
        quote_list = read_txt(season, char_list[randint(0, len(char_list) - 1)])
        return quote_list[randint(0, len(quote_list) - 1)]


@app.route('/title')
def get_title():
    quote_list = read_txt('toyst', 'toyst')
    if request.args.get('name'):
        return quote_list[randint(0, len(quote_list) - 1)]+f"Title of {request.args.get('name').title()}'s sex tape."
    else:
        return quote_list[randint(0, len(quote_list) - 1)]


@app.route('/insults/<name>')
def get_insults(name):
    quote_list = read_txt('insults', 'holt')
    single_q = quote_list[randint(0, len(quote_list) - 1)]
    if name:
        return single_q.replace('$$', name.title())
    else:
        return 'The endpoint requires a name. Try with /insults/boyle .'


@app.route('/alias')
def get_alias():
    with open('src/alias/alias.json') as f:
        data = json.load(f)
    f.close()
    if request.args.get('season'):
        return json.dumps(data[request.args.get('season')])
    else:
        return json.loads(json.dumps(data))


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(port=port, debug=True)
