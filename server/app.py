import click
from flask import Flask

from graph.content_graph import load_content_index
from graph.bipartite_graph import load_indexes
from server.content import content
from server.recommendation import recommendation

app = Flask(__name__)
app.register_blueprint(recommendation, url_prefix='/recommendation')
app.register_blueprint(content, url_prefix='/content')


@click.command()
@click.option('--hash-function', default="", help='hash function used for partitioning (defaults nothing).')
@click.option('--partition-number', default="", help='number of partition')
@click.option('--port', default=5001, help='port number of server')
def cli(hash_function, partition_number, port):
    click.secho(f"Loading indexes for hash function {hash_function} and partition {partition_number}", fg='green')

    load_indexes(hash_function=hash_function, partition_number=partition_number)

    load_content_index()

    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    cli()
