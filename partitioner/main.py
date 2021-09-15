import click

from definitions import ROOT_DIR
from indexer.tweetid_content_index import TweetIdContentIndex
from indexer.userid_tweetid_index import UserIdTweetIdIndex
from partitioner.hash_functions.modulo_partition import ModuloPartition
from partitioner.hash_functions.murmur2_partition import Murmur2Partition
from partitioner.hash_functions.partition_base import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition
from partitioner.hash_functions.star_space_partition import StarSpacePartition
from partitioner.partition import partition_data

data_folder_path = f"{ROOT_DIR}/data"
data = "tweets-dump.tsv"


@click.group()
@click.option('-f', '--path-to-file', default=f"{data_folder_path}/{data}",
              help="path to the tsv data file (default is /data/tweets-dump.tsv)")
@click.option('--content-index/--no-content-index', default=False,
              help="A flag dedicating if the content index should be generated or not (default is false)")
@click.pass_context
def cli(ctx, path_to_file, content_index):
    ctx.ensure_object(dict)

    ctx.obj['should_create_content'] = content_index
    ctx.obj['path_to_file'] = path_to_file


@cli.command()
@click.pass_context
def single(ctx):
    partition_method = SinglePartition()
    __creat_indices(partition_method, ctx.obj['should_create_content'], ctx.obj['path_to_file'])


@cli.command()
@click.option('-n', '--partition-number', default=2, help='total number of partitions (default 2)')
@click.pass_context
def modulo(ctx, partition_number):
    partition_method = ModuloPartition(partition_number)
    __creat_indices(partition_method, ctx.obj['should_create_content'], ctx.obj['path_to_file'])


@cli.command()
@click.option('-n', '--partition-number', default=2, help='total number of partitions (default 2)')
@click.pass_context
def murmur2(ctx, partition_number):
    partition_method = Murmur2Partition(partition_number)
    __creat_indices(partition_method, ctx.obj['should_create_content'], ctx.obj['path_to_file'])


@cli.command()
@click.option('-n', '--partition-number', default=2, help='total number of partitions (default 2)')
@click.option('-m', '--model-folder', required=True, help="folder name of the model parameter")
@click.pass_context
# Example: -m "lr_0.01_dim_300_dropoutRHS_0.8_normalizeText_False"
def star_space(ctx, partition_number, model_folder):
    partition_method = StarSpacePartition(partition_number, model_folder)
    __creat_indices(partition_method, ctx.obj['should_create_content'], ctx.obj['path_to_file'])


def __creat_indices(partition_method: PartitionBase, should_create_content_index: bool, file_path: str):
    df_partition = partition_data(partition_method=partition_method, file_path=file_path)
    UserIdTweetIdIndex(partitioning_method=partition_method).create_indices(df_partition)
    if should_create_content_index:
        TweetIdContentIndex(partitioning_method=partition_method).create_indices(df_partition)


if __name__ == "__main__":
    # Example: cli(["-f", "/home/ramin/Developer/master-thesis/salsa/data/tweets.tsv", "single"])
    cli()
