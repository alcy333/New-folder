from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            existing_user = User.query.filter(
                func.lower(User.email) == func.lower(form.email.data.strip()) |
                func.lower(User.username) == func.lower(form.username.data.strip())
            ).first()
            
            if existing_user:
                flash('Email or username already exists', 'danger')
                return render_template('register.html', form=form)

            user = User(
                username=form.username.data.strip(),
                email=form.email.data.strip().lower()
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))

        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error: {str(e)}')
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)  # Proper usage
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))