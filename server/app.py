import click
from flask import Flask, request
from flask_cors import CORS

from graph.bipartite_graph import load_indexes
from graph.content_graph import load_content_index
from server.content import content
from server.recommendation import recommendation
from server.status import status

app = Flask(__name__)
app.register_blueprint(recommendation, url_prefix='/recommendation')
app.register_blueprint(content, url_prefix='/content')
app.register_blueprint(status, url_prefix='/status')
CORS(app)


@click.command()
@click.option('--partition-method', type=click.Choice(['single_partition', 'modulo', 'murmur2', 'star-space']),
              default="single_partition",
              help='hash function used for partitioning (defaults single_partition).')
@click.option('--partition-number', default=0, help='number of partition')
@click.option('--port', default=5000, help='port number of server')
@click.option('--content-index/--no-content-index', default=False, help='Flag whether to load content index or not')
def cli(partition_method, partition_number, port, content_index):
    click.secho(f"Loading indexes for partition {partition_method} and partition(s) {partition_number}", fg='green')

    load_indexes(partition_method=partition_method, partition_number=partition_number)

    if content_index:
        load_content_index()

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
