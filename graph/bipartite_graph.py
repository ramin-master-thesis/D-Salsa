from indexer.index_base import IndexBase


class BipartiteGraph:
    ADJACENCY_LIST = "adjacency_list"

    def __init__(self, indexer: IndexBase):
        self.indexer = indexer

    def get_left_node_neighbors(self, node_id: int) -> list:
        try:
            values = self.indexer.left_index_df._get_value(node_id, self.ADJACENCY_LIST)
        except KeyError:
            return []
        return values

    def get_right_node_neighbors(self, node_id: int) -> list:
        try:
            values = self.indexer.right_index_df._get_value(node_id, self.ADJACENCY_LIST)
        except KeyError:
            return []
        return values

    def get_edges_count(self) -> int:
        return int(self.indexer.right_index_df[self.ADJACENCY_LIST].str.len().sum())

    def get_left_index_node_count(self) -> int:
        return len(self.indexer.left_index_df)

    def get_right_index_node_count(self) -> int:
        return len(self.indexer.right_index_df)
