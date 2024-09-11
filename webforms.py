from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField
from wtforms.validators import  Length, ValidationError, DataRequired, EqualTo, Email
from wtforms.widgets import TextArea
from app import db
db = class Users()

# Registration Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
     
    password_hash = PasswordField('Password', validators=[DataRequired(), 
        EqualTo('password_hash2', message='Passwords Must Match !'), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
    
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
    
    student = StringField('Student Number', validators=[DataRequired(), Length(
        min=4, max=8)], render_kw={"Placeholder": "eg. 12345678"})
    
    title = StringField('Title', validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={"Placeholder": "eg. Mr/Mrs"})

    surname= StringField('Surname',validators=[DataRequired(), Length(
      min=4, max=50)], render_kw={"Placeholder": ""})

    initials= StringField('Initial',validators=[DataRequired(), Length(
       min=1, max=8)], render_kw={"Placeholder": ""})

    degree= StringField('Degree',validators=[DataRequired(), Length(
       min=4, max=30)], render_kw={"Placeholder": "eg. B.Com Risk Managemet"})

    name= StringField('Name',validators=[DataRequired(), Length(
       min=4, max=20)], render_kw={"Placeholder": ""})

    campus= StringField('Camups',validators=[DataRequired(), Length(
       min=1, max=50)], render_kw={"Placeholder": "eg. Vaal Campus"})
    
    #email= EmailField('Email',validators=[DataRequired(), Length(
       #min=1, max=100)], render_kw={"Placeholder": "eg. Email@gmail.com"})
    
    submit = SubmitField("Submit")

    def validate_username(self, username):
        # Later you can make the student number a validator
        existing_user_username = Users.query.filter_by(
                username=username.data ).first()
        
        if existing_user_username:
            raise ValidationError(
                "That Username already exits!!! Please choose a different one.")
        # later on validate using student number
   
    def validate_username(self, student):
        existing_user_student = Users.query.filter_by(
            student=student.data).first()
        
        if existing_user_student:
            raise ValidationError('student number already exits.')
 

# Login Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
    
    # Later you can make the student number a validator
    """
    student_number = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": "Student Number"})
    """
    
    password_hash = PasswordField('Password',validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
    
    submit = SubmitField("Login")

class NotesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
    
    selected_module_id = IntegerField('Module', validators=[DataRequired()], 
                render_kw={"Placeholder": "Module"})
    
    content = StringField('Notes',validators=[DataRequired()], widget=TextArea(), render_kw={"Placeholder": "Add Notes"})
    
    slug = StringField('Slug',validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
        
    submit = SubmitField("Submit") 