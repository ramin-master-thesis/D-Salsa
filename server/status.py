from flask import Blueprint, jsonify

from graph.bipartite_graph import get_left_node_count, get_right_node_count, get_edges_count

status = Blueprint('status', __name__)


@status.route('/', methods=['GET'])
def get_stats():
    data = {'edges': get_edges_count(), 'left-nodes': get_left_node_count(), 'right-nodes': get_right_node_count()}
    return jsonify(data)


@status.route('/edges', methods=['GET'])
def get_count_edges():
    return jsonify(get_edges_count())


@status.route('/left-nodes', methods=['GET'])
def get_count_left_node():
    return jsonify(get_left_node_count())


@status.route('/right-nodes', methods=['GET'])
def get_count_right_node():
    return jsonify(get_right_node_count())
