from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user = User(**user_data)  # Vulnerable to mass assignment
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

# Vulnerable API signup route (susceptible to mass assignment)
@app.route('/api/signup', methods=['POST'])
def api_signup():
    user_data = request.json
    user = User(**user_data)  # Vulnerable to mass assignment
    db.session.add(user)
    db.session.commit()
    return {'message': 'Account created successfully!'}, 201

# Secure API signup route
@app.route('/api/secure_signup', methods=['POST'])
def api_secure_signup():
    data = request.json
    if not all(k in data for k in ('email', 'password', 'name')):
        return {'message': 'Missing required fields'}, 400
    
    user = User(
        email=data['email'],
        password=data['password'],
        name=data['name'],
        is_admin=False  # Explicitly set to False
    )
    db.session.add(user)
    db.session.commit()
    return {'message': 'Account created successfully!'}, 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)