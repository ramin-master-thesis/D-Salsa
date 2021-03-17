import ast
import os

import click
import numpy as np
import pandas as pd

from partitioner.hash_functions.modulo_partition import ModuloPartition
from partitioner.hash_functions.partition_base_class import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition


def partition_index(partition_method: PartitionBase):
    for index_side in ["left", "right"]:
        partition_method_folder = f"../data/{partition_method.name}"
        if not os.path.isdir(partition_method_folder):
            os.mkdir(partition_method_folder)
        click.echo(f"start to hash {index_side} index")
        df_index = pd.read_csv(f"../data/{index_side}_index.csv", index_col=0)
        indices = list(df_index.index.values)
        click.echo(f"start to hash {index_side} index")
        partitions = []
        for i, index in enumerate(indices):
            click.echo(f"hashing index number {index}, {i + 1}/{len(indices)}")
            partition = partition_method.calculate_partition(index)
            partitions.append(partition)

        df_index['partition_number'] = np.array(partitions)
        for i in range(partition_method.partition_count):
            partition_folder = f"{partition_method_folder}/partition_{i}"
            if not os.path.isdir(partition_folder):
                os.mkdir(partition_folder)
            df_index_partition = df_index[df_index['partition_number'] == i]
            df_index_partition["Adjacency List"] = df_index_partition["Adjacency List"].map(
                lambda x: partition_adjacency_list(partition_method, ast.literal_eval(x), i))
            df_index_partition.to_csv(
                f"{partition_folder}/{index_side}_index.csv",
                sep=',',
                encoding='utf-8'
            )
            del df_index_partition
        del df_index


def partition_adjacency_list(partition_method: PartitionBase, adjacency_list: list, partition_number: int):
    new_list = []
    for value in adjacency_list:
        partition = partition_method.calculate_partition(value)
        if partition == partition_number:
            new_list.append(value)
    return new_list


def partition_data(partition_method: PartitionBase):
    click.echo(
        f"Starting to partition data for partition method {partition_method.name} and num of partition(s) {partition_method.partition_count}")
    partition_method_folder = f"../data/{partition_method.name}"
    if not os.path.isdir(partition_method_folder):
        os.mkdir(partition_method_folder)
    df_index = pd.read_csv(f"../data/tweets-dump.tsv", sep="\t", usecols=[0, 1, 4], lineterminator='\n',
                           names=["user_id", "tweet_id", "content"], header=None, error_bad_lines=False)

    df_index["partition"] = df_index.apply(lambda x: partition_method.calculate_partition(x["tweet_id"]), axis=1)
    for num in range(partition_method.partition_count):
        partition_df = df_index[df_index["partition"] == num]

        partition_df.to_csv(
            f"{partition_method_folder}/partition_{num}/tweets.tsv",
            columns=["user_id", "tweet_id", "content"],
            sep='\t',
            encoding='utf-8',
            index=False
        )


if __name__ == "__main__":
    partition_data(partition_method=SinglePartition())
    partition_data(partition_method=ModuloPartition(2))
