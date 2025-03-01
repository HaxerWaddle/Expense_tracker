from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo

class Register_Form(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    register = SubmitField('Register')

class Login_Form(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')

class Add_expense(FlaskForm):  
    name = StringField('ExpenseName', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder":"Description here"})
    submit = SubmitField('Add')

class Edit_expense(FlaskForm):  
    name = StringField('ExpenseName')
    description = TextAreaField('Description', render_kw={"placeholder":"Description here"})
    submit = SubmitField('Save')