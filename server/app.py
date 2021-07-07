import importlib
import inspect
import sys

import click
from flask import Flask, request
from flask_cors import CORS

from indexer.tweetid_content_index import TweetIdContentIndex
from indexer.userid_tweetid_index import UserIdTweetIdIndex
from server.content import content
from server.recommendation import recommendation
from server.status import status

app = Flask(__name__)
app.register_blueprint(recommendation, url_prefix='/recommendation')
app.register_blueprint(content, url_prefix='/content')
app.register_blueprint(status, url_prefix='/status')
CORS(app)


@click.command()
@click.option('--partition-method', type=click.Choice(['single', 'modulo', 'murmur2', 'star_space']),
              default="single",
              help='hash function used for partitioning (defaults single_partition).')
@click.option('--partition-number', default=0, help='number of partition')
@click.option('--port', default=5000, help='port number of server')
@click.option('--content-index/--no-content-index', default=False, help='Flag whether to load content index or not')
def cli(partition_method, partition_number, port, content_index):
    click.secho(f"Loading indexes for partition {partition_method} and partition(s) {partition_number}", fg='green')

    m = importlib.import_module(f"partitioner.hash_functions.{partition_method}_partition")
    partition_method_obj = inspect.getmembers(m, inspect.isclass)[1][1]

    userid_tweetid_indexer = UserIdTweetIdIndex(partitioning_method=partition_method_obj)
    userid_tweetid_indexer.load_indices(partition_number)
    app.config["userid_tweetid_indexer"] = userid_tweetid_indexer

    if content_index:
        tweetid_content_indexer = TweetIdContentIndex(partitioning_method=partition_method_obj)
        tweetid_content_indexer.load_indices(partition_number)
        app.config["tweetid_content_indexer"] = tweetid_content_indexer

    app.run(host="0.0.0.0", port=port, debug=False)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/healthy', methods=['GET'])
def health_check():
    return 'server is healthy'


if __name__ == "__main__":
    cli()
