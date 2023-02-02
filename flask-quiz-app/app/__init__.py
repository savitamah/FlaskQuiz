from flask import Flask
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
#postgres://app_klyb_user:hXNbIsd0F4Vw5toPStQcfOMbaz32BEI2@dpg-cfdnqj9gp3jolclpli00-a.oregon-postgres.render.com/app_klyb
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes

   