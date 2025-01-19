from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import recommendation_bp
    app.register_blueprint(recommendation_bp, url_prefix='/recommendations')

    return app
