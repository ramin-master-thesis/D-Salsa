from flask import Blueprint
import pandas as pd

recommendation = Blueprint('recommendation', __name__)


@recommendation.route('/salsa')
def salsa():
    return "hello salsa"


def read_data():
    data = pd.read_csv("/data/tweet")
