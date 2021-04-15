import os

import click
import pandas as pd

from graph import current_directory

DATA_FOLDER = '../data'
CONTENT = "content"
CONTENT_INDEX = pd.DataFrame()


def load_content_index(partition_method: str = "single_partition", partition_number: int = 0):
    global CONTENT_INDEX
    partition_folder = f"partition_{partition_number}"
    content_index_file = "content_index.gzip"
    index_csv = os.path.join(current_directory, DATA_FOLDER, partition_method, partition_folder, content_index_file)

    side_index = pd.read_parquet(index_csv, engine='fastparquet')
    CONTENT_INDEX = side_index
    click.echo("Finish loading content index")


def get_content_by_id(index: int):
    try:
        content = CONTENT_INDEX._get_value(index, CONTENT)
        return content
    except KeyError:
        return None
