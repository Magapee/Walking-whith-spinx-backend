from FlaskTemplate import app
from flask_sqlalchemy import SQLAlchemy 
from .config import BaseConfig as Config
from flask import jsonify
from flask_migrate import Migrate

app.config.from_object(Config)
db = SQLAlchemy(app)
#migrate = Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique = True)
    password_hash = db.Column(db.String)
    score = db.Column(db.Integer,default=0)
    email = db.Column(db.String,unique=True)
    def ser(self):
        return jsonify({'id':self.id,'username':self.username,'email':self.email,
                        'password_hash':self.password_hash})


#class Achievements(db.Model):
#    achiev_1 = db.Column(db.Integer)
#    achiev_2 = db.Column(db.Integer)
#    achiev_3 = db.Column(db.Integer)
#    achiev_4 = db.Column(db.Integer)
#    def get_Achievements(self):
#        return {"1":self.achiev_1,"2":self.achiev_2,"3":self.achiev_3,"4":self.achiev_4}

#class Questions(db.Model):
#    id = db.Column(db.Integer,primary_key=True)
#    text_of_question = db.Column(db.String)
    
    #type_of_question = db.Column(db.Integer)

class Answers(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    answer1 = db.Column(db.String)
    answer2 = db.Column(db.String)
    answer3 = db.Column(db.String)
    answer4 = db.Column(db.String,default="null")
    answer5 = db.Column(db.String,default="null")
    answer6 = db.Column(db.String,default="null")
    correct_answer = db.Column(db.Integer,default=-1)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'),nullable=False)
    def get_Answers(self):
        output_dict = {'answers':{'answer1':self.answer1,'answer2':self.answer2,'answer3':self.answer3}}
        count_of_questions = 3
        if (self.answer4!='null'):
            output_dict['answers'].update({'answer4':self.answer4})
            count_of_questions+=1
        if (self.answer5!='null'):
            output_dict['answers'].update({'answer5':self.answer5})
            count_of_questions+=1
        if (self.answer6!='null'):
            output_dict['answers'].update({'answer6':self.answer6})
            count_of_questions+=1
        output_dict.update({'count_of_answers':count_of_questions,'correct_answer':self.correct_answer})
        return output_dict

class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String,nullable=False)
    answers = db.relationship('Answers',backref='question',uselist=False)
    def get_Question(self):
        return {'id_question':self.id,'text':self.text}
    def get_Answers(self):
        return self.answers.get_Answers()


db.create_all()
