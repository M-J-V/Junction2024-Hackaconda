from flask_restful import Resource
from flask import request

from survall import Survall
from objects.question import Question
from objects.answer import Answer
from objects.user_question import UserQuestionPair
from objects.authentication import Authentication

class RequestQuestion(Resource):
    def get(self):
        authentication:Authentication = Survall().authenticate(request.headers.get('Authorization'))
        if authentication is None: return 401

        question:Question = Survall().get_question(authentication.user_hash)

        # If there is no valid question to ask return a error code
        if question is None:
            return None, 204

        return question.to_dict_short(), 200
    
class AnswerQuestion(Resource):
    def post(self):
        data = request.get_json()

        authentication:Authentication = Survall().authenticate(request.headers.get('Authorization'))
        if authentication is None: return 401

        answer:Answer = Answer.from_dict(data)

        data['user_uuid'] = authentication.user_hash
        user_question_pair:UserQuestionPair = UserQuestionPair.from_dict(data)

        Survall().save_answer(answer, user_question_pair)

        related_question = Survall().get_question_by_id(answer)
        Survall().generate_new_question(related_question)

        print(related_question)

        return related_question.to_json(), 200
    
class PreviousQuestions(Resource):
    def get(self):
        authentication:Authentication = Survall().authenticate(request.headers.get('Authorization'))
        if authentication is None: return 401

        print(authentication.user_hash)

        previous_questions = Survall().get_previous_questions(authentication)

        previous_questions_dict_list = [question.to_dict() for question in previous_questions]

        return previous_questions_dict_list, 200
    
class RelatedQuestions(Resource):
    def post(self):
        authentication:Authentication = Survall().authenticate(request.headers.get('Authorization'))
        if authentication is None: return 401

        print(authentication.user_hash)

        data = request.get_json()
        question:Question = Question.from_dict(data)

        related_questions = Survall().get_related_questions(question)
        related_questions_dict_list = [question.to_dict() for question in related_questions]

        return related_questions_dict_list, 200
    
class ClosedQuestions(Resource):
    def get(self):
        authentication:Authentication = Survall().authenticate(request.headers.get('Authorization'))
        if authentication is None: return 401

        closed_questions = Survall().get_closed_questions()

        print(closed_questions)

        closed_questions_dict_list = [question.to_dict() for question in closed_questions]

        return closed_questions_dict_list, 200    

class BrewCoffee(Resource):
    def get(self):
        return 418