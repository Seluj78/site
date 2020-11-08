import os

from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask_admin import Admin
from peewee import SqliteDatabase

AFPY_ROOT = os.path.join(os.path.dirname(__file__), "../")  # refers to application_top
dotenv_path = os.path.join(AFPY_ROOT, ".env")
load_dotenv(dotenv_path)

REQUIRED_ENV_VARS = ["FLASK_PORT", "FLASK_DEBUG", "FLASK_HOST", "FLASK_SECRET_KEY", "DB_NAME"]

for item in REQUIRED_ENV_VARS:
    if item not in os.environ:
        raise EnvironmentError(f"{item} is not set in the server's environment or .env file. It is required.")

from afpy.static import FLASK_SECRET_KEY, DB_NAME

database = SqliteDatabase(database=DB_NAME)

application = Flask(__name__)

if os.getenv("FLASK_DEBUG", "false") == "true" or os.getenv("FLASK_DEBUG", "false") == "1":
    application.debug = True
else:
    application.debug = False

application.secret_key = FLASK_SECRET_KEY
application.config.update(FLASK_SECRET_KEY=FLASK_SECRET_KEY)
application.config["FLASK_ADMIN_SWATCH"] = "lumen"


@application.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404


from afpy.routes.home import home_bp

application.register_blueprint(home_bp)


from afpy.models.AdminUser import AdminUser, AdminUser_Admin
from afpy.models.NewsEntry import NewsEntry, NewsEntry_Admin

# Creates the Admin manager
admin = Admin(application, name="Afpy Admin", template_mode="bootstrap3")

# Registers the views for each table
admin.add_view(AdminUser_Admin(AdminUser))
admin.add_view(NewsEntry_Admin(NewsEntry))
