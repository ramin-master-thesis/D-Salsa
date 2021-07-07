import click
import pandas as pd
import requests
from pandas import DataFrame

from definitions import ROOT_DIR


def __get_recommendations_content(identifier: int) -> list:
    # api-endpoint
    url = f"http://localhost:5001/recommendation/salsa/tweet/{identifier}"

    # defining a params dict for the parameters to be sent to the API
    params = {'first': True, 'content': True}

    # sending get request and saving the response as response object
    r = requests.get(url=url, params=params)

    # extracting data in json format
    data = r.json()

    return [d.get("content", "None") for d in data]


def __get_identifiers():
    identifiers = pd.read_parquet(f"{ROOT_DIR}/data/single_partition/partition_0/right_index.gzip")

    df = DataFrame()

    df["tweet_id"] = identifiers.index

    del identifiers

    return df


def __generate_train_test_data(df: DataFrame(), is_train=True):
    document_count = round(len(df) / 1000)
    file_name = f"twitter_train_{document_count}k.txt" if is_train else f"twitter_test_{document_count}k.txt"
    with open(f"{ROOT_DIR}/data/StarSpace_data/{file_name}", "w") as outfile:
        training_data = []
        count = 1
        for row in df.itertuples(index=False):
            content = __get_recommendations_content(row[0])
            formatted_content = '\t'.join(content)
            training_data.append(formatted_content)
            if len(training_data) == 10000:
                outfile.write("\n".join(training_data))
                print(f"Write first {10000 * count} data. Left: {len(df) - (10000 * count)}")
                count += 1
                training_data = []


if __name__ == "__main__":
    df_ids = __get_identifiers()
    click.echo("Starting to generate train data")
    __generate_train_test_data(df_ids, is_train=True)
    click.echo("Finish generating train data")
