import hashlib

from partitioner.partition_base_class import PartitionBase


class SHA256Partition(PartitionBase):
    name = "SHA256"

    def __init__(self, partitions):
        super().__init__(partitions)

    def calculate_partition(self, value) -> int:
        hash_object = hashlib.sha256(value)
        pb_hash = int(hash_object.hexdigest(), 16)
        return pb_hash % self.partitions
