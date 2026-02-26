from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from src.db import get_db
from src.auth import login_required

bp = Blueprint("rwumfind",__name__)


# helper functions

def match_links(link1, link2):
    pass

# end of helper functions


# routes


@bp.route('/')
def index():
    db = get_db()
    error = None
    if g.user['id']:
        user_ad_links = db.execute('SELECT ad_link from posts WHERE posts.user_id = ?', (g.user['id'],)).fetchall()
        session['ad_links'] = [row['ad_link'] for row in user_ad_links
    posts = db.execute('SELECT p.id,  p.room_count, p.post_type, p.monthly_rent, p.created_at, p.monthly_rent, p.city, p.village, p.ad_link, p.user_id, u.email as user_mail '
        'FROM posts  p JOIN users u ON p.user_id = u.id '            
        'ORDER BY p.created_at DESC').fetchall()
     #  
    
    return render_template('rwumfind/index.html', posts=posts)
    



"""
-- Table: posts
CREATE TABLE IF NOT EXISTS  posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    room_dimensions VARCHAR(120),
    monthly_rent INTEGER,
    non_advance_monthly_rent INTEGER DEFAULT 0,
    from_owner INTEGER DEFAULT 0,
    bills_included_on_rent BOOLEAN DEFAULT 0,
    deposit_factor INTEGER DEFAULT 1,
    commission_factor INTEGER DEFAULT 1,
    payment_interval INTEGER,
    posting_type VARCHAR(30) CHECK (posting_type IN ('need_roommate', 'need_room_and_roommate')) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    link_id INTEGER REFERENCES links(id),
    user_id INTEGER REFERENCES users(id),
    location_id INTEGER REFERENCES locations(id)
);


"""



@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        error = None
        post_type = request.form['post_type']

        if post_type is None:
            error = "Post type is required"
        
        ad_link = request.form['ad_link']
        monthly_rent = request.form['monthly_rent']
        currency = request.form['currency']
        city = request.form['city']
        village = request.form['village']
        room_count = request.form['room_count']

        if error is not None:
            flash(error)
        
        else:
            db = get_db()       # 
            db.execute(
                'INSERT INTO posts (post_type, ad_link, monthly_rent, city, village, room_count, user_id, currency) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (post_type, ad_link, int(monthly_rent), city, village, room_count, g.user['id'], currency))
            db.commit()
            return redirect(url_for('rwumfind.index'))
        
    return render_template('rwumfind/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, p.user_id,  p.post_type, p.ad_link, p.monthly_rent, p.city, p.village, p.currency, p.room_count'
        ' FROM posts p JOIN users u ON p.user_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['user_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        error = None
        post_type = request.form['post_type']

        if post_type is None:
            error = "Post type is required"
        
        ad_link = request.form['ad_link']
        monthly_rent = request.form['monthly_rent']
        currency = request.form['currency']
        city = request.form['city']
        village = request.form['village']
        room_count = request.form['room_count']

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE posts SET post_type = ?, ad_link = ?, monthly_rent = ?, currency = ?, city = ?, village = ?, room_count = ? '
                ' WHERE id = ?',
                (post_type, ad_link, monthly_rent, currency, city, village, room_count, id)
            )
            db.commit()
            return redirect(url_for('rwumfind.index'))

    return render_template('rwumfind/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('rwumfind.index'))



def search_for_posts():
    pass

def group_posts():
    pass

