from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv

from endpoints.template_endpoint import *

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

api.add_resource(TemplateEndpoint, '/template_get')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    load_dotenv()
    app.run(host="0.0.0.0",debug=True, port=1338)