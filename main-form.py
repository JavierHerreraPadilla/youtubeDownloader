from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from time import sleep

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/files/'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
db.create_all()


@app.route('/')
def home():
    print(current_user)
    print(current_user.__dict__)
    print(current_user.__dict__.get('name'))
    return render_template("index.html", logged_in=current_user)


@app.route('/register', methods=["POST", "GET"])
def register():
    print(len(User.query.all()))
    error = None
    if request.method == "POST":
        form_data = request.form
        all_emails = [user.email for user in User.query.all()]
        if form_data.get('email') in all_emails:
            error = 'El correo ya está registrado. Ingresa!'
            return redirect(url_for('login', registered_error=error))
        hashed_password = generate_password_hash(form_data.get('password'),
                                                 method='pbkdf2:sha256',
                                                 salt_length=8)
        new_user = User(
            email=form_data.get('email'),
            password=hashed_password,
            name=form_data.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        print(form_data, len(User.query.all()))
        return redirect(url_for('secrets', name=form_data.get('name')))
    return render_template("register.html", logged_in=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    email_error = None
    pass_error = None
    reg_error = request.args.get('registered_error')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        #all_emails = [user.email for user in User.query.all()]
        if not user:
            email_error = 'Correo no requistrado'
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('secrets', name=user.name))
            else:
                pass_error ='Contraseña incorrecta.'
    if email_error:
        error = email_error
    elif pass_error:
        error = pass_error
    else:
        error = None

    return render_template("login.html", error=error, reg_error=reg_error, logged_in=current_user)


@app.route('/secrets')
@login_required
def secrets():
    name = request.args.get('name')
    return render_template("secrets.html", name=name, logged_in=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download/')
@login_required
def download():
    return send_from_directory('static/files/', 'cheat_sheet.pdf', as_attachment=True)


@app.route('/del')
def delete_all_users():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
        db.session.commit()
    return 'All users deleted'


if __name__ == "__main__":
    app.run(debug=True)
