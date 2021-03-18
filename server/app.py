import click
from flask import Flask, request

from graph.content_graph import load_content_index
from graph.bipartite_graph import load_indexes
from server.content import content
from server.recommendation import recommendation

app = Flask(__name__)
app.register_blueprint(recommendation, url_prefix='/recommendation')
app.register_blueprint(content, url_prefix='/content')


@click.command()
@click.option('--partition-method', type=click.Choice(['single_partition', 'modulo', 'murmur2']),
              default="single_partition",
              help='hash function used for partitioning (defaults single_partition).')
@click.option('--partition-number', default=0, help='number of partition')
@click.option('--port', default=5001, help='port number of server')
def cli(partition_method, partition_number, port):
    click.secho(f"Loading indexes for partition {partition_method} and partition(s) {partition_number}", fg='green')

    load_indexes(partition_method=partition_method, partition_number=partition_number)

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


if __name__ == "__main__":
    cli()
