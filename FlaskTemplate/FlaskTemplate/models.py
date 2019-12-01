from FlaskTemplate import app, lm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy 
from .config import DevelopmentConfig as Config
from flask_mail import Mail
from flask import jsonify
from flask_migrate import Migrate

app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
mail.connect()
migrate = Migrate(app,db)


assosication_table = db.Table('association',db.Model.metadata,
                              db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                                        db.Column('block_id',db.Integer,db.ForeignKey('block.id'))
                                        )



#lm callback
@lm.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique = True)
    password_hash = db.Column(db.String)
    score = db.Column(db.Integer,default=0)
    email = db.Column(db.String,unique=True)
    random_code = db.Column(db.Integer,default=0)
    is_confirmed = db.Column(db.Integer,default=0)
    blocks = db.relationship('Block',backref='user_blocks',secondary=assosication_table,lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #blocks = db.Column(db.Integer,db.ForeignKey('block.id'))

    

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
    

    def get_Correct_Answer(self):
        return self.correct_answer


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
    block_id = db.Column(db.Integer,db.ForeignKey('block.id'),nullable=False)


    def get_Question(self):
        return {'text':self.text,'id_question':self.id}


    def get_Answers(self):
        return self.answers.get_Answers()

    def get_Correct_Answer_int(self):
        return self.answers.get_Correct_Answer()


    def get_Answer_str(self,number):
        #correct_answer = self.get_Correct_Answer_int()
        return self.get_Answers()['answers']['answer'+str(number)]


    def get_All(self):
        output_data = self.get_Question()
        output_data.update(self.get_Answers())
        return output_data


class Block(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    questions = db.relationship('Question',backref='block',lazy='dynamic')
    users = db.relationship('User',backref='block_users',secondary=assosication_table,lazy='dynamic')
    block_type = db.Column(db.Integer)

    def get_Questions(self):
        count_of_questions = 0
        output_data = {'questions':{}}
        for question in Question.query.filter_by(block_id=self.id):
            count_of_questions+=1
            output_data['questions'].update({str(count_of_questions):question.get_All()})
        output_data.update({'count':count_of_questions})
        return output_data


db.create_all()
