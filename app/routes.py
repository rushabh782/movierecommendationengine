# routes.py

from flask import Blueprint, request, jsonify
from app.recommendation import get_song_recommendations  # assuming recommendation logic is in this file

recommendation_bp = Blueprint('recommendations', __name__)

# Route for song-based recommendations (GET request)
@recommendation_bp.route('/song', methods=['GET'])
def recommend_song():
    song_name = request.args.get('song_name', type=str)
    if not song_name:
        return jsonify({'error': 'Song name is required.'}), 400
    recommendations = get_song_recommendations(song_name)
    return jsonify(recommendations)

# Route for user-based recommendations (GET request)
@recommendation_bp.route('/user', methods=['GET'])
def recommend_user():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'User ID is required.'}), 400
    recommendations = get_user_recommendations(user_id)
    return jsonify(recommendations)
