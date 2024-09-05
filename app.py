from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import UserMixin, login_user,LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, ValidationError
from wtforms.validators import  Length, ValidationError, DataRequired, EqualTo, Length
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime
from flask_login import current_user

app = Flask(__name__)
# Postgre SQL Connection


# SQLite Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1969@localhost/users'
app.config['SQLALCHEMY_TRACK_MIDIFICATIONS'] = True 
# Connects the DB to the app
app.config['SECRET_KEY'] = 'htnethnet'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



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



# ROUTING WEB PAGES
# Route Homepgae
@app.route("/") # this routes to home page
def home():
    name = "Student Card"
    return render_template("home.html", name=name)

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


# User Password Recovery
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html')

# Invalid error
@app.errorhandler(404)
def page_nt_found(e):
    return render_template('404.html'), 404


# Internal Server error
@app.errorhandler(500)
def page_nt_found(e):
    return render_template('500.html'), 500


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


# User DashBoard
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
        return redirect('login')
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
    
# Create Model for Notes
class UserModules(db.Model):
    __tablename__ = 'UserModules'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('vaal.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    Vaal = db.relationship('Vaal', backref='Vaal')
    users= db.relationship('Users', backref='Users')

    
    

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


# Individual Module
@app.route('/module', methods=['GET', 'POST'])
@login_required
def module():
    
    return render_template('module.html')
# Delete Individual Module
@login_required
@app.route('/deletemod/<id>', methods=['GET', 'POST'])
def deletemod(id):
    if request.method == "POST":

        delete = UserModules.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            flash('Module Deleted!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Module Not Deleted !')
            return f"ERROR:{e}"
   


# Notes Model
# Later You should Link this table To each particular Module
class Notes:
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    module = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Add Notes to Modele
@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    all_notes = Notes.query.order_by(Notes.id)
    return render_template('modules.html', all_notes=all_notes)


# Delete Notes to Modele
@app.route('/delete_notes/<id>', methods=['GET', 'POST'])
@login_required
def delete_notes():
    all_notes = Notes.query.order_by(Notes.id)
    return render_template('modules.html', all_notes=all_notes)

# Update  Notes to Modele
@app.route('/update_notes/<id>', methods=['GET', 'POST'])
@login_required
def update_notes(id):
    all_notes = Notes.query.order_by(Notes.id)
    return render_template('modules.html', all_notes=all_notes)

if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    app.run(debug=True)