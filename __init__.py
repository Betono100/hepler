from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
# from flask_session import Session
# from flask_mail import Mail, Message
from hepler.UserLogin import UserLogin
import os
import json
import datetime

app = Flask(__name__)
login_manager = LoginManager(app)


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:Neet2001@localhost:3306/helper?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app_root = os.path.dirname(os.path.abspath(__file__))

# DB Model USER
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)


# DB Model CATEGORIES
class Categories(db.Model):
    category_name = db.Column(db.String(200), nullable=False, primary_key=True)

# DB Model SUBCATEGORIES
class Subcategories(db.Model):
    category_name = db.Column(db.String(200), nullable=False, primary_key=True)
    category = db.Column(db.String(200), db.ForeignKey("categories.category_name"))

# DB Model CONTENT
class Content(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.TEXT(), nullable=False)
    category = db.Column(db.String(200), db.ForeignKey("subcategories.category_name"))
    date = db.Column(db.DateTime(), default=datetime.datetime.now())


# --- AUTHORIZATION ---

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDataBase(user_id, User)


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    """Auth user"""
    if request.method == "POST":
        user_data = User.query.filter_by(login=request.form['login']).first()
        print(user_data.password)
        if user_data.password == request.form['password'] and user_data.login == request.form['login']:
            user_login = UserLogin().create(user_data)
            login_user(user_login)

            return redirect(url_for('main'))
        # flash('Ошибка')
    return render_template('auth.html')

# ---


@app.route('/main')
@login_required
def main():
    """Main page"""
    category = Categories.query.all()
    sub_category = Subcategories.query.all()
    data_category = {}
    for i in category:
        data_category[i.category_name] = [sub.category_name for sub in sub_category if sub.category == i.category_name]

   
    return render_template('index.html', category=data_category)


@app.route('/get_content/<string:category>')
def get_content_by_category(category):
    """GET CONTENTS BY CATEGOTY"""
    content = Content.query.filter_by(category=category).first()
    data_content = {}
    data_content[category] = {'title': content.title, 'text': content.text, 'date': content.date}


    return jsonify(data_content)

@app.route('/get_content_text/<string:text_search>')
def get_content_by_text(text_search):
    """GET CONTENTS BY TEXT"""
    text_search = text_search
    print(text_search)
    content = Content.query.all()
    search_content = [i for i in content if text_search in i.text]
    content = search_content[0]
    data_content = {}
    data_content[content.category] = {'title': content.title, 'text': content.text, 'date': content.date}


    return jsonify(data_content)


@app.route('/')
def main_auth():
    """Main page AUTH"""
    
    return render_template('auth.html', category=None)


if __name__ == '__main__':
    db.create_all()
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=5001)
    # Session(app)
