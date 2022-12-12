from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import models

app = Flask(__name__,template_folder='./frontend/templates',static_folder='./frontend/static')
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///database\sqlite.db"
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

