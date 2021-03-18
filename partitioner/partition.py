import os

import click
import pandas as pd

from partitioner import current_directory
from partitioner.hash_functions.modulo_partition import ModuloPartition
from partitioner.hash_functions.murmur2_partition import Murmur2Partition
from partitioner.hash_functions.partition_base_class import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition

DATA_FOLDER = f"{current_directory}/../data"


def partition_data(partition_method: PartitionBase):
    click.echo(
        f"Starting to partition data for partition method {partition_method.name} and num of partition(s) {partition_method.partition_count}")
    partition_method_folder = f"{DATA_FOLDER}/{partition_method.name}"
    if not os.path.isdir(partition_method_folder):
        os.mkdir(partition_method_folder)
    df_index = pd.read_csv(f"{DATA_FOLDER}/tweets-dump.tsv", sep="\t", usecols=[0, 1, 4],
                           lineterminator='\n',
                           names=["user_id", "tweet_id", "content"], header=None, error_bad_lines=False)

    df_index["partition"] = df_index.apply(lambda x: partition_method.calculate_partition(x["tweet_id"]), axis=1)
    for num in range(partition_method.partition_count):
        partition_df = df_index[df_index["partition"] == num]
        partition_number_folder = os.path.join(partition_method_folder, f"partition_{num}")
        if not os.path.isdir(partition_number_folder):
            os.mkdir(partition_number_folder)

        partition_df.to_csv(
            os.path.join(partition_number_folder, "tweets.tsv"),
            columns=["user_id", "tweet_id", "content"],
            sep='\t',
            encoding='utf-8',
            index=False
        )


@click.group()
def cli():
    pass


@cli.command()
def single():
    partition_data(partition_method=SinglePartition())


@cli.command()
@click.option('--partition-number', default=2, help='number of partitions (default 2)')
def modulo(partition_number):
    partition_data(partition_method=ModuloPartition(partition_number))


@cli.command()
@click.option('--partition-number', default=2, help='number of partitions (default 2)')
def murmur2(partition_number):
    partition_data(partition_method=Murmur2Partition(partition_number))


if __name__ == "__main__":
    cli()
