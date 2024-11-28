from flask import Blueprint, request, jsonify
from app.models import Team
from app.utils.s3_utils import upload_file_to_s3
from flasgger import swag_from
from datetime import datetime


bp = Blueprint('team_routes', __name__)

@bp.route('', methods=['POST'], strict_slashes=False)
@swag_from({
    'tags': ['Teams'],
    'responses': {
        201: {
            'description': 'Team created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'position': {'type': 'varchar'},
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
    name = request.form.get('name')
    description = request.form.get('description')
    position = request.form.get('position')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    data = {
        'name': name,
        'description': description,
        'position': position
    }

    try:
        new_team = Team.create(data)
        return jsonify(new_team.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@bp.route('', methods=['GET'], strict_slashes=False)
@swag_from({
    'tags': ['Teams'],
    'responses': {
        200: {
            'description': 'List of teams',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'description': {'type': 'string'},
                        'position': {'type': 'varchar'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        }
    }
})
def get_teams():
    filters = {}
    name = request.args.get('name')
    position = request.args.get('position')
    if name:
        filters['name'] = name
    if position:
        filters['position'] = position
    if created_at:
        try:
            created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S')
            filters['created_at'] = {'gte': created_at}
        except ValueError:
            return jsonify({'error': 'Invalid created_at format. Use ISO 8601 format.'}), 400
    
    order_by = []
    order_fields = request.args.getlist('order_by')
    for field in order_fields:
        field_name, direction = field.split(':')
        order_by.append((field_name, direction))
    
    teams = Team.list(filters, order_by)
    return jsonify([team.to_dict() for team in teams])


@bp.route('/<int:team_id>', methods=['PUT', 'GET'])
@swag_from({
    'tags': ['Teams'],
    'responses': {
        200: {
            'description': 'Team updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'position': {'type': 'varchar'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        404: {
            'description': 'Team not found'
        }
    }
})
def get_or_update_team(team_id):
    team = Team.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404

    if request.method == 'GET':
        return jsonify(team.to_dict()), 200

    if request.method == 'PUT':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                s3_url = upload_file_to_s3(file, Team.__tablename__)
                team.avatar = s3_url


        try:
            team.save()
            return jsonify(team.to_dict()), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400


@bp.route('/<int:team_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Teams'],
    'responses': {
        200: {
            'description': 'Team deleted successfully'
        },
        404: {
            'description': 'Team not found'
        }
    }
})
def delete_team(team_id):
    team = Team.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    team.delete()
    return jsonify({'message': 'Team deleted'}), 200

