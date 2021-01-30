from flask import Flask

from recommendation import recommendation

HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__)
app.register_blueprint(recommendation, url_prefix='/recommendations')
