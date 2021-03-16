import click
import pandas as pd
import requests
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from start_space import current_directory


def __get_recommendations_content(identifier: int) -> list:
    # api-endpoint
    url = f"http://localhost:5001/recommendation/salsa/tweet/{identifier}"

    # defining a params dict for the parameters to be sent to the API
    params = {'first': True, 'content': True}

    # sending get request and saving the response as response object
    r = requests.get(url=url, params=params)

    # extracting data in json format
    data = r.json()

    return data


def __get_identifiers():
    identifiers = pd.read_csv(f"{current_directory}/../data/right_index_new.csv", usecols=[0])
    return identifiers


def __generate_train_test_data(df: DataFrame(), is_train=True):
    training_data = []
    for row in df.itertuples(index=False):
        content = __get_recommendations_content(row[0])
        formatted_content = '\t'.join(content)
        training_data.append(formatted_content)
    file_name = "twitter_train130k.txt" if is_train else "twitter_test30k.txt"
    with open(f"{current_directory}/../data/{file_name}", "w") as outfile:
        outfile.write("\n".join(training_data))


if __name__ == "__main__":
    df_ids = __get_identifiers()
    train, test = train_test_split(df_ids, test_size=0.2)
    __generate_train_test_data(test, is_train=False)
    click.echo("Finish generating test data")
    __generate_train_test_data(train, is_train=True)
    click.echo("Finish generating train data")
