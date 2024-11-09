from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from openai import OpenAI
from dotenv import load_dotenv

from endpoints.questions_endpoint import AnswerQuestion, RequestQuestion

from survall import Survall
from endpoints.openai_endpoint import RequestOpenAi

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai = OpenAI()

Survall().setup(openai)

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

# @app.errorhandler(Exception)
# def handle_exception(e):
#     print(e)

#     # You could log the error here, if desired
#     response = {
#         "message": "An internal error occurred. Please try again later."
#     }
#     return response, 500

api.add_resource(RequestQuestion, '/get_question')
api.add_resource(AnswerQuestion, '/post_answer')
api.add_resource(RequestOpenAi, '/get_openai')

if __name__ == '__main__':
    pass

    #app.run(host="0.0.0.0",debug=True, port=1337)


        