from flask import Flask

from src.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)
