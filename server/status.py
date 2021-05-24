from flask import Blueprint, jsonify

from graph.bipartite_graph import get_left_index_node_count, get_right_index_node_count, get_edges_count, \
    get_left_node_neighbors, get_right_node_neighbors

status = Blueprint('status', __name__)


@status.route('/', methods=['GET'])
def get_stats():
    data = {'edges': get_edges_count(),
            'left-index-nodes': get_left_index_node_count(),
            'right-index-nodes': get_right_index_node_count()
            }
    return jsonify(data)


@status.route('/count/edges', methods=['GET'])
def get_count_edges():
    return jsonify(get_edges_count())


@status.route('/count/left-index', methods=['GET'])
def get_count_left_index():
    return jsonify(get_left_index_node_count())


@status.route('/count/right-index', methods=['GET'])
def get_count_right_index():
    return jsonify(get_right_index_node_count())


@status.route('/degree/left-index/<int:node_id>', methods=['GET'])
def get_degree_left_index_node(node_id: int):
    return jsonify(len(get_left_node_neighbors(node_id)))


@status.route('/degree/right-index/<int:node_id>', methods=['GET'])
def get_degree_right_index_node(node_id: int):
    return jsonify(len(get_right_node_neighbors(node_id)))
