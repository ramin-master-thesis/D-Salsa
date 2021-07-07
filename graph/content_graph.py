import pandas as pd

from indexer.tweetid_content_index import TweetIdContentIndex

CONTENT = "content"
CONTENT_INDEX = pd.DataFrame()


class ContentGraph:

    def __init__(self, indexer: TweetIdContentIndex):
        self.indexer = indexer

    def get_content_by_id(self, index: int):
        try:
            content = self.indexer.content_index_df._get_value(index, CONTENT)
            return content
        except KeyError:
            return None
