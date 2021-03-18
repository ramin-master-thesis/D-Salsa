import glob
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


def __get_partitions_count(partition_method):
    path = os.path.join(current_directory, DATA_FOLDER, partition_method)
    return len(glob.glob(f"{path}/partition_*"))


def __read_data(use_cols: list, dtype: dict, partition_number, partition_method) -> DataFrame():
    sep = ',' if 'csv' in FILE else '\t'
    partition_method_folder = partition_method
    partition_folder = f"partition_{partition_number}"
    csv_filename = os.path.join(current_directory, DATA_FOLDER, partition_method_folder, partition_folder, FILE)
    df = pd.read_csv(csv_filename, sep=sep, usecols=use_cols, lineterminator='\n', header=0, names=list(dtype.keys()),
                     dtype=dtype)
    return df


def create_indices(partition_method="single_partition"):
    num_partitions = __get_partitions_count(partition_method)

    click.echo(f"-------------{partition_method}---------------------")
    for num in range(num_partitions):
        df = __read_data([0, 1], {LEFT_PARTY: int, RIGHT_PARTY: int}, partition_number=num,
                         partition_method=partition_method)
        df = df[df[RIGHT_PARTY].notna()]
        df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
        df.dropna(inplace=True)
        click.echo(f"-------------Partition {num}---------------------")
        click.echo(f"len indices: {len(df)}")
        for side in ["left", "right"]:
            index_side = LEFT_PARTY if side == "left" else RIGHT_PARTY
            value_side = RIGHT_PARTY if side == "left" else LEFT_PARTY
            index_df = df.groupby(index_side)[value_side].apply(list).reset_index(name=ADJACENCY_LIST)
            index_df.set_index(index_side, inplace=True)
            click.echo(f"{side} index ready. Len: {len(index_df)}")
            save_path = os.path.join(current_directory, DATA_FOLDER, partition_method, f"partition_{num}",
                                     f"{side}_index.csv")
            index_df.to_csv(
                save_path,
                sep=',',
                encoding='utf-8'
            )
            del index_df
    del df


def create_content_index(partition_method="single_partition"):
    num_partitions = __get_partitions_count(partition_method)

    for num in range(num_partitions):
        df = __read_data(use_cols=[1, 2], dtype={RIGHT_PARTY: int, CONTENT: str}, partition_number=num,
                         partition_method=partition_method)
        df = df[df[RIGHT_PARTY].notna()]
        df.drop_duplicates([RIGHT_PARTY], keep='first', inplace=True, ignore_index=True)
        df.dropna(inplace=True)
        print("len content indices: ", len(df))
        df.set_index(RIGHT_PARTY, inplace=True)
        click.echo(f"content index ready")
        save_path = os.path.join(current_directory, DATA_FOLDER, partition_method, f"partition_{num}",
                                 "content_index.tsv")
        df.to_csv(
            save_path,
            sep='\t',
            encoding='utf-8'
        )


@click.group()
def cli():
    pass


@cli.command()
def single():
    create_indices(partition_method="single_partition")
    create_content_index(partition_method="single_partition")


@cli.command()
def modulo():
    create_indices(partition_method="modulo")
    create_content_index(partition_method="modulo")


@cli.command()
def murmur2():
    create_indices(partition_method="murmur2")
    create_content_index(partition_method="murmur2")


if __name__ == "__main__":
    cli()
