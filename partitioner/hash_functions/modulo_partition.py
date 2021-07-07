from partitioner.hash_functions.partition_base import PartitionBase


class ModuloPartition(PartitionBase):
    name = "modulo"

    def __init__(self, partition_count):
        super().__init__(partition_count)

    def calculate_partition(self, value: int) -> int:
        return value % self.partition_count
