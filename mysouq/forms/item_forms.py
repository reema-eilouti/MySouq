from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField, FloatField, SelectField

class AddItemForm(FlaskForm):
    title = StringField("Title: ", [validators.InputRequired()])
    description = TextAreaField("Description: ", [validators.InputRequired()])
    price = FloatField("Price: ", [validators.InputRequired()])
    category = SelectField(u'Category')
    submit = SubmitField("Add Item")


class EditItemForm(FlaskForm):
    title = StringField("Title: ", [validators.InputRequired()])
    description = TextAreaField("Description: ", [validators.InputRequired()])
    price = FloatField("Price: ", [validators.InputRequired()])
    category = SelectField(u'Category')
    submit = SubmitField("Edit Item")   


class AddCategoryForm(FlaskForm):
    value = StringField("Category Number: ")
    label = StringField("Category Name: ")
    submit = SubmitField("Add Category")