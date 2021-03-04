from partitioner.hash_functions.partition_base_class import PartitionBase


class ModuloPartition(PartitionBase):
    name = "modulo"

    def __init__(self, partitions):
        super().__init__(partitions)

    def calculate_partition(self, value) -> int:
        return value % self.partitions
