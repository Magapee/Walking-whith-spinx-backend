"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,jsonify,request
from FlaskTemplate import app,loginManager
from .models import User,db,Question,Answers


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/api/register', method = ['POST'])
def registration():
    pass


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/api/create_question',methods=['POST'])
def create_question():
    if (request.method=='POST'):
        data =request.get_json()
        text = data['text']
        q = Question(text=text)
        answers = Answers(answer1='Da',answer2='Net',answer3='Ya gay',answer4='huy',correct_answer=0)
        q.answers = answers
        db.session.add(q)
        db.session.commit()
        return jsonify(data)


@app.route('/api/get_question',methods=['POST'])
def get_question():
    if(request.method=='POST'):
        data = request.get_json()
        try:
            id_question = data['id_question']
        except KeyError:
            output_data = jsonify({'ERROR':'ID doesnt exist'})
            return output_data
        question = Question.query.get(id_question)
        if question is not None:
            output_data = question.get_Question()
            output_data.update(question.get_Answers())
            output_data = jsonify(output_data)
        else:
            output_data = jsonify({'ERROR':'Question doesnt exist'})
        return output_data

#@app.route('/login_check')
#def check_login():

@app.route('/check')
def check():
   u = User(username="admin1232",email="admin123")
   db.session.add(u)
   db.session.commit()
   return jsonify({'size':len(User.query.all())})


@loginManager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/is_alive', methods = ['POST'])
def alive():
    resp = app.make_response(jsonify({"value" : "There should be a cookie"}))
    resp.set_cookie("testing", 'testing')
    return resp

