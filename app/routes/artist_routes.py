from flask import Blueprint, request, jsonify
from app.models import Artist
from app.utils.s3_utils import upload_file_to_s3
from flasgger import swag_from
from datetime import datetime


bp = Blueprint('artist_routes', __name__)

@bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Artists'],
    'responses': {
        201: {
            'description': 'Artist created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'artist_name': {'type': 'string'},
                    'link_x': {'type': 'string'},
                    'style': {'type': 'string'},
                    'x_tag': {'type': 'string'},
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
def create_artist():
    artist_name = request.form.get('artist_name')
    link_x = request.form.get('link_x')
    style = request.form.get('style')
    x_tag = request.form.get('x_tag')

    if not artist_name or not style:
        return jsonify({'error': 'Artist name and style are required'}), 400

    data = {
        'artist_name': artist_name,
        'style': style,
        'link_x': link_x,
        'x_tag': x_tag
    }

    try:
        new_artist = Artist.create(data)
        return jsonify(new_artist.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Artists'],
    'responses': {
        200: {
            'description': 'List of artists',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'artist_name': {'type': 'string'},
                        'link_x': {'type': 'string'},
                        'style': {'type': 'string'},
                        'x_tag': {'type': 'string'},
                        'avatar': {'type': 'string'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        }
    }
})
def get_artists():
    filters = {}
    style = request.args.get('style')
    artist_name = request.args.get('artist_name')
    created_at = request.args.get('created_at')

    if style:
        filters['style'] = style
    if artist_name:
        filters['artist_name'] = {'like': f'%{artist_name}%'}
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
    
    artists = Artist.list(filters, order_by)
    return jsonify([artist.to_dict() for artist in artists])


@bp.route('/<int:artist_id>', methods=['PUT', 'GET'])
@swag_from({
    'tags': ['Artists'],
    'responses': {
        200: {
            'description': 'Artist retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'artist_name': {'type': 'string'},
                    'link_x': {'type': 'string'},
                    'style': {'type': 'string'},
                    'x_tag': {'type': 'string'},
                    'avatar': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        404: {
            'description': 'Artist not found'
        }
    }
})
def get_or_update_artist(artist_id):
    artist = Artist.get(artist_id)
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404

    if request.method == 'GET':
        return jsonify(artist.to_dict()), 200

    if request.method == 'PUT':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                s3_url = upload_file_to_s3(file)
                artist.avatar = s3_url

        artist.save()
        return jsonify(artist.to_dict()), 200


@bp.route('/<int:artist_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Artists'],
    'responses': {
        200: {
            'description': 'Artist deleted successfully'
        },
        404: {
            'description': 'Artist not found'
        }
    }
})
def delete_artist(artist_id):
    artist = Artist.get(artist_id)
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404
    artist.delete()
    return jsonify({'message': 'Artist deleted'}), 200
