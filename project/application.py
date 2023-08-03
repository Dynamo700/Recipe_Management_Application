import os.path
from forms import RecipeForm
from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = "bdhejdcbe7773bdcxe34cfb00ojhdb2"
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')

#Home page
@app.route('/')
def index():
    return render_template('index.html')

#Recipe page
@app.route('/Recipe_page')
def Recipe_page():
    return render_template("Recipe_page.html")

#Page for adding recipes
@app.route('/add_recipe', methods = ['POST', 'GET'])
def add_recipe():

    form = RecipeForm()
    ##remove function goes into this if
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        recipe_ingreidents = form.recipe_ingreidents.data
        recipe_prep = form.recipe_prep.data
        recipe_image = form.recipe_image.data
        pic_filename = recipe_name.lower().replace(" ", "_") + "." + secure_filename(form.recipe_image.data.filename).split('.')[-1]
        form.recipe_image.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'name': recipe_name, 'ingreidents': recipe_ingreidents, 'prep': recipe_prep, 'image': recipe_image}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower() + '.csv'))
        return render_template('Recipe_page.html')
    else:
        return render_template('add_recipe.html', form=form)

@app.route('/display_info/<name>')
def render_information(name):
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'), index_col=False)
    print(df.iloc[0]['name'])
    return render_template('view_recipe.html', recipe=df.iloc[0])

# @app.route('/input', methods = ['POST', 'GET'])
# def information():

@app.route('/nametest/<name>')
def print_name(name):

    return 'Recipe name: ' % name

#Page for removing recipes
@app.route('/remove_recipe')
def remove_recipe():
    form = RecipeForm()
    return render_template("remove_recipe.html", form=form)



@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)