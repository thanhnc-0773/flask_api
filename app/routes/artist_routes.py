from flask import Blueprint, request, jsonify
from app.models import Artist
from app.utils.s3_utils import upload_file_to_s3
from flasgger import swag_from

bp = Blueprint('artist_routes', __name__)

@bp.route('/', methods=['POST'])
@swag_from({
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        s3_url = upload_file_to_s3(file)

    artist_name = request.form.get('artist_name')
    style = request.form.get('style')

    if not artist_name or not style:
        return jsonify({'error': 'Artist name and style are required'}), 400

    data = {
        'artist_name': artist_name,
        'style': style,
        'link_x': s3_url
    }

    try:
        new_artist = Artist.create(data)
        return jsonify(new_artist.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/', methods=['GET'])
@swag_from({
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
    if style:
        filters['style'] = style
    if artist_name:
        filters['artist_name'] = {'like': f'%{artist_name}%'}
    
    order_by = []
    order_fields = request.args.getlist('order_by')
    for field in order_fields:
        field_name, direction = field.split(':')
        order_by.append((field_name, direction))
    
    artists = Artist.list(filters, order_by)
    return jsonify([artist.to_dict() for artist in artists])

@bp.route('/<int:artist_id>', methods=['PUT', 'GET'])
@swag_from({
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
        artist_name = request.form.get('artist_name')
        style = request.form.get('style')

        if not artist_name or not style:
            return jsonify({'error': 'Artist name and style are required'}), 400

        artist.artist_name = artist_name
        artist.style = style

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                s3_url = upload_file_to_s3(file)
                artist.link_x = s3_url

        artist.save()
        return jsonify(artist.to_dict()), 200

@bp.route('/<int:artist_id>', methods=['DELETE'])
@swag_from({
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