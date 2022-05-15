from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user
from UserLogin import UserLogin
import requests
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
    category = db.Column(db.String(200), db.ForeignKey(
        "categories.category_name"))

# DB Model CONTENT


class Content(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.TEXT(), nullable=False)
    category = db.Column(db.String(200), db.ForeignKey(
        "subcategories.category_name"))
    date = db.Column(db.DateTime(), default=datetime.datetime.now())

# DB Model Question


class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.TEXT(), nullable=False)

# DB Model Qu


class Answer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.TEXT(), nullable=False)
    question = db.Column(db.Integer(), db.ForeignKey("question.id"))
    next_question = db.Column(db.Integer(), db.ForeignKey("question.id"))

# --- AUTHORIZATION ---


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDataBase(user_id, User)


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    """Auth user"""
    if request.method == "POST":
        user_data = User.query.filter_by(login=request.form['login']).first()
        print(user_data)
        if user_data.password == request.form['password'] and user_data.login == request.form['login']:
            user_login = UserLogin().create(str(user_data.login))
            login_user(user_login)

            return redirect(url_for('main'))
        # flash('Ошибка')
    return render_template('auth.html')

# ---


def get_caregory():
    """Return category dict"""
    category = Categories.query.all()
    sub_category = Subcategories.query.all()
    data_category = {}
    for i in category:
        data_category[i.category_name] = [
            sub.category_name for sub in sub_category if sub.category == i.category_name]

    return data_category


@app.route('/main')
@login_required
def main():
    """Main page"""

    return render_template('index.html', category=get_caregory())


@app.route('/script/<string:id>')
def get_script_data(id):
    """Script logic"""
    question = Question.query.filter_by(id=id).first()
    answers = Answer.query.filter_by(question=id).all()
    data = {}
    data['question'] = {'text': question.text}
    data['answers'] = [{'text': i.text, 'next': i.next_question}
                       for i in answers]

    html = f'<div class="popup__form"><div class="popup__question"><p id="question">{question.text}</p></div><div class="popup__answers">'
    for i in answers:
        html += f'<button class="popup__answer-button" value="{i.next_question}">{i.text}</button>'
        
    if int(id) != 1:
        html += f'</div><button class="popup__answer-button" value="{int(id)-1}" style="background-color: silver; margin-top: 10px">Назад</button>' \
            '<button class="popup__answer-button" value="1" style="background-color: silver; margin-top: -5px;">В начало</button></div>'
    else:
        html += '</div><button class="popup__answer-button" value="1" style="background-color: silver; margin-top: 10px;">В начало</button></div>'

    return jsonify({'html': html})


@app.route('/label/<string:cat>')
@login_required
def label(cat):
    """Label page"""

    return render_template('label.html', category=get_caregory(), sub=cat, content=Content.query.filter_by(category=cat).all())


@app.route('/content/<string:id_>')
@login_required
def content(id_):
    """Content page"""

    return render_template('content.html', category=get_caregory(), content=Content.query.filter_by(id=id_).first())


@app.route('/get_content_text/<string:text_search>')
def get_content_by_text(text_search):
    """GET CONTENTS BY TEXT"""

    content = Content.query.all()
    search_content = [i for i in content if text_search in i.text]

    html = f'<div class="article__content"><div class="article__label"><div class="article__label-item"><h3 class="article__label-title">Поиск: {text_search}</h3><ul>'
    for i in search_content:
        html += f'<li><a href="/content/{i.id}"> • {i.title} </a><a href="/label/{i.category}"style="float: right;">{i.category}</a><br><span style="": right">{i.date}</span></li>'
    html += '</ul></div></div>'

    return jsonify({'html': html})


@app.route('/')
def main_auth():
    """Main page AUTH"""

    return render_template('auth.html', category=None)

def send_message_tg(message, username):
    message = message + '\n\n' + '@' + username
    token = '5305755369:AAEQKDy6d3KFaGzELPsFCO-ka91PfuC4t-s'
    id = '661213202'
    request = requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={message}')


@app.route('/send_message', methods=['POST', 'GET'])
@login_required
def send():
    """Send message"""

    if request.method == "POST":
        user = current_user.get_id().login
        message = request.form['message']
        send_message_tg(message, user)

        return redirect(url_for('main'))
    # print(User.query.filter_by(login=current_user.get_id()).first())
    
    return render_template('index.html', category=get_caregory())



if __name__ == '__main__':
    db.create_all()
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=5005)
    # Session(app)
