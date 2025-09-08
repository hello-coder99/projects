from flask import Flask
import redis

def create_app():
    app = Flask(__name__)
    
    # Configure Redis connection
    app.redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    
    # Ensure the unique_id counter exists
    try:
        app.redis.setnx('url_shortener:unique_id', 1000000)  # Start at 1 million for shorter codes
    except redis.ConnectionError:
        print("Error: Could not connect to Redis. Is it running?")
        raise
    
    # Register blueprints or routes
    from .routes import bp
    app.register_blueprint(bp)
    
    return app
