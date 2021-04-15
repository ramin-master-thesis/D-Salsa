import os

import click
import pandas as pd

from partitioner import current_directory
from partitioner.hash_functions.modulo_partition import ModuloPartition
from partitioner.hash_functions.murmur2_partition import Murmur2Partition
from partitioner.hash_functions.partition_base_class import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition
from partitioner.hash_functions.star_space_partition import StarSpacePartition
from partitioner.index import create_indices, create_content_index

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


@click.group()
@click.option('-f', '--path-to-file', default=f"{data_folder_path}/{data}")
def cli(path_to_file):
    global data_folder_path
    global data
    data_folder_path = os.path.dirname(path_to_file)
    data = os.path.basename(path_to_file)


@cli.command()
def single():
    partition_method = SinglePartition()
    df_partition = partition_data(partition_method=partition_method)
    create_indices(df_partition, partition_method=partition_method)
    create_content_index(df_partition, partition_method=partition_method)


@cli.command()
@click.option('-n', '--partition-number', default=2, help='number of partitions (default 2)')
def modulo(partition_number):
    partition_method = ModuloPartition(partition_number)
    df_partition = partition_data(partition_method=partition_method)
    create_indices(df=df_partition, partition_method=partition_method)
    create_content_index(df=df_partition, partition_method=partition_method)


@cli.command()
@click.option('-n', '--partition-number', default=2, help='number of partitions (default 2)')
def murmur2(partition_number):
    partition_method = Murmur2Partition(partition_number)
    df_partition = partition_data(partition_method=partition_method)
    create_indices(df=df_partition, partition_method=partition_method)
    create_content_index(df=df_partition, partition_method=partition_method)


@cli.command()
@click.option('-n', '--partition-number', default=2, help='number of partitions (default 2)')
@click.option('-m', '--model-folder', help="folder name of the model parameter")
# Example: -p "initRandSd_0.01_adagrad_True_lr_0.01_margin_0.05_epoch_20_dim_100_negSerachLimit_100_dropoutRHS_0.5_minCount_5_normalizeText_True"
def star_space(partition_number, model_folder):
    partition_method = StarSpacePartition(partition_number, model_folder)
    df_partition = partition_data(partition_method=partition_method)
    create_indices(df=df_partition, partition_method=partition_method)
    create_content_index(df=df_partition, partition_method=partition_method)


if __name__ == "__main__":
    # Example: cli(["-f", "/home/ramin/Developer/master-thesis/salsa/data/StarSpace_data/tweets-dump-train.tsv", "single"])
    cli()
