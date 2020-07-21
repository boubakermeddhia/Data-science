import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://suljevvezarygo:2b8061cd3ee09ef09428764e6db15b206631ba2744d17403855bfd289f1442a7@ec2-54-234-28-165.compute-1.amazonaws.com:5432/d9qtve3lvoe1fg'

db = SQLAlchemy(app)



from scrape import routes