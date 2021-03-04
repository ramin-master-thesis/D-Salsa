import ast
import os

import click
import pandas as pd

from graph import current_file

DATA_FOLDER = '../data'
CONTENT = "content"
CONTENT_INDEX = pd.DataFrame()


def load_content_index():
    global CONTENT_INDEX
    path_to_index_file = f"{DATA_FOLDER}/content_index_new.tsv"
    index_csv = os.path.join(current_file, path_to_index_file)
    side_index = pd.read_csv(index_csv, sep='\t', index_col=0)
    CONTENT_INDEX = side_index
    click.echo("Finish loading content index")


def __convert_content(content):
    return ast.literal_eval(content)[0]


def get_content_by_id(index: int):
    try:
        content = CONTENT_INDEX._get_value(index, CONTENT)
        return content
    except KeyError:
        return None
