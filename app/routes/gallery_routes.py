from flask import Blueprint, request, jsonify
from app.models import Gallery
from app.utils.s3_utils import upload_file_to_s3, get_presign_url_from_s3
from flasgger import swag_from
from datetime import datetime


bp = Blueprint('gallery_routes', __name__)

@bp.route('', methods=['POST'], strict_slashes=False)
@swag_from({
    'tags': ['Galleries'],
    'parameters': [
        {
            'name': 'artist_id',
            'in': 'formData',
            'type': 'integer',
            'required': True,
            'description': 'ID of the artist'
        },
        {
            'name': 'show_on_top',
            'in': 'formData',
            'type': 'boolean',
            'description': 'Whether to show the gallery item on top'
        },
        {
            'name': 'picture',
            'in': 'formData',
            'type': 'file',
            'description': 'File to upload'
        }
    ],
    'responses': {
        201: {
            'description': 'Gallery item created successfully',
            'schema': {
                'type': 'object',
                'properties': {
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
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file.filename != '':
                s3_url = upload_file_to_s3(file, f"{Gallery.__tablename__}/{new_gallery.id}")
                new_gallery.picture = s3_url
                new_gallery.save()
        return jsonify(new_gallery.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400



@bp.route('', methods=['GET'], strict_slashes=False)
@swag_from({
    'tags': ['Galleries'],
    'parameters': [
        {
            'name': 'artist_id',
            'in': 'query',
            'type': 'integer',
            'description': 'ID of the artist to filter by'
        },
        {
            'name': 'show_on_top',
            'in': 'query',
            'type': 'boolean',
            'description': 'Filter by whether to show the gallery item on top'
        },
        {
            'name': 'created_at',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'description': 'Filter by creation date (ISO 8601 format)'
        },
        {
            'name': 'order_by',
            'in': 'query',
            'type': 'array',
            'items': {
                'type': 'string'
            },
            'collectionFormat': 'multi',
            'description': 'Fields to order by in the format field:direction'
        },
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Page number for pagination'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'description': 'Number of items per page for pagination'
        }
    ],
    'responses': {
        200: {
            'description': 'List of gallery items',
            'schema': {
                'type': 'object',
                'properties': {
                    'current_page': {'type': 'integer'},
                    'total_pages': {'type': 'integer'},
                    'datas': {
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
        }
    }
})
def get_galleries():
    filters = {}
    artist_id = request.args.get('artist_id')
    show_on_top = request.args.get('show_on_top')
    created_at = request.args.get('created_at')
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
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    galleries, total, total_records = Gallery.paginate(page, per_page, filters, order_by)
    total_pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'current_page': page,
        'total_pages': total_pages,
        'total_records': total_records,
        'datas': [gallery.to_dict() for gallery in galleries]
    }), 200



@bp.route('/<int:gallery_id>', methods=['GET'])
@swag_from({
    'tags': ['Galleries'],
    'parameters': [
        {
            'name': 'gallery_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the gallery item to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Gallery item retrieved successfully',
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
        404: {
            'description': 'Gallery item not found'
        }
    }
})
def get_gallery(gallery_id):
    gallery = Gallery.get(gallery_id)
    if not gallery:
        return jsonify({'error': 'Gallery item not found'}), 404
    return jsonify(gallery.to_dict()), 200


@bp.route('/<int:gallery_id>', methods=['PUT'])
@swag_from({
    'tags': ['Galleries'],
    'parameters': [
        {
            'name': 'gallery_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the gallery item to update'
        },
        {
            'name': 'show_on_top',
            'in': 'formData',
            'type': 'boolean',
            'description': 'Whether to show the gallery item on top'
        },
        {
            'name': 'picture',
            'in': 'formData',
            'type': 'file',
            'description': 'File to upload'
        }
    ],
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
def update_gallery(gallery_id):
    gallery = Gallery.get(gallery_id)
    if not gallery:
        return jsonify({'error': 'Gallery item not found'}), 404

    show_on_top = request.form.get('show_on_top', 'false').lower() == 'true'
    gallery.show_on_top = show_on_top

    if 'avatar' in request.files:
        file = request.files['avatar']
        if file.filename != '':
            s3_url = upload_file_to_s3(file, f"{Gallery.__tablename__}/{gallery.id}")
            gallery.picture = s3_url

    gallery.save()
    return jsonify(gallery.to_dict()), 200


@bp.route('/<int:gallery_id>/images', methods=['GET'])
@swag_from({
    'tags': ['Galleries'],
    'responses': {
        200: {
            'description': 'List of images for the gallery item',
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
        },
        404: {
            'description': 'Gallery item not found'
        }
    }
})
def get_gallery_images(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    if not gallery:
        return jsonify({'error': 'Gallery item not found'}), 404

    artist = gallery.artist()
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404

    artist_galleries = artist.galleries()

    return jsonify({
        'artist': artist.to_dict(),
        'pictures': [{'picture': get_presign_url_from_s3(g.picture, location=f"Galleries/{g.id}")} for g in artist_galleries if g.picture]
    }), 200



@bp.route('/<int:gallery_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Galleries'],
    'parameters': [
        {
            'name': 'gallery_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the gallery item to delete'
        }
    ],
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
