from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'simple'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mynetworkin4@gmail.com'
app.config['MAIL_PASSWORD'] = 'Aluta.1_$@'

db = SQLAlchemy(app)
cache = Cache(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Integer, default=0)
    tap_capacity = db.Column(db.Integer, default=1)
    storage_capacity = db.Column(db.Integer, default=1000)
    recharge_speed = db.Column(db.Integer, default=1)
    theme = db.Column(db.String(50), default='default')
    referral_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    first_level_referrals = db.relationship('User', backref=db.backref('referral', remote_side=[id]), lazy=True)
    referral_rewards_last_claim = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='sha256')
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    first_level_usernames = [u.username for u in user.first_level_referrals]
    return render_template('profile.html', user=user, first_level_usernames=first_level_usernames)

@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('tasks.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/boost_tap', methods=['POST'])
def boost_tap():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    user = User.query.get(session['user_id'])
    cost = user.tap_capacity * 10
    if user.balance >= cost:
        user.balance -= cost
        user.tap_capacity += 1
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Not enough balance'})

@app.route('/boost_storage', methods=['POST'])
def boost_storage():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    user = User.query.get(session['user_id'])
    cost = user.storage_capacity // 2
    if user.balance >= cost:
        user.balance -= cost
        user.storage_capacity += 500
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Not enough balance'})

@app.route('/boost_recharge_speed', methods=['POST'])
def boost_recharge_speed():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    user = User.query.get(session['user_id'])
    cost = user.recharge_speed * 20
    if user.balance >= cost and user.recharge_speed < 10:
        user.balance -= cost
        user.recharge_speed += 1
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Not enough balance or max level reached'})

@app.route('/referral_rewards', methods=['POST'])
def referral_rewards():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    user = User.query.get(session['user_id'])
    now = datetime.utcnow()
    if now - user.referral_rewards_last_claim >= timedelta(hours=4):
        first_level_rewards = sum(u.balance * 0.1 for u in user.first_level_referrals)
        second_level_users = User.query.filter(User.referral_id.in_([u.id for u in user.first_level_referrals])).all()
        second_level_rewards = sum(u.balance * 0.05 for u in second_level_users)
        total_rewards = first_level_rewards + second_level_rewards
        user.balance += total_rewards
        user.referral_rewards_last_claim = now
        db.session.commit()
        return jsonify({'success': True, 'rewards': total_rewards})
    return jsonify({'success': False, 'message': 'Rewards already claimed recently'})

@app.route('/update_theme', methods=['POST'])
def update_theme():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    user = User.query.get(session['user_id'])
    new_theme = request.json['theme']
    user.theme = new_theme
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
