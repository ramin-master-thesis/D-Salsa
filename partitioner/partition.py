import os

import click
import pandas as pd

from partitioner import current_directory
from partitioner.hash_functions.partition_base_class import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition
from partitioner.hash_functions.star_space_partition import StarSpacePartition

data_folder_path = f"{current_directory}/../data"
data = "tweets-dump.tsv"


def partition_data(partition_method: PartitionBase):
    click.echo(
        f"Starting to partition data for partition method {partition_method.name} and num of partition(s) {partition_method.partition_count}")

    file_location = os.path.join(data_folder_path, data)

    df_index = pd.read_csv(file_location, sep="\t", usecols=[0, 1, 4],
                           lineterminator='\n',
                           names=["user_id", "tweet_id", "content"], header=None)

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

    # TODO: make it optional
    __save_partition_to_file(df_index, partition_method)

    return df_index


def __save_partition_to_file(df_index, partition_method):
    partition_method_folder = f"{data_folder_path}/{partition_method.name}"

    if not os.path.isdir(partition_method_folder):
        os.mkdir(partition_method_folder)

    for num in range(partition_method.partition_count):
        partition_df = df_index[df_index["partition"] == num]
        partition_number_folder = os.path.join(partition_method_folder, f"partition_{num}")
        if not os.path.isdir(partition_number_folder):
            os.mkdir(partition_number_folder)

        save_path = os.path.join(partition_number_folder, "tweets.gzip")
        partition_df.to_parquet(save_path, compression='gzip')
