import os

from flask import Flask

def create_app(test_config=None):
    """
    - app = Flask ..
      - Creates flask instance
    - instance_relative tells app config files are relative to
      instance folder
    - Instance folder exists outside src and has data that
      should not go to VCS.
    - app.confing.from_mapping: default configuration
      - dev is unsafe but good enough for a dev secret key
      - DATABASE, path to the sqlite file
    - config from py file: values taken from config.py in instance
      folder.
    - Then the creation of the instance folder if it don't exist.
    - DB is initialized with flask --app src init-db
    """
    app = Flask(__name__, instance_relative_config=None)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'src.sqlite'),
        )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    
    # @app.route('/')
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    # registering a blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # rwumfind's index same as root index
    from . import rwumfind
    app.register_blueprint(rwumfind.bp)
    app.add_url_rule('/', endpoint='index')

    return app
