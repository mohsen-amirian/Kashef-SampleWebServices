import random

from flask import Flask, request, jsonify, send_file
import tempfile
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
    r"/multiple_json/*": {"origins": "*"},
    r"/sum_json/*": {"origins": "*"},
    r"/div_json/*": {"origins": "*"},
    r"/sub_json/*": {"origins": "*"},
    r"/sum/*": {"origins": "*"},
    r"/*/*": {"origins": "*"}
})

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/sampler/', methods=['POST'])
def sampler():
    if 'file' not in request.files:
        return "پارامتر «فایل» در درخواست موجود نیست.", 400
    f = request.files['file']
    if f.filename == '':
        return "فایل انتخاب نشده است.", 400
    filename = tempfile.mktemp()
    f.save(filename)
    num = float(request.form['perc'])
    with open(filename) as fi:
        num_list = [int(x) for x in fi.readlines()]
    rand_smpl = [num_list[i] for i in random.sample(range(len(num_list)), int(num * len(num_list) / 100))]
    return json.dumps({'num_list': str(rand_smpl)})


@app.route('/sum/', methods=['POST'])
def add():
    try:
        print(len(request.form))
        return json.dumps({'add_result': float(request.form['number1']) + float(request.form['number2'])})
    except:
        return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/sum_json/', methods=['POST'])
def add_json():
    try:
        data = json.loads(request.data)
        return json.dumps({"add_result": data['number1'] + data['number2']})
    except:
        return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/sub/', methods=['POST'])
def sub():
    return json.dumps({'sub_result': float(request.form['number1']) - float(request.form['number2'])})

    # try:
    #     return json.dumps({'sub_result': float(request.form['number1']) - float(request.form['number2'])})
    # except:
    #     return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/sub_json/', methods=['POST'])
def sub_json():
    try:
        data = json.loads(request.data)
        return json.dumps({"sub_result": data['number1'] - data['number2']})
    except:
        return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/multiple/', methods=['POST'])
def multiple():
    try:
        return json.dumps({'result': float(request.form['number1']) * float(request.form['number2'])})
    except:
        return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/multiple_json/', methods=['POST'])
def multiple_json():
    try:
        data = json.loads(request.data)
        return json.dumps({"mul_result": data['number1'] * data['number2']})
    except:
        return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/div/', methods=['POST'])
def div():
    try:
        return json.dumps({'result': float(request.form['number1']) / float(request.form['number2'])})
    except:
        return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/div_json/', methods=['POST'])
def div_json():
    try:
        data = json.loads(request.data)
        return json.dumps({"div_result": data['number1'] / data['number2']})
    except:
        return "درخواست ارسال شده معتبر نیست.", 400


@app.route('/read_text_file/', methods=['POST'])
def read_text_file():
    if 'file1' not in request.files:
        return "پارامتر «file1» در درخواست موجود نیست.", 400
    f = request.files['file1']
    if f.filename == '':
        return "فایل انتخاب نشده است.", 400
    f.save('temp.txt')

    return send_file('temp.txt')


@app.route('/read_text_file_json/', methods=['POST'])
def read_text_file_json():
    if 'text-file' not in request.files:
        return "پارامتر «text-file» در درخواست موجود نیست.", 400
    f = request.files['text-file']
    if f.filename == '':
        return "فایل انتخاب نشده است.", 400
    f.save('temp.txt')

    data = open('temp.txt', 'r')
    x = data.read()
    return json.dumps({"text": x})



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005)
