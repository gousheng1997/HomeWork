# coding=utf-8
import os

from flask import Flask

from handlers.hello_handler import HelloHandler

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', "docx"])

app.add_url_rule('/hello', view_func=HelloHandler.as_view("index"))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
