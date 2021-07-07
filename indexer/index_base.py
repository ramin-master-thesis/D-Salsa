from abc import ABC, abstractmethod

from pandas import DataFrame

from partitioner.hash_functions.partition_base import PartitionBase


class IndexBase(ABC):
    left_party: str
    right_party: str

    def __init__(self, partitioning_method: PartitionBase):
        super().__init__()
        self.partitioning_method = partitioning_method

    @abstractmethod
    def create_indices(self, df: DataFrame()):
        pass

    @abstractmethod
    def load_indices(self, partition_number: int):
        pass

    def __str__(self):
        return (
            f'Partitioning method: {self.partitioning_method}\n'
        ).format(**self.__dict__)
