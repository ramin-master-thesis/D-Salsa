import os

import click
import pandas as pd
from pandas import DataFrame

from graph.bipartite_graph import current_directory
from partitioner.hash_functions.partition_base_class import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition

DATA_FOLDER = '../data'
FILE = 'tweets.gzip'
LEFT_PARTY = "user_id"
RIGHT_PARTY = "tweet_id"
CONTENT = "content"
ADJACENCY_LIST = "adjacency_list"


def __read_data(use_cols: list, partition_number, partition_method_name: str) -> DataFrame():
    partition_number_folder = f"partition_{partition_number}"
    csv_filename = os.path.join(current_directory, DATA_FOLDER, partition_method_name, partition_number_folder, FILE)

    df = pd.read_parquet(csv_filename, columns=use_cols)
    return df


def create_indices(df: DataFrame() = None, partition_method: PartitionBase = SinglePartition()):
    click.echo(f"-------------{partition_method.name}---------------------")
    for num in range(partition_method.partition_count):
        if df is None:
            df_partition = __read_data([LEFT_PARTY, RIGHT_PARTY], num, partition_method.name)
        else:
            df_partition = df[df["partition"] == num]
        df_partition = df_partition[[LEFT_PARTY, RIGHT_PARTY]]
        df_partition = df_partition[df_partition[RIGHT_PARTY].notna()]
        df_partition.drop_duplicates(keep='first', inplace=True, ignore_index=True)
        df_partition.dropna(inplace=True)
        click.echo(f"-------------Partition {num}---------------------")
        click.echo(f"Number of edges: {len(df_partition)}")

        partition_number_folder = os.path.join(current_directory, DATA_FOLDER, partition_method.name,
                                               f"partition_{num}")
        if not os.path.isdir(partition_number_folder):
            os.mkdir(partition_number_folder)

        for side in ["left", "right"]:
            index_side = LEFT_PARTY if side == "left" else RIGHT_PARTY
            value_side = RIGHT_PARTY if side == "left" else LEFT_PARTY
            index_df = df_partition.groupby(index_side)[value_side].apply(list).reset_index(name=ADJACENCY_LIST)
            index_df.set_index(index_side, inplace=True)
            click.echo(f"{side} index ready. Len: {len(index_df)}")

            save_path = os.path.join(partition_number_folder, f'{side}_index.gzip')

            index_df.to_parquet(save_path, compression='gzip')

            del index_df
    del df_partition


def create_content_index(df: DataFrame() = None, partition_method: PartitionBase = SinglePartition()):
    for num in range(partition_method.partition_count):
        if df is None:
            df_partition = __read_data([RIGHT_PARTY, CONTENT], num, partition_method.name)
        else:
            df_partition = df[df["partition"] == num]
        df_partition = df_partition[[RIGHT_PARTY, CONTENT]]
        df_partition = df_partition[df_partition[RIGHT_PARTY].notna()]
        df_partition.drop_duplicates([RIGHT_PARTY], keep='first', inplace=True, ignore_index=True)
        df_partition.dropna(inplace=True)
        df_partition.set_index(RIGHT_PARTY, inplace=True)
        click.echo(f"content index ready")
        save_path = os.path.join(current_directory, DATA_FOLDER, partition_method.name, f"partition_{num}",
                                 "content_index.gzip")

        df_partition.to_parquet(save_path, compression='gzip')
