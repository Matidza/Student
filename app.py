from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import UserMixin, login_user,LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField
from wtforms.validators import  Length, ValidationError, DataRequired, EqualTo
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import current_user
from sqlalchemy import ForeignKeyConstraint
from wtforms.widgets import TextArea

import os


""""
APP CONFIGURATIONS

"""
app = Flask(__name__)

# Postgre SQL Connection

# SQLite Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# MySQL CONNECTION
# Creating App Instance
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Zwivhuya:1969Zwi%21%40%23@Zwivhuya.mysql.pythonanywhere-services.com:3306/Zwivhuya$Users'




app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1969@localhost/users"

app.config['SQLALCHEMY_TRACK_MIDIFICATIONS'] = False

app.config['SECRET_KEY'] = "Thesecrectkeyisequalto1969Zwi!@#"

# Connects the DB to the app
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
#migrate = Migrate(app, db)



""""
LOGIN MANAGER RELATED

"""
login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



""""
GLOBAL TABLE RELATED

"""
# DB Table
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    student = db.Column(db.String(8), nullable=True, unique=True)
    title  = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    initials = db.Column(db.String(8), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    #email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    UsersNotes= db.relationship('Notes', backref='UsersNotes', cascade='all, delete-orphan')
    Users= db.relationship('UserModules', backref='Users', cascade='all, delete-orphan')#, passive_deletes=True
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash , password)
    
    def __repr__(self):
        return 'Name %r' % self.id  

# Module Table
class Vaal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Module = db.Column(db.Text)
    Date = db.Column(db.Text)
    Session  = db.Column(db.Text)
    Duration = db.Column(db.Text)
    Venue = db.Column(db.Text)
    Students = db.Column(db.Text)
    Vaal = db.relationship('UserModules', backref='Vaal')
    VaalNotes= db.relationship('Notes', backref='VaalNotes')




 


    
    
   

""""
HOME RELATED

"""
# ROUTING WEB PAGES
# Route Homepgae
@app.route("/") # this routes to home page
def home():
    name = "Student Card"
    return render_template("home.html", name=name)








""""
HOME RELATED

"""
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
 



""""
LOGIN RELATED

"""
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

# User Login
@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                flash("Login Succesfully")  
                return redirect(url_for('dashboard'))
            else:
                flash("Password Invalid! Try Again!")
                return redirect(url_for('login'))
        else:
            flash("Username Invalid! Try Again!")
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)

# User Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out! ')
    return redirect(url_for('login'))











""""
ERROR HANDLING RELATED

"""
# Invalid error
@app.errorhandler(404)
def page_nt_found(e):
    return render_template('404.html'), 404


# Internal Server error
@app.errorhandler(500)
def page_nt_found(e):
    return render_template('500.html'), 500












""""
FORGOT PASSWORD RELATED

"""
# User Password Recovery
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = RegisterForm()
    return render_template('forgot.html', form=form)









""""
REGISTER RELATED

"""
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

# Register New User
@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password_hash.data)
            new_user = Users(username=form.username.data, 
                            password_hash=hashed_password, student=form.student.data,
                            title=form.title.data , surname=form.surname.data,
                            initials=form.initials.data, degree=form.degree.data,
                            name=form.name.data, campus=form.campus.data)
            # Register user to DB
            db.session.add(new_user)
            db.session.commit()
            # return a message 
            flash('Form was submited successfully!')
            return redirect(url_for('login'))
        except Exception as e:
            flash("Username/student number already exists! Please try again!")
            return redirect(url_for('register'))
    else:
        
        return render_template('register.html', form=form)













""""
DASHBOARD RELATED

"""
# User DashBoard to display uer modules
@app.route('/dashboard', methods=["GET","POST"])
@login_required
def dashboard():
    
    modules = UserModules.query.filter_by(user_id=UserModules.user_id).all()
    return render_template('dashboard.html', modules=modules)

# Delete User Account
@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):

    current_user = Users.query.get_or_404(id)    
    try:
        db.session.delete(current_user)
        db.session.commit()
        flash('Account Deleted Successfully !')
        return redirect('/login')
    except:
        flash('Accont Deletion Not Successful !')
        return render_template('dashboard.html')
    

# Update User Account
@app.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = RegisterForm()
    current_user = Users.query.get_or_404(id)
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.title = request.form['title']
        current_user.surname = request.form['surname']
        current_user.name = request.form['name']
        current_user.initials = request.form['initials']
        current_user.degree = request.form['degree']
        current_user.campus = request.form['campus']
        #current_user.student = request.form['student']
        #current_user.password_hash = request.form['password_hash']
        try:
            # Validate on submit Username and Student number on update before updaing
            db.session.commit()
            flash('Account Updated Successfully !')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Updating Account was Not Successful !')
            return redirect('/dashboard')
    else:

        return render_template('update.html', form=form, current_user=current_user)











