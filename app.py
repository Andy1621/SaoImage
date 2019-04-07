#! env python3
# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request
from style_transfer import setup, StyleTransfer
import json

app = Flask(__name__)

style_transfer = StyleTransfer()

prog = 0


@app.route('/')
@app.route('/ist')
def ist():
    return render_template('ist.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/v1/mix', methods=['POST'])
def mix():
    setup()
    content_img = request.form['content']
    style_img = request.form['style']
    train = request.form['train']
    # 指定像素尺寸
    img_width = 400
    img_height = 300
    # style transfer
    global style_transfer
    style_transfer = StyleTransfer(content_img, style_img, img_width, img_height)
    style_transfer.build()
    style_transfer.train(int(train))
    style_transfer.gif()
    print(train)
    res = dict()
    res['gif'] = style_transfer.res
    res['mix_img'] = style_transfer.mix_img
    return json.dumps(res)


@app.route('/api/v1/progress', methods=['GET'])
def progress():
    global style_transfer
    res = dict()
    res['prog'] = str(style_transfer.prog)
    res['mix_img'] = style_transfer.mix_img
    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
