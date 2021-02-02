from flask import Flask

from graph.graph import create_indexes
from server.recommendation import recommendation

app = Flask(__name__)
app.register_blueprint(recommendation, url_prefix='/recommendations')

create_indexes()
