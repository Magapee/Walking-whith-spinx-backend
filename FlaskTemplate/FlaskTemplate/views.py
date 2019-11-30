"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,jsonify,request
from FlaskTemplate import app,lm
from .models import User,db,Question,Answers,Block



#@app.route('/api/create_question',methods=['POST'])
#def create_question():
#    if (request.method=='POST'):
#        data =request.get_json()
#        text = data['text']
#        q = Question(text=text)
#        answers = Answers(answer1='Da',answer2='Net',answer3='Ya gay',answer4='huy',correct_answer=0)
#        q.answers = answers
#        db.session.add(q)
#        db.session.commit()
#        return jsonify(data)


@app.route('/api/get_block_info',methods=['POST'])
def get_block_info():
    if (request.method=='POST'):
        data = request.get_json()
        try:
            id_block = data['id_block']
        except KeyError: 
            output_data = jsonify({'ERROR':'ID in POST doesnt exist'})
            return output_data
        block = Block.query.get(id_block)
        if block is not None:
            output_data = block.get_Questions()
            return jsonify(output_data)
        else:
            output_data = jsonify({'ERROR':'Block doesnt exist'})
            return output_data


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

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

#@app.route('/check')
#def check():
#   u = User(username="admin1232",email="admin123")
#   db.session.add(u)
#   db.session.commit()
#   return jsonify({'size':len(User.query.all())})


@lm.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/api/check_answers',methods=['POST'])
def check_answers():
    if (request.method == 'POST'):
        data = request.get_json()
        return jsonify(data)


@app.route('/api/tablescore',methods=['GET','POST'])
def get_tablescore():
    q = User.query.order_by(User.score.desc())
    output_data = {'users':{}}
    count_of_users = 0
    for user in q.all():
        count_of_users += 1
        output_data['users'].update({count_of_users:{'score':user.score,'username':user.username}})
    output_data.update({'count_of_users':count_of_users})
    return jsonify(output_data)

@app.route('/check')
def check():
   u = User(username="admin1232",email="admin123")
   db.session.add(u)
   db.session.commit()
   return jsonify({'size':len(User.query.all())})
@lm.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

