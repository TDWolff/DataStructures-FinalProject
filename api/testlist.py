import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
import csv

from model.users import User

testlist_api = Blueprint('testlist_api', __name__,
                   url_prefix='/api/tests')

api = Api(testlist_api)

class TestListAPI:
    class _tlist(Resource):
        def get(self):
            with open('tests.csv', 'r') as f:
                reader = csv.DictReader(f)
                tests = []
                for row in reader:
                    # Open the CSV file specified in the Path column
                    with open(row['Path'], 'r') as test_file:
                        test_reader = csv.reader(test_file)
                        # Skip the header line
                        next(test_reader)
                        # Get the first question
                        first_question = next(test_reader)[0]
                        tests.append(f"{first_question}, {row['Level']}")
            if not tests:
                return {'message': 'No tests found'}, 404
            return jsonify(tests)
    
    api.add_resource(_tlist, '/testlist')