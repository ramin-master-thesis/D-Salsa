from flask import Blueprint, jsonify, current_app

from graph.bipartite_graph import BipartiteGraph
from graph.content_graph import ContentGraph

status = Blueprint('status', __name__)


@status.route('/', methods=['GET'])
def get_stats():
    indexer = current_app.config.get("userid_tweetid_indexer")
    bipartite_graph = BipartiteGraph(indexer)
    data = {'edges': bipartite_graph.get_edges_count(),
            'left-index-nodes': bipartite_graph.get_left_index_node_count(),
            'right-index-nodes': bipartite_graph.get_right_index_node_count()
            }
    return jsonify(data)


@status.route('/count/edges', methods=['GET'])
def get_count_edges():
    indexer = current_app.config.get("userid_tweetid_indexer")
    bipartite_graph = BipartiteGraph(indexer)
    return jsonify(bipartite_graph.get_edges_count())


@status.route('/count/left-index', methods=['GET'])
def get_count_left_index():
    indexer = current_app.config.get("userid_tweetid_indexer")
    bipartite_graph = BipartiteGraph(indexer)
    return jsonify(bipartite_graph.get_left_index_node_count())


@status.route('/count/right-index', methods=['GET'])
def get_count_right_index():
    indexer = current_app.config.get("userid_tweetid_indexer")
    bipartite_graph = BipartiteGraph(indexer)
    return jsonify(bipartite_graph.get_right_index_node_count())


@status.route('/degree/left-index/<int:node_id>', methods=['GET'])
def get_degree_left_index_node(node_id: int):
    indexer = current_app.config.get("userid_tweetid_indexer")
    bipartite_graph = BipartiteGraph(indexer)
    return jsonify(len(bipartite_graph.get_left_node_neighbors(node_id)))


@status.route('/degree/right-index/<int:node_id>', methods=['GET'])
def get_degree_right_index_node(node_id: int):
    indexer = current_app.config.get("userid_tweetid_indexer")
    bipartite_graph = BipartiteGraph(indexer)
    return jsonify(len(bipartite_graph.get_right_node_neighbors(node_id)))


@status.route('/degree/content/<int:node_id>', methods=['GET'])
def get_user_interactions(node_id: int):
    indexer = current_app.config.get("userid_tweetid_indexer")
    bipartite_graph = BipartiteGraph(indexer)
    neighbors = bipartite_graph.get_left_node_neighbors(node_id)

    indexer = current_app.config.get("tweetid_content_indexer")
    content_graph = ContentGraph(indexer)
    res = [content_graph.get_content_by_id(identifier) for identifier in neighbors]

    return jsonify(res)
