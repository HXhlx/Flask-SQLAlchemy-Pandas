import sys
from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import Users, db

auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        User = Users.query.filter(or_(Users.Username == user, Users.Email == user)).first()
        if User and check_password_hash(User.Password, request.form['password']):
            session.clear()
            session['user_id'] = User.UserID
            return redirect(url_for('home.index'))
        else:
            return render_template('auth/login.html', error=sys.exc_info())
    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            User = Users(request.form['username'], request.form['email'], generate_password_hash(request.form['password']))
            db.session.add(User)
            db.session.commit()
            flash('注册成功! 将跳转到登录页面')
            return redirect(url_for('auth.login'))
        except:
            return render_template('auth/register.html', error=sys.exc_info())
    return render_template('auth/register.html')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = Users.query.filter_by(UserID=user_id).first()
    else:
        g.user = None


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return view(**kwargs)
        else:
            return redirect(url_for('auth.login'))

    return wrapped_view
