from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		user = Users.query.filter_by(username=username).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Logged in successfully!', category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password, try again.', category='error')
		else:
			flash('Username does not exist.', category='error')
	return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')

		user = Users.query.filter_by(username=username).first()
		if user:
			flash('Username already exists.', category='error')
		elif len(username) < 2:
			flash('Username must be greater than 1 character.', category='error')
		elif len(password) < 7 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
			flash('Password must be at least 7 characters with minimum 1 number, 1 Uppercase letter', category='error')
		elif password != confirm_password:
			flash('Passwords do not match.', category='error')
		else:
			new_user = Users(username=username, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=64))
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)
			flash('Account created!', category='success')
			return redirect(url_for('views.home'))
	return render_template("sign-up.html", user=current_user)
