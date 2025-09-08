from flask import Blueprint, request, jsonify, redirect
from app import create_app

# Create a Blueprint
bp = Blueprint('main', __name__)

@bp.route('/shorten', methods=['POST'])
def shorten_url():
    # We need to get the Redis connection from the app
    app = create_app()
    redis_conn = app.redis
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON data is required'}), 400
        
    long_url = data.get('url')
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    # Generate a unique short code
    short_code = generate_short_code(redis_conn)

    # Store the mapping in Redis: key=short_code, value=long_url
    redis_conn.set(f'url_shortener:{short_code}', long_url)

    # Return the shortened URL to the user
    short_url = f"{request.host_url}{short_code}"
    return jsonify({'short_url': short_url, 'short_code': short_code}), 201

@bp.route('/<short_code>')
def redirect_to_long_url(short_code):
    app = create_app()
    redis_conn = app.redis
    
    # Look up the long URL in Redis using the short_code
    long_url = redis_conn.get(f'url_shortener:{short_code}')

    if long_url is None:
        return jsonify({'error': 'Short code not found'}), 404

    # Perform the HTTP redirect
    return redirect(long_url, code=302) # 302 Found (temporary redirect)

@bp.route('/')
def index():
    return jsonify({
        'message': 'URL Shortener API',
        'endpoints': {
            'shorten': 'POST /shorten',
            'redirect': 'GET /<short_code>'
        }
    })

# Import here to avoid circular imports
from .utils import generate_short_code
