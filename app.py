from flask import Flask, render_template, request
import random
import re
import webview


app = Flask(__name__)
window = webview.create_window("Job Generator", app)

def words_shuffle(words):
    def word_shuffle(word):
        chars = list(word)
        random.shuffle(chars)
        return ''.join(chars)
    return '\n'.join([word_shuffle(w) for w in words])


def words_placeholder(words, percentage):
    result = ""

    for w in words:
        rw = list(w)
        for i in random.sample(list(range(len(w))), int(len(w) * percentage / 100)):
            rw[i] = '_'
        result = result + ''.join(rw) + '\n'

    return result


def miss_characters(words, characters):
    result = ""
    for word in words:
        for char in characters:
            word = word.replace(char, '_')
        result = f"{result}{word}\n"

    return result


def match_words(lines):
    col1, col2 = [], []
    for line in lines:
        x = line.split(':')
        col1.append(x[0])
        if len(x) > 1:
            col2.append(x[1])

    random.shuffle(col1)
    random.shuffle(col2)

    def result(col):
        return '\n'.join([f'{i}) {j}' for (i, j) in enumerate(col, start=1)])

    if len(col1) == len(col2):
        return f"{result(col1)}\n{result(col2)}"

    return '\n'.join(col1)


def regexp_omit(sentences):

    def helper(sentence, flag='"', separator='/'):
        matches = [
            m.group() for m in
            re.compile(r'{0}.*?{0}'.format(flag)).finditer(sentence)
        ]

        for match in matches:
            word = random.choice(match[1:-1].split(separator))

            if word.startswith('to ') or word.startswith('not to '):
                sentence = sentence.replace(
                    match, 20 * '_' + ' ({})'.format(word))
            else:
                sentence = sentence.replace(match, '{}'.format(word))

        return sentence

    return '\n'.join(helper(sentence) for sentence in sentences)


def omitted_word(sentences, omit_word):
    def helper(sentence, omit_word):
        for omit in omit_word:
            sentence = re.sub(omit, 15 * '_', sentence, flags=re.IGNORECASE)
        return sentence

    return '\n'.join(helper(sentence, omit_word) for sentence in sentences)


@app.route('/', methods=('GET', 'POST'))
def index():
    def default(field, value):
        return int(field) if len(field) else value

    if request.method == 'POST':

        nums = default(request.form['variants'], 3)
        partition = default(request.form['partition'], 0)
        percentage = default(request.form['percentage'], 10)
        chars = set(request.form['characters'])
        omit_word = [word.strip()
                     for word in request.form['omit_word'].split(',')]
        task = int(request.form.get('task_type'))
        result = ""

        for i in range(nums):
            words = request.form['input'].split('\r\n')
            if partition < len(words) and partition != 0:
                words = random.choices(words, k=partition)

            if task == 1:
                result = f"{result}{i+1})\n{words_shuffle(words)}\n\n"
            elif task == 2:
                result = f"{result}{i+1})\n{words_placeholder(words, percentage)}\n\n"
            elif task == 3:
                result = f"{result}{i+1}) {chars}\n{miss_characters(words, chars)}\n\n"
            elif task == 4:
                result = f"{result}{i+1})\n{match_words(words)}\n\n"
            elif task == 5:
                result = f"{result}{i+1})\n{regexp_omit(words)}\n\n"
            elif task == 6:
                result = f"{result}{i+1})\n{omitted_word(words, omit_word)}\n\n"

        return render_template("index.html", variants=nums, input=request.form['input'], partition=partition, output=result)
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    webview.start()