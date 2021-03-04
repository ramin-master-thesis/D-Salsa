from flask import Blueprint, jsonify, request

from graph.content_graph import get_content_by_id

content = Blueprint('content', __name__)


@content.route('/<identifier>', methods=['GET'])
def get_content(identifier: int):
    return jsonify(get_content_by_id(identifier))


@content.route('/bulk', methods=['POST'])
def bulk_get():
    id_list = request.json

    res = []

    for identifier in id_list:
        res.append(get_content_by_id(identifier))

    return jsonify(res)
