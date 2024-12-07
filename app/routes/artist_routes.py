from flask import Blueprint, request, jsonify
from app.models import Artist
from app.utils.s3_utils import upload_file_to_s3
from flasgger import swag_from
from datetime import datetime
from urllib.parse import urlparse


bp = Blueprint('artist_routes', __name__)

@bp.route('', methods=['POST'], strict_slashes=False)
@swag_from({
    'tags': ['Artists'],
    'parameters': [
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Name of the artist'
        },
        {
            'name': 'link_x',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Link X of the artist'
        },
        {
            'name': 'style',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Style of the artist'
        },
        {
            'name': 'x_tag',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'X tag of the artist'
        }
    ],
    'responses': {
        201: {
            'description': 'Artist created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
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
    name = request.form.get('name')
    link_x = request.form.get('link_x')
    style = request.form.get('style')
    x_tag = request.form.get('x_tag')

    if not name or not style:
        return jsonify({'error': 'Artist name and style are required'}), 400

    if link_x:
        parsed_url = urlparse(link_x)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return jsonify({'error': 'Invalid URL format for link_x'}), 400

    data = {
        'name': name,
        'style': style,
        'link_x': link_x,
        'x_tag': x_tag
    }

    try:
        new_artist = Artist.create(data)
        return jsonify(new_artist.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@bp.route('', methods=['GET'], strict_slashes=False)
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
                        'name': {'type': 'string'},
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
    name = request.args.get('name')
    created_at = request.args.get('created_at')

    if style:
        filters['style'] = style
    if name:
        filters['name'] = {'like': f'%{name}%'}
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
    'parameters': [
        {
            'name': 'artist_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the artist'
        },
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': False,
            'description': 'Avatar file of the artist'
        }
    ],
    'responses': {
        200: {
            'description': 'Artist retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
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
                s3_url = upload_file_to_s3(file, location=Artist.__tablename__)
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
