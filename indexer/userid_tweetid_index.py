import os

import click
import pandas as pd
from pandas import DataFrame

from definitions import ROOT_DIR
from indexer.index_base import IndexBase
from partitioner.hash_functions.partition_base import PartitionBase


class UserIdTweetIdIndex(IndexBase):
    left_party = "user_id"
    right_party = "tweet_id"
    left_index_df: DataFrame
    right_index_df: DataFrame

    def __init__(self, partitioning_method: PartitionBase):
        super().__init__(partitioning_method)

    def create_indices(self, df: DataFrame()):
        click.echo(f"-------------{self.partitioning_method.name}---------------------")
        for num in range(self.partitioning_method.partition_count):
            df_partition = df[df["partition"] == num]
            df_partition = df_partition[[self.left_party, self.right_party]]
            df_partition = df_partition[df_partition[self.right_party].notna()]
            df_partition.drop_duplicates(keep='first', inplace=True, ignore_index=True)
            df_partition.dropna(inplace=True)
            click.echo(f"-------------Partition {num}---------------------")
            click.echo(f"Number of edges: {len(df_partition)}")

            partition_number_folder = os.path.join(ROOT_DIR, "data", self.partitioning_method.name,
                                                   f"partition_{num}")
            if not os.path.isdir(partition_number_folder):
                os.mkdir(partition_number_folder)

            for side in ["left", "right"]:
                index_side = self.left_party if side == "left" else self.right_party
                value_side = self.right_party if side == "left" else self.left_party
                index_df = df_partition.groupby(index_side)[value_side].apply(list).reset_index(name="adjacency_list")
                index_df.set_index(index_side, inplace=True)
                click.echo(f"{side} index ready. Len: {len(index_df)}")

                save_path = os.path.join(partition_number_folder, f'{side}_index.gzip')

                index_df.to_parquet(save_path, compression='gzip')

                del index_df
        del df_partition

    def load_indices(self, partition_number: int):
        sides = ["left", "right"]
        partition_folder = f"partition_{partition_number}"
        for side in sides:
            index_file = f"{side}_index.gzip"
            index_csv = os.path.join(ROOT_DIR, "data", self.partitioning_method.name, partition_folder, index_file)
            side_index = pd.read_parquet(index_csv, engine='fastparquet')
            if side == "left":
                self.left_index_df = side_index
            else:
                self.right_index_df = side_index
            click.echo(f"finish loading the {side} index")
