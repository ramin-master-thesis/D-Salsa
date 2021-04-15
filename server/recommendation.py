from flask import Blueprint, request, jsonify

from algorithm.salsa import Salsa
from graph.content_graph import get_content_by_id

recommendation = Blueprint('recommendation', __name__)


@recommendation.route('/salsa/<int:user_id>', methods=['GET'])
def salsa(user_id: int):
    """
    Calls the SALSA algorithm for the given user_id.
    ---
    parameters:
      - name: user_id
        in: path
        type: int
        required: true
        description: The user identifier

      - name: with_content
        in: query
        type: string
        required: false
        default: true
        description: determines if the content or the result id should be returned

    responses:
      500:
        description: Error!
      200:
        description: A list of top K recommendations
    """
    limit, reset_probability, walks, walks_length = __init_parameters()
    with_content = False if request.args.get('content') == 'false' else True

    recommendations = Salsa(user_id, limit, walks, walks_length, reset_probability).compute()
    results = []
    for r in recommendations:
        results.append({"id": r[0], "hit": r[1]})

    if with_content:
        results = []
        for r in recommendations:
            results.append({"id": r[0], "content": get_content_by_id(r[0]), "hit": r[1]})
        return jsonify(results)

    return jsonify(results)


@recommendation.route('/salsa/tweet/<int:tweet_id>', methods=['GET'])
def salsa_for_tweets(tweet_id: int):
    with_content = False if request.args.get('content') == 'false' else True
    should_include_first = False if request.args.get('first') == 'false' else True
    limit, reset_probability, walks, walks_length = __init_parameters()

    recommendations = Salsa(tweet_id, limit, walks, walks_length, reset_probability).compute(for_user=False)

    if should_include_first:
        recommendations.insert(0, (tweet_id, 0))

    if with_content:
        res = []
        for r in recommendations:
            res.append({"id": r[0], "content": get_content_by_id(r[0]), "hit": r[1]})
        return jsonify(res)

    return jsonify(recommendations)


def __init_parameters():
    limit = request.args.get('limit', default=10, type=int)
    walks = request.args.get('walks', default=1000, type=int)
    walks_length = request.args.get('walk_length', default=100, type=int)
    reset_probability = request.args.get('reset_probability', default=0.1, type=float)
    return limit, reset_probability, walks, walks_length
