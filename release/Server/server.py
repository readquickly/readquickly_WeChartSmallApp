from flask import Flask, request, abort, redirect
from flask import render_template

import json
import time

from . import content
from .notice import superNotice, admindo
from .spider import driver as spiderDriver

'''
处理来自前端的请求响应

使用：在服务器上：
$ export FLASK_APP=server.py
$ flask run --host=0.0.0.0
'''

app = Flask(__name__)

# 根目录，测试链接通畅
@app.route('/')
def index():
    return 'Hello, Read Quickly!'

# 前端请求数据
@app.route('/readquickly/api/getnews', methods=['GET'])
def requestNews():
    error = None
    city = request.args.get('city', '')
    if city:
        print(city)
        news = content.getContent(city)
        if news:
            return json.dumps(news)
        else:
            error = {'error': 'False to get content.'}
    else:
        error = {'error': 'Bad arg (city) was given.'}

    return json.dumps(error)

# 手动添加数据
@app.route('/readquickly/admin/notice', methods=['GET', 'POST'])
def notice():
    response = None
    if request.method == 'POST':
        if admindo.exist(request.form['key']):
            useful = {
                'title': request.form['title'],
                'source': request.form['source'] or 'Admin',
                'href': request.form['href'],
                'time': time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
                'text': request.form['text'],
                'pic': request.form['pic'],
                'expires': request.form['expires'] or "0"
            }

            if useful['title'] == useful['text'] == '':
                response = '<h1>Invalid Data!</h1><p>Unexpected Empty Notice.</p>'
            else:
                superNotice.saveData([useful])
                response = '<h1>Succeed!</h1>'
        else:
            response = '<h1>Invalid Data!</h1><p>Unexpected Key.</p>'

        return response
        
    return render_template('newNotice.html')

# 刷新爬虫数据
@app.route('/readquickly/refresh', methods=['GET', 'POST'])
def refresh():
    spiderDriver.run()
    return "<h1>Succeed!</h1>"