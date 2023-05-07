from flask import Flask, render_template, request
import random


app = Flask(__name__)


def word_shuffle(word):
    chars = list(word)
    random.shuffle(chars)
    return ''.join(chars)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random_letters')
def random_letters():
    return render_template('random_letters.html')


@app.route('/random_letters', methods=('GET', 'POST'))
def create():
    def words_shuffle(words, partition):
        words = words.split('\r\n')
        if partition < len(words) and partition!=0:
            words = random.choices(words, k=partition)
        return '\n'.join([word_shuffle(w) for w in words])

    if request.method == 'POST':
        words = request.form['input']
        nums = request.form['variants']
        partition = int(request.form['partition']) if len(request.form['partition']) else 0
        result = ""
        for i in range(int(nums)):
            result = f"{result}{i+1})\n{words_shuffle(words, partition)}\n\n"

        return render_template("random_letters.html", variants=nums, input=words, output=result, partition=partition)
    elif request.method == 'GET':
        return render_template("random_letters.html")

