from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_user, login_required
# from flask_session import Session
# from flask_mail import Mail, Message
# from UserLogin import UserLogin
import os
import json

app = Flask(__name__)
# login_manager = LoginManager(app)


app.config['SECRET_KEY'] = 'secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:2110@localhost:3306/helper?charset=utf8mb4'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app_root = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def main():
    """Main page"""
    return render_template('index.html')


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
    # Session(app)