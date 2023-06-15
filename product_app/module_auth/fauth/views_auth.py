from flask import Blueprint, session, render_template, abort, request, redirect, url_for, flash, get_flashed_messages
from product_app import db
from product_app.module_auth.model.user import User, LoginForm, RegisterForm
from flask_login import login_user, logout_user, current_user, login_required
from product_app import login_manager

fauth=Blueprint('fauth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
@fauth.route('/register', methods=('GET','POST'))
def register(): 
    #if session.get('username'):
    if 'username' in session:
        print(session['username']) 
          
    form=RegisterForm(meta={'csrf':False})
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('El usuario ya existe en el sistema', 'danger')
        else:
            p=User(form.username.data, form.password.data)
            db.session.add(p)
            db.session.commit()
            flash('Usuario creado con exito')
            return redirect(url_for('fauth.register'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/register.html', form=form)

@fauth.route('/login', methods=('GET','POST'))
def login():
    if current_user.is_authenticated:
        flash('Ya estas autenticado')
        return redirect(url_for('product.index'))
        
    form=LoginForm(meta={'csrf':False})
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Bienvenido denuevo ' + user.username)
            
            next=request.form['next']
            #if not is_safe_url(next):
            #    abotr(400)
            
            return redirect(next or url_for('product.index'))
            pass
        else:
            flash('Usuario o contrasena inconrrecto', 'danger')

    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/login.html', form=form)

@fauth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('fauth.login'))
    