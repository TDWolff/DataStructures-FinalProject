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
    class _tests(Resource):
        def post(self):
            body = request.get_json()
            if body is None:
                return {'message': 'No data provided'}, 400
            if 'Path' not in body:
                return {'message': 'Path not provided'}, 400
            path = body['Path']
            try:
                with open(path, 'r') as f:
                    reader = csv.reader(f)
                    # Skip the first three lines
                    for _ in range(3):
                        next(reader)
                    # Skip the header row
                    next(reader)
                    # Get all remaining lines
                    questions = [row for row in reader]
                    return jsonify(questions)
            except FileNotFoundError:
                return {'message': 'File not found'}, 404
    api.add_resource(_tlist, '/testlist')
    api.add_resource(_tests, '/test')