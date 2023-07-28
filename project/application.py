from flask import Flask, render_template, request, url_for, redirect
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/variabletest/<name>')
# def print_variable(name):
#     return 'Hello %s' % name

if __name__ == '__main__':
    app.run(debug=True)