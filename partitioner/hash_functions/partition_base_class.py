from abc import ABC, abstractmethod


class PartitionBase(ABC):
    name: str

    def __init__(self, partitions):
        self.partitions = partitions
        super().__init__()

    @abstractmethod
    def calculate_partition(self, value) -> int:
        pass

    def __str__(self):
        return (
            f'Name: {self.name}\n'
            f'partitions: {self.partitions}\n'
        ).format(**self.__dict__)
