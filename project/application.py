import os.path
from csv import writer
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
@app.route('/recipe/Recipe_page/')
def Recipe_page():
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'], "recipes.csv"), index_col=False)
    recipes = df.to_dict(orient='records')
    print(recipes)
    print(df.iloc[0]['name'])
    print("Hello")
    return render_template('Recipe_page.html', recipes = recipes)

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
        recipe = {'name': recipe_name, 'ingreidents': recipe_ingreidents, 'prep': recipe_prep, 'serving': recipe_serving, 'image': recipe_image}
        with open(os.path.join(app.config['SUBMITTED_DATA'] + 'recipes.csv'), 'a') as f_object:

            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(recipe.values())

            # Close the file object
            f_object.close()

        return render_template('index.html')
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
        data_filename = os.path.join(data_dir, "recipes.csv")
        image_filename = os.path.join(image_dir, f"{recipe_name}.jpg")

        if os.path.exists(data_filename):
            df = pd.read_csv(os.path.join(data_filename))
            recipes = df.to_dict(orient= 'records')
            i = None
            for index, recipe in enumerate(recipes):
                if recipe['name'] == recipe_name:
                    i = index
                    break

        if i is not None:
            df_updated = df.drop(i)
            df_updated.to_csv(data_filename, index= False)
            if os.path.exists(image_filename):
                print(f"Image file still exists: {image_filename}")
                os.remove(image_filename)
            return f"Recipe '{recipe_name}' removed!"
        else:
            return f"Sorry, recipe does not exist"

    return render_template('remove_recipe.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = RecipeForm()
    print("Before submission")
    print(form.is_submitted())
    if form.is_submitted():
        recipe_name = form.recipe_name.data.lower()
        data_dir = app.config['SUBMITTED_DATA']
        image_dir = app.config['SUBMITTED_IMG']
        data_filename = os.path.join(data_dir, "recipes.csv")
        image_filename = os.path.join(image_dir, f"{recipe_name}.jpg")

        print("After submission")
        if os.path.exists(data_filename):
            # recipe_name = form.recipe_name.data.lower()
            print(f"Recipe exists: {data_filename}")
            print(recipe_name)
            df = pd.read_csv(os.path.join(data_filename))
            recipes = df.to_dict(orient= 'records')
            # recipesfound = []
            RecipesList = []
            for recipe in recipes:
                if recipe_name.lower() in recipe['name'].lower():
                    print("found")
                    RecipesList.append(recipe)
                    # recipesfound.insert(recipe)
            print(df.iloc[0])
            print(df.to_dict(orient='records'))
            if os.path.exists(image_filename):
                print("Image file found!")
            return render_template('search.html', recipes=RecipesList, form=form)
        else:
            return f"Sorry, recipe does not exist"



    return render_template('search.html', form=form)

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)