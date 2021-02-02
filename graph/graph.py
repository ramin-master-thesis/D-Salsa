import os

import click
import pandas as pd

current_file = os.path.abspath(os.path.dirname(__file__))

DATA_PATH = '../data/tweets-dedupe.csv'

LEFT_PARTY = "UserID"
RIGHT_PARTY = "TweetID"
ADJACENCY_LIST = "Adjacency List"
LEFT_INDEX = pd.DataFrame()
RIGHT_INDEX = pd.DataFrame()


def create_indexes():
    global LEFT_INDEX
    global RIGHT_INDEX
    csv_filename = os.path.join(current_file, DATA_PATH)
    df = pd.read_csv(csv_filename,
                     names=[LEFT_PARTY, RIGHT_PARTY, "Interaction"])

    LEFT_INDEX = df.groupby(LEFT_PARTY)[RIGHT_PARTY].apply(list).reset_index(name=ADJACENCY_LIST)
    LEFT_INDEX.set_index(LEFT_PARTY, inplace=True)
    click.echo("left index ready")

    RIGHT_INDEX = df.groupby(RIGHT_PARTY)[LEFT_PARTY].apply(list).reset_index(name=ADJACENCY_LIST)
    RIGHT_INDEX.set_index(RIGHT_PARTY, inplace=True)
    click.echo("right index ready")

    del df


def get_left_node_neighbors(node: int) -> list:
    try:
        values = LEFT_INDEX._get_value(node, ADJACENCY_LIST)
    except KeyError:
        return []
    return values


def get_right_node_neighbors(node) -> list:
    try:
        values = RIGHT_INDEX._get_value(node, ADJACENCY_LIST)
    except KeyError:
        return []
    return values
