from partitioner.hash_functions.partition_base import PartitionBase


class SinglePartition(PartitionBase):
    name = "single_partition"

    def __init__(self):
        super().__init__(partition_count=1)

    def calculate_partition(self, value) -> int:
        return 0
