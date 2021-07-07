import os

import click
import pandas as pd
from pandas import DataFrame

from definitions import ROOT_DIR
from indexer.index_base import IndexBase
from partitioner.hash_functions.partition_base import PartitionBase


class TweetIdContentIndex(IndexBase):
    left_party = "tweet_id"
    right_party = "content"
    content_index_df: DataFrame

    def __init__(self, partitioning_method: PartitionBase):
        super().__init__(partitioning_method)

    def create_indices(self, df: DataFrame()):
        for num in range(self.partitioning_method.partition_count):
            df_partition = df[df["partition"] == num]
            df_partition = df_partition[[self.left_party, self.right_party]]
            df_partition = df_partition[df_partition[self.left_party].notna()]
            df_partition.drop_duplicates([self.left_party], keep='first', inplace=True, ignore_index=True)
            df_partition.dropna(inplace=True)
            df_partition.set_index(self.left_party, inplace=True)
            click.echo(f"content index ready")
            save_path = os.path.join(ROOT_DIR, "data", self.partitioning_method.name, f"partition_{num}",
                                     "content_index.gzip")

            df_partition.to_parquet(save_path, compression='gzip')

    def load_indices(self, partition_number: int):
        partition_folder = f"partition_{partition_number}"
        content_index_file = "content_index.gzip"
        index_csv = os.path.join(ROOT_DIR, 'data', self.partitioning_method.name, partition_folder, content_index_file)

        self.content_index_df = pd.read_parquet(index_csv, engine='fastparquet')
        click.echo("Finish loading content index")
