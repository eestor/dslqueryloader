from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_script import Shell
from flask_migrate import MigrateCommand
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
migrate = Migrate(app, db)
admin = Admin(app, 'DSQueryLoader Admin Page')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from src.controllers.authentication import auth
from src.controllers.main import main
from src.controllers.schemas import schemas
from src.controllers.errors import page_not_found, internal_server_error

from src.models.role import Role
from src.models.user import User, AnonymousUser
from src.models.ds_schema import DsSchema

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(schemas)

def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User, Schema=DsSchema)

manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))

admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(DsSchema, db.session))
