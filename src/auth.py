import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from src.db import get_db

# TODO: confiure mailer "from mailer import Mailer"

# __name__ so the bp can know where it is defined.
# covers all urls prepended with /auth
# is called 'auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')


# helper functions

def email_format_is_valid(email):
    # TODO regex
    return True

def get_current_timestamp():
    return datetime.datetime.now().timestamp()

# end of helper functions


# blue prints


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender'].lower()

        
        # TODO: schools from edu emails. school = request.form.get('school')
        major = request.form.get('major')
        yoe = request.form.get('yoe')
        profile_description = request.form.get('profile_description')

        
        db = get_db()
        error = None

        if not email_format_is_valid(email):
            error = "Email format invalid. Email must be a .edu or student email."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (fname, lname, password_hash, email, gender, uni_major, year_of_school, profile_description, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (fname, lname, generate_password_hash(password), email, gender, major, yoe, profile_description, username))
                db.commit()
            except Exception as e:
                error = f"Error: {e} ."
            else:
                # TODO: return redirect(url_for("auth.validate_email")) 
                return redirect(url_for("index"))

        flash(error)

    return render_template("auth/register.html")



@bp.route('/validate_email/<string:email>', methods=('GET','POST'))
def validate_email(email):
    # TODO
    if request.method == 'POST':
        confirmation_code = request.form['confirmation_code']
        db = get_db()
        error = None
        # email confirmation logic
        timestamp = db.execute(
            'SELECT timespamp, confirmation_code FROM email_validation where email = ?', (email, confirmation)
        )
        if timestamp is not None:
            current_timestamp = get_current_timestamp()
            if timestamp < current_timestamp:
                error = "Code is expired"
            else:
                user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        else:
            error = "Unrecognized email"
                
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    
    return render_template('auth/validate_email.html')

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #TODO: parse profile photo and turn to bs64
         
        db = get_db()
        print(db)
        error = None
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        # user_ad_links = db.execute('SELECT p.ad_link from posts p JOIN users u ON p.user_id = u.id').fetchall()
        if user is None or (not check_password_hash(user['password_hash'], password)):
            error = 'Incorrect credentials'
            flash(error)
            return render_template('auth/login.html')
        user_ad_links = db.execute('SELECT ad_link from posts WHERE posts.user_id = ?', (user['id'],)).fetchall()
        # if user_ad_links is None:
        #     user_ad_links = []
        # else:
        #     user_ad_links = user_ad_links.fetchall()
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['ad_links'] = [row['ad_link'] for row in user_ad_links]
            print(session['ad_links'])
            # url for: generate url for a view based on name and args.
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()


# decorators

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        #if g.user is None:
        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
