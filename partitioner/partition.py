import os

import click
import pandas as pd

from partitioner.hash_functions.partition_base import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition
from partitioner.hash_functions.star_space_partition import StarSpacePartition


def partition_data(partition_method: PartitionBase, file_path: str):
    click.echo(
        f"Starting to partition data for partition method {partition_method.name} and num of partition(s) "
        f"{partition_method.partition_count}")

    is_tsv = True if os.path.splitext(file_path)[1] == ".tsv" else False

    if is_tsv:
        df_index = pd.read_csv(file_path, sep="\t", usecols=[0, 1, 4],
                               lineterminator='\n',
                               names=["user_id", "tweet_id", "content"], header=None)

    else:
        df_index = pd.read_parquet(file_path, columns=['user_id', 'tweet_id', 'content'])

    df_index.dropna(inplace=True)
    df_index['user_id'] = df_index['user_id'].astype('int')
    df_index['tweet_id'] = df_index['tweet_id'].astype('int')

    df_index.drop_duplicates(keep="first", inplace=True)

    if isinstance(partition_method, StarSpacePartition):
        df_index["partition"] = df_index.apply(lambda x: partition_method.calculate_partition(x["content"]), axis=1)
    elif isinstance(partition_method, SinglePartition):
        df_index["partition"] = 0
        return df_index
    else:
        df_index["partition"] = df_index.apply(lambda x: partition_method.calculate_partition(x["tweet_id"]), axis=1)

    return df_index