""""
UserModules RELATED
"""
# Create Model for UserModules
class UserModules(db.Model):
    __tablename__ = 'UserModules'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('vaal.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #__table_args__ = (ForeignKeyConstraint(['user_id'], ['(link unavailable)'], ondelete='CASCADE'),)
    
# Add Modules To User DashBoard
@app.route('/modules', methods=['GET', 'POST'])
@login_required
def modules():
    if request.method == 'POST':
        module_id = request.form.get('module_id')
        user_id = request.form.get('user_id')
        new_user_module = UserModules(module_id=module_id, user_id=user_id)
        db.session.add(new_user_module)
        db.session.commit()
        flash('Module added successfully!')
        return redirect(url_for('dashboard'))  # or wherever you want to redirect
    all_modules = Vaal.query.order_by(Vaal.Module)
    return render_template('modules.html', all_modules=all_modules)
    #all_modules = Vaal.query.order_by(Vaal.Module) # I use Vaal.Module and not Vaal.id since Vaal.Module will be Alphabetic order
    
    #if request.method == 'POST':
    #    selected_modules = request.form.getlist('Vaal.id')

      #  for module_id in selected_modules:
      #      # Check if the module is already added to the user's dashboard
      #      existing_module = UserModules.query.filter_by(user_id=current_user.id, module_id=module_id).first()
      #      if not existing_module:
       #         user_module = UserModules(user_id=current_user.id, module_id=module_id)
      #          db.session.add(user_module)

     #   db.session.commit()
    #    flash('Modules added to your dashboard!', 'success')
    #    return redirect(url_for('dashboard'))

   # return render_template('modules.html', all_modules=all_modules)
class SearchForm(FlaskForm):
    search = StringField('Searched', validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
    submit = SubmitField("Search")

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

# Search Modules
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    form = SearchForm()
    modules = Vaal.query
    if form.validate_on_submit():
        # Get data

        module.searched = form.searched.data
        modules = Vaal.query.filter(Vaal.Module.like('%' + modules.searched + '%'))
        modules = Vaal.order_by(Vaal.Module).all()
        return render_template('modules.html', form=form, searched=module.searched, modules=modules)

""""
Module Display are on 
Dashboard Route

"""
# Individual Module Page
@app.route('/module/<id>')
@login_required
def module(id):
    notes = Notes.query.order_by(Notes.date_created)
    module = UserModules.query.get_or_404(id)
    return render_template('module.html', module=module, notes=notes)


# Delete Individual Module
@app.route('/deletemod/<id>', methods=['GET', 'POST'])
@login_required
def deletemod(id):
    
    # Delete variable
    delete = UserModules.query.get_or_404(id)
    id = current_user.id
    if id == delete.Users.id:

        try:
            db.session.delete(delete)
            db.session.commit()
            flash('Module Deleted!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Module Not Deleted !')
            return f"ERROR:{e}"
    else:
        flash('Module Not Deleted!')
        return redirect(url_for('dashboard'))












""""
NOTES RELATED
"""
# Notes Model
# Later You should Link this table To each particular Module
class Notes(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    selected_module_id = db.Column(db.Integer, db.ForeignKey('vaal.id'),  nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    


# Notes Form
class NotesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
    
    selected_module_id = IntegerField('Module', validators=[DataRequired()], 
                render_kw={"Placeholder": "Module"})
    
    content = StringField('Notes',validators=[DataRequired()], widget=TextArea(), render_kw={"Placeholder": "Add Notes"})
    
    slug = StringField('Slug',validators=[DataRequired(), Length(
        min=4, max=20)], render_kw={"Placeholder": ""})
        
    submit = SubmitField("Submit")    

# Add Notes to Modele
@app.route('/notesform', methods=['GET', 'POST'])
@login_required
def notesform():

    if request.method == 'POST':
        title = request.form.get('title')
        user_id = request.form.get('user_id')
        selected_module_id = request.form.get('selected_module_id')
        content = request.form.get('content')
        
        notes = Notes(title=title, selected_module_id=selected_module_id, 
                user_id=user_id, content=content)#, slug=slug
        db.session.add(notes)
        db.session.commit()
        flash('Notes Added !')
        return redirect(url_for('allnotes'))  # or wherever you want to redirect
    
    notes = UserModules.query.order_by(UserModules.id)
    return render_template('notesform.html', notes=notes)



@app.route('/allnotes', methods=['GET', 'POST'])
@login_required
def allnotes():

    user_id = current_user.id
    notes = Notes.query.filter_by(user_id=user_id).all()
    
    # Group notes by selected_module_id
    grouped_notes = {}
    for note in notes:
        module_id = note.selected_module_id  # Module ID from the note
        if module_id not in grouped_notes:
            grouped_notes[module_id] = []
        grouped_notes[module_id].append(note)
    
    return render_template('allnotes.html',  grouped_notes=grouped_notes)

# individual Note page
@app.route('/note/<id>')
@login_required
def note(id):
    
    note = Notes.query.get_or_404(id)
    return render_template('note.html', note=note)

# Delete Notes to Modele
@app.route('/delete_notes/<id>', methods=['GET', 'POST'])
@login_required
def delete_notes(id):
    delete = Notes.query.get_or_404(id)
    id = current_user.id

    if id == delete.UsersNotes.id:
        
        try:
            db.session.delete(delete)
            db.session.commit()
            flash('Notes Deleted!')
            return redirect(url_for('allnotes'))
        except Exception as e:
            flash('Module Not Deleted !')
            return f"ERROR:{e}"
    else:
        flash('Notes Not Deleted!')
        return redirect(url_for('allnotes'))
    
    
# Update  Notes to Modele
@app.route('/update_notes/<id>', methods=['GET', 'POST'])
@login_required
def update_notes(id):
    update_notes = Notes.query.get_or_404(id)
    if request.method == 'POST':
        update_notes.title = request.form.get('title')       
        update_notes.user_id = request.form.get('user_id')     
        update_notes.selected_modlue_id = request.form.get('selected_module_id')
        update_notes.content = request.form.get('content')
        try:
            db.session.commit()
            flash('Notes Updated !')
            return redirect('/allnotes')
        except:
            flash('Notes Not Updated !')
            return render_template('update_notes.html')
    else:
        return render_template('update_notes.html', update_notes=update_notes)

"""
Developer's Page
"""
@app.route('/dev', methods=['GET', 'POST'])
def dev():
    return render_template('dev.html')

""""
FOOTER PAGE RELATED
"""

if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    app.run(debug=False)