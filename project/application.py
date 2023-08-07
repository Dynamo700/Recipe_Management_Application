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
        recipe_serving = form.recipe_serving.data
        recipe_image = form.recipe_image.data
        pic_filename = recipe_name.lower().replace(" ", "_") + "." + secure_filename(form.recipe_image.data.filename).split('.')[-1]
        form.recipe_image.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'name': recipe_name, 'ingreidents': recipe_ingreidents, 'prep': recipe_prep, 'serving': recipe_serving, 'image': recipe_image}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower() + '.csv'))
        return render_template('Recipe_page.html')
    else:
        return render_template('add_recipe.html', form=form)

@app.route('/display_info/')
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
@app.route('/remove_recipe/', methods=['POST', 'GET'])
def remove_recipe():
    form = RecipeForm()
    print("before Submission")
    print(form.is_submitted())
    if form.is_submitted():
        recipe_name = form.recipe_name.data.lower()
        data_dir = app.config['SUBMITTED_DATA']
        image_dir = app.config['SUBMITTED_IMG']
        data_filename = os.path.join(data_dir, f"{recipe_name}.csv")
        image_filename = os.path.join(image_dir, f"{recipe_name}.jpg")

        #Check if both the data and image files exist before removing
        print("After submission")
        if os.path.exists(data_filename):
            print(f"Data file exists: {data_filename}")
            os.remove(data_filename)
            if os.path.exists(image_filename):
                print(f"Image file still exists: {image_filename}")
                os.remove(image_filename)
            return f"Recipe '{recipe_name}' removed!"
        else:
            return f"Sorry, Recipe '{recipe_name}' not found."

    return render_template('remove_recipe.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = RecipeForm()
    if form.is_submitted():
        recipe_name = form.recipe_name.data.lower()
        print(recipe_name)
        df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'], f"{recipe_name.lower()}.csv"))
        print(df.iloc[0])
        print(df.to_dict(orient='records'))
        return render_template('search.html', recipes=df.to_dict(orient='records'), form=form)


    return render_template('search.html', form=form)

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)