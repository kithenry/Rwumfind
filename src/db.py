import sqlite3
from datetime import datetime

"""
g: a special object unique for each request.
   a connection reused other than creating a new connection
   on recurrent connections
current app: a special object pointing to the app handling
             requests
sqlite3.connect: Establish a connection to the DATABASE
                 File DATABASE only exists after db initialization.
sqlite3.Row: Rows should behave like dicts.
             This allows access to columns by name.
close_db: Close connection if g.db is set.
          called after each request.


"""


import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        try:
            db.executescript(f.read().decode('utf8'))
        except Exception as e:
            print(f"Error: {e}")
            exit()
# define init-db commandline command
@click.command('init-db')
def init_db_command():
        """ Clear table and create new tables """
        init_db()
        click.echo()

sqlite3.register_converter(
        "timestamp", lambda v: datetime.fromisoformat(v.decode())
    )


def init_app(app):
    # function to call when cleaning app after returning a response
    app.teardown_appcontext(close_db)
    # function to add init_db_command to what fns can be called
    # with the flask command
    app.cli.add_command(init_db_command)
    
