from flask import Blueprint, request, jsonify

from algorithm.salsa import Salsa

recommendation = Blueprint('recommendation', __name__)


@recommendation.route('/salsa/<int:user_id>')
def salsa(user_id: int):
    limit = request.args.get('limit', default=10, type=int)
    walks = request.args.get('walks', default=1000, type=int)
    walks_length = request.args.get('walk_length', default=100, type=int)
    reset_probability = request.args.get('reset_probability', default=0.1, type=float)

    recommendations = Salsa(user_id, limit, walks, walks_length, reset_probability).compute()
    return jsonify(recommendations)
