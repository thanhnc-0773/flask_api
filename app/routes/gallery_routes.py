from flask import Blueprint, request, jsonify
from app.models import Gallery
from app.utils.s3_utils import upload_file_to_s3
from flasgger import swag_from
from datetime import datetime


bp = Blueprint('gallery_routes', __name__)

@bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Galleries'],
    'responses': {
        201: {
            'description': 'Gallery item created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'artist_id': {'type': 'integer'},
                    'picture': {'type': 'string'},
                    'show_on_top': {'type': 'boolean'},
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
def create_gallery():
    artist_id = request.form.get('artist_id')
    show_on_top = request.form.get('show_on_top', 'false').lower() == 'true'

    if not artist_id:
        return jsonify({'error': 'Artist ID is required'}), 400

    data = {
        'artist_id': artist_id,
        'show_on_top': show_on_top
    }

    try:
        new_gallery = Gallery.create(data)
        return jsonify(new_gallery.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Galleries'],
    'responses': {
        200: {
            'description': 'List of gallery items',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'artist_id': {'type': 'integer'},
                        'picture': {'type': 'string'},
                        'show_on_top': {'type': 'boolean'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        }
    }
})
def get_galleries():
    filters = {}
    artist_id = request.args.get('artist_id')
    show_on_top = request.args.get('show_on_top')
    if artist_id:
        filters['artist_id'] = artist_id
    if show_on_top:
        filters['show_on_top'] = show_on_top.lower() == 'true'
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
    
    galleries = Gallery.list(filters, order_by)
    return jsonify([gallery.to_dict() for gallery in galleries])


@bp.route('/<int:gallery_id>', methods=['PUT', 'GET'])
@swag_from({
    'tags': ['Galleries'],
    'responses': {
        200: {
            'description': 'Gallery item updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'artist_id': {'type': 'integer'},
                    'picture': {'type': 'string'},
                    'show_on_top': {'type': 'boolean'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        404: {
            'description': 'Gallery item not found'
        }
    }
})
def get_or_update_gallery(gallery_id):
    gallery = Gallery.get(gallery_id)
    if not gallery:
        return jsonify({'error': 'Gallery item not found'}), 404

    if request.method == 'GET':
        return jsonify(gallery.to_dict()), 200

    if request.method == 'PUT':
        show_on_top = request.form.get('show_on_top', 'false').lower() == 'true'
        gallery.show_on_top = show_on_top

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                s3_url = upload_file_to_s3(file)
                gallery.picture = s3_url

        gallery.save()
        return jsonify(gallery.to_dict()), 200


@bp.route('/<int:gallery_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Galleries'],
    'responses': {
        200: {
            'description': 'Gallery item deleted successfully'
        },
        404: {
            'description': 'Gallery item not found'
        }
    }
})
def delete_gallery(gallery_id):
    gallery = Gallery.get(gallery_id)
    if not gallery:
        return jsonify({'error': 'Gallery item not found'}), 404
    gallery.delete()
    return jsonify({'message': 'Gallery item deleted'}), 200
