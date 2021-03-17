from abc import ABC, abstractmethod


class PartitionBase(ABC):
    name: str

    def __init__(self, partition_count):
        self.partition_count = partition_count
        super().__init__()

    @abstractmethod
    def calculate_partition(self, value) -> int:
        pass

    def __str__(self):
        return (
            f'Name: {self.name}\n'
            f'partitions: {self.partition_count}\n'
        ).format(**self.__dict__)
