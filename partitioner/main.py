import click
import os

from partitioner import current_directory
from partitioner.hash_functions.modulo_partition import ModuloPartition
from partitioner.hash_functions.murmur2_partition import Murmur2Partition
from partitioner.hash_functions.partition_base_class import PartitionBase
from partitioner.hash_functions.single_partition import SinglePartition
from partitioner.hash_functions.star_space_partition import StarSpacePartition
from partitioner.index import create_indices, create_content_index
from partitioner.partition import partition_data

data_folder_path = f"{current_directory}/../data"
data = "tweets-dump.tsv"


@click.group()
@click.option('-f', '--path-to-file', default=f"{data_folder_path}/{data}",
              help="path to the tsv data file (default is /data/tweets-dump.tsv)")
@click.option('--content-index/--no-content-index', default=False,
              help="A flag dedicating if the content index should be generated or not (default is false)")
@click.pass_context
def cli(ctx, path_to_file, content_index):
    global data_folder_path
    global data
    data_folder_path = os.path.dirname(path_to_file)
    data = os.path.basename(path_to_file)
    ctx.ensure_object(dict)

    ctx.obj['should_create_content'] = content_index


@cli.command()
@click.pass_context
def single(ctx):
    partition_method = SinglePartition()
    __creat_indices(partition_method, ctx.obj['should_create_content'])


@cli.command()
@click.option('-n', '--partition-number', default=2, help='number of partitions (default 2)')
@click.pass_context
def modulo(ctx, partition_number):
    partition_method = ModuloPartition(partition_number)
    __creat_indices(partition_method, ctx.obj['should_create_content'])


@cli.command()
@click.option('-n', '--partition-number', default=2, help='number of partitions (default 2)')
@click.pass_context
def murmur2(ctx, partition_number):
    partition_method = Murmur2Partition(partition_number)
    __creat_indices(partition_method, ctx.obj['should_create_content'])


@cli.command()
@click.option('-n', '--partition-number', default=2, help='number of partitions (default 2)')
@click.option('-m', '--model-folder', required=True, help="folder name of the model parameter")
@click.pass_context
# Example: -m "lr_0.01_dim_100_dropoutRHS_0.5_normalizeText_True"
def star_space(ctx, partition_number, model_folder):
    partition_method = StarSpacePartition(partition_number, model_folder)
    __creat_indices(partition_method, ctx.obj['should_create_content'])


def __creat_indices(partition_method: PartitionBase, should_create_content_index: bool):
    df_partition = partition_data(partition_method=partition_method)
    create_indices(df=df_partition, partition_method=partition_method)
    if should_create_content_index:
        create_content_index(df=df_partition, partition_method=partition_method)


if __name__ == "__main__":
    # Example: cli(["-f", "/home/ramin/Developer/master-thesis/salsa/data/tweets.tsv", "single"])
    cli()
