from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    recipe_name = StringField('recipe_name: ', validators=[DataRequired()])
    recipe_ingreidents = TextAreaField("recipe ingreidents: ", validators=[DataRequired()])
    recipe_prep = TextAreaField('receipe preperation instructions:', validators=[DataRequired()])
    recipe_image = FileField('Receipe picture: ', validators=[FileRequired()])
    ##Make it so it only accepts PNG, or JPG files

##Make second form to delete recipes