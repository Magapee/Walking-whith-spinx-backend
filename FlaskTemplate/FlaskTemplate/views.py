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

#ПОЛУЧИТЬ ВОПРОСЫ И ИНФУ БЛОКА
#ПОЛУЧАЮ
#{
#	"id_block":"1"
#}
#ОТПРАВЛЯЮ
#{
#  "count": 2, // количество вопросов
#  "questions": {
#    "1": { // номер вопроса
#      "answers": {
#        "answer1": "1",
#        "answer2": "2", //варианты ответов
#        "answer3": "3",
#        "answer4": "4"
#      },
#      "correct_answer": 2, // правильный ответ
#      "count_of_answers": 4, // количество ответов
#      "text": "1" // сам вопрос
#    },
#    "2": {
#      "answers": {
#        "answer1": "1_2",
#        "answer2": "2_2",
#        "answer3": "3_2",
#        "answer4": "4_2"
#      },
#      "correct_answer": 4,
#      "count_of_answers": 4,
#      "text": "2"
#    }
#  }
#}

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


#ПОЛУЧИТЬ КОНКРЕТНЫЙ ВОПРОС?????
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





#ПРОВЕРКА ПОЛУЧЕННЫХ ОТВЕТОВ
#ПРОВЕРКА РЕЗУЛЬТАТОВ
#ПОЛУЧАЮ
#{
#	"id_block":"2", // айди блока
#	"username":"admin", // имя пользователя
#	"answers":{
#		"1":{//номер вопроса
#			"text":"1", //текст вопроса
#			"user_answer":"2" //ответ пользователя (номер ответа)
#		},
#		"2":{
#			"text":"2",
#			"user_answer":"3"
#		},
#		"count":"2" //количество вопросов для проверки
#	}
#}

#ОТПРАВЛЯЮ
#{
#  "block_id": "2", //айди блока
#  "result": {
#    "1": {
#      "status": "correct" //статус
#    },
#    "2": {
#      "correct_answer": "4_2", //правильный ответ (текст ответа)
#      "status": "mistake",
#      "user_answer": "3_2" //ответ пользователя (текст ответа)
#    }
#  }
#}
@app.route('/api/check_answers', methods=['POST'])
def check_answers():
    if (request.method == 'POST'):
        data = request.get_json()
        try:

            dict_of_answers = data['answers']
            username = data['username']
            block_id = data['id_block']

        except KeyError:

            output_data = jsonify({'ERROR':'ID doesnt exist'})
            return output_data

        b = Block.query.get(int(block_id))
        if (len(b.users.filter_by(username=username).all())>0):
            output_data = {'ERROR':'user has already passed the block'}
            return jsonify(output_data)

        user = User.query.filter_by(username=username).first()
        output_data = {'result':{},'block_id':block_id}
        for i in range(1,int(dict_of_answers['count'])+1):

            current_answers = dict_of_answers[str(i)]
            question = current_answers['text']
            question_id = int(current_answers['id_question'])
            user_answer = current_answers['user_answer']
            question = b.questions.filter_by(id=question_id).first()
            bd_correct_answer = question.get_Correct_Answer_int()
            bd_correct_answers = question.get_Answers()

            if (bd_correct_answer==int(user_answer)):
                output_data['result'].update({i:{'status':'correct'}})
                user.score+=1

            else:
                output_data['result'].update({i:{'status':'mistake','correct_answer':question.get_Answer_str(bd_correct_answer),'user_answer':question.get_Answer_str(user_answer)}})
        b.users.append(user)
        user.blocks.append(b)
        db.session.add(user)
        db.session.add(b)
        db.session.commit()
        return jsonify(output_data)




#ВЫВОД ТАБЛИЦ ЛИДЕРОВ
#ПОЛУЧАЮ
#ничего get/post
#ОТПРАВЛЯЮ
#{
#  "count_of_users": 3, // количество пользователя
#  "users": {
#    "1": {
#      "score": 100, // баллы
#      "username": "admin" // имя пользователя
#    },
#    "2": {
#      "score": 80,
#      "username": "dsadsadas"
#    },
#    "3": {
#      "score": 10,
#      "username": "2312"
#    }
#  }
#}
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





#ПОЛУЧИТЬ СПИСОК АКТИВНЫХ БЛОКОВ(для главного меню)
#ПОЛУЧАЮ
#{
#	"username":"test" // имя пользователя
#}
#ОТПРАВЛЯЮ
#{
#  "blocks": {
#    "1": 1, //блок активен
#    "2": 0 //блок неактивен
#  }
#}
@app.route('/api/get_active_blocks',methods=['POST'])
def get_active_blocks():
    if request.method=='POST':
        data = request.get_json()
        try:
            username = data['username']
        except KeyError:
            output_data = {'ERROR':'ID doesnt exist'}
            return jsonify(output_data)
        b = Block.query.all()
        output_data = {'blocks':{}}
        for block in b:
            if (block.users.filter_by(username=username).first() is not None):
                status = 1
            else:
                status = 0
            output_data['blocks'].update({block.id:status})
        return jsonify(output_data)



#ПОЛУЧИТЬ ПОЛЬЗОВАТЕЛЬСКУЮ ИНФОРМАЦИЮ
@app.route('/api/get_user_info',methods=['POST'])
def get_user_info():
    if request.method == 'POST':
        data = request.get_json()
        try:
            username = data['username']
        except KeyError:
            output_data = {'ERROR':'Username doesnt exist'}
            return jsonify(output_data)
        u = User.query.filter_by(username=username).all()
        if (len(u)>0):
            u = u[0]
            output_data = {'username':u.username,'score':u.score,'email':u.email,'active_blocks':{}}
            b = Block.query.all()
            for block in b:
                if (block.users.filter_by(username=username).first() is not None):
                    output_data['active_blocks'].update({block.id:'1'})
        else:
            output_data = {'ERROR':'User doesnt exist'}
        return jsonify(output_data)





#def get_Active_blocks(username):
#    b = Block.query.all()
#    output_data = {'blocks':{}}
#    for block in b:
#        if (block.users.filter_by(username=username).first() is not None):
#            status = 1
#        else:
#            status = 0
#        output_data['blocks'].update({block.id:status})
#    return output_data



#Registration
@app.route('/api/registration', methods = ['POST'])
def registration():
    data = request.get_json()
    try:
        username = data['login']
        email = data['email']
        password = data['password']
    except KeyError:
        return jsonify({'ERROR':'Wrong data'})
    
    if User.query.filter_by(username=username).first() is not None or User.query.filter_by(email=email).first() is not None:
        return jsonify({'result':'0'})
    
    user = User(username=username, email=email, password_hash=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'result':'1'})