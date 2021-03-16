import os

import click
import pandas as pd
from pandas import DataFrame

from graph.bipartite_graph import current_directory

DATA_FOLDER = '../data'
FILE = 'tweets.tsv'
LEFT_PARTY = "user_id"
RIGHT_PARTY = "tweet_id"
CONTENT = "content"
ADJACENCY_LIST = "adjacency_list"


def __read_data(usecols: list, dtype: dict) -> DataFrame():
    sep = ',' if 'csv' in FILE else '\t'
    csv_filename = os.path.join(current_directory, DATA_FOLDER, FILE)
    df = pd.read_csv(csv_filename, sep=sep, usecols=usecols, header=0, names=list(dtype.keys()),
                     dtype=dtype)
    return df


def create_indices():
    df = __read_data([0, 1], {LEFT_PARTY: int, RIGHT_PARTY: int})
    df = df[df[RIGHT_PARTY].notna()]
    df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    df.dropna(inplace=True)
    print("len indices: ", len(df))
    for side in ["left", "right"]:
        index_side = LEFT_PARTY if side == "left" else RIGHT_PARTY
        value_side = RIGHT_PARTY if side == "left" else LEFT_PARTY
        index_df = df.groupby(index_side)[value_side].apply(list).reset_index(name=ADJACENCY_LIST)
        index_df.set_index(index_side, inplace=True)
        click.echo(f"{side} index ready")
        index_df.to_csv(
            f"{DATA_FOLDER}/{side}_index_new.csv",
            sep=',',
            encoding='utf-8'
        )


def create_content_index():
    df = __read_data(usecols=[1, 4], dtype={RIGHT_PARTY: int, CONTENT: str})
    df = df[df[RIGHT_PARTY].notna()]
    df.drop_duplicates([RIGHT_PARTY], keep='first', inplace=True, ignore_index=True)
    df.dropna(inplace=True)
    print("len content indices: ", len(df))
    df.set_index(RIGHT_PARTY, inplace=True)
    click.echo(f"content index ready")
    df.to_csv(
        f"{DATA_FOLDER}/content_index_new.tsv",
        sep='\t',
        encoding='utf-8'
    )


if __name__ == "__main__":
    create_indices()
    create_content_index()
