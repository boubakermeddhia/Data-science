import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mxktqvdzpeeteg:00b868962d778ae0e85a19e47da434f7413c3f6d84178f2d957b5421e626e613@ec2-35-173-94-156.compute-1.amazonaws.com:5432/d427kpvudu9nnu'

db = SQLAlchemy(app)



from scrape import routes