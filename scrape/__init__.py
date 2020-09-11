import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
UPLOAD_FOLDER = './scrape/static/csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analysisstocks.db'

db = SQLAlchemy(app)



from scrape import routes