from flask import Blueprint, jsonify, request, current_app

from graph.content_graph import ContentGraph

content = Blueprint('content', __name__)


@content.route('/<identifier>', methods=['GET'])
def get_content(identifier: int):
    indexer = current_app.config.get("tweetid_content_indexer")
    return jsonify(ContentGraph(indexer).get_content_by_id(identifier))


@content.route('/bulk', methods=['POST'])
def bulk_get():
    indexer = current_app.config.get("tweetid_content_indexer")
    id_list = request.json

    res = []

    for identifier in id_list:
        res.append(ContentGraph(indexer).get_content_by_id(identifier))

    return jsonify(res)
