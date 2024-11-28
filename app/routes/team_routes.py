from flask import Blueprint, request, jsonify
from flasgger import swag_from

bp = Blueprint('team_routes', __name__)

@bp.route('/', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Team created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'team_name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'avatar': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {
            'description': 'Invalid input'
        }
    }
})
def create_team():
    # Add logic to create team
    return jsonify({'message': 'Team created successfully'}), 201

@bp.route('/', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of teams',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'team_name': {'type': 'string'},
                        'description': {'type': 'string'},
                        'avatar': {'type': 'string'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        }
    }
})
def get_teams():
    # Add logic to return list of teams
    return jsonify({'teams': []}), 200