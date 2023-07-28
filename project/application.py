from flask import Flask, render_template, request, url_for, redirect
import pandas as pd

app = Flask(__name__)

#Home page
@app.route('/')
def index():
    return render_template('index.html')

#Recipe page
@app.route('/Recipe_page')
def Recipe_page():
    return render_template("Recipe_page.html")

#Page for adding recipes
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")

#Page for removing recipes
@app.route('/remove_recipe')
def remove_recipe():
    return render_template("remove_recipe.html")

if __name__ == '__main__':
    app.run(debug=True)