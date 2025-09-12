from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db   # Import the database instance from __init__.py
from flask_login import login_user, login_required, logout_user, current_user

# Blueprint for authentication-related routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route: Handles user login via email and password.
    On successful login, redirects to the home page.
    """
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Look for user in the database
        user = User.query.filter_by(email=email).first()

        if user:
            # Verify password using hash
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # Log in the user
                return redirect(url_for('views.welcome'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    Logout route: Logs out the current user and redirects to login page.
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Sign-up route: Creates a new user if the input is valid.
    Logs in the new user and redirects to the home page.
    """
    if request.method == 'POST':
        # Get form input values
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if user already exists
        user = User.query.filter_by(email=email).first()

        # Input validation checks
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create new user with hashed password
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )

            # Add and commit to the database
            db.session.add(new_user)
            db.session.commit()

            # Automatically log in new user
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.welcome'))

    return render_template("sign_up.html", user=current_user)
