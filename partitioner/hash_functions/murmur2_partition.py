import struct

from partitioner.hash_functions.partition_base_class import PartitionBase


class Murmur2Partition(PartitionBase):
    name = "murmur2"

    def calculate_partition(self, value: int) -> int:
        data = struct.pack('>Q', value)
        idx = self.__murmur2(data)
        idx &= 0x7fffffff
        return idx % self.partition_count

    @staticmethod
    def __murmur2(data):
        """Pure-python Murmur2 implementation.

        Based on java client, see org.apache.kafka.common.utils.Utils.murmur2

        Args:
            data (bytes): opaque bytes

        Returns: MurmurHash2 of data
        """
        length = len(data)
        seed = 0x9747b28c
        # 'm' and 'r' are mixing constants generated offline.
        # They're not really 'magic', they just happen to work well.
        m = 0x5bd1e995
        r = 24

        # Initialize the hash to a random value
        h = seed ^ length
        length4 = length // 4

        for i in range(length4):
            i4 = i * 4
            k = ((data[i4 + 0] & 0xff) +
                 ((data[i4 + 1] & 0xff) << 8) +
                 ((data[i4 + 2] & 0xff) << 16) +
                 ((data[i4 + 3] & 0xff) << 24))
            k &= 0xffffffff
            k *= m
            k &= 0xffffffff
            k ^= (k % 0x100000000) >> r  # k ^= k >>> r
            k &= 0xffffffff
            k *= m
            k &= 0xffffffff

            h *= m
            h &= 0xffffffff
            h ^= k
            h &= 0xffffffff

        # Handle the last few bytes of the input array
        extra_bytes = length % 4
        if extra_bytes >= 3:
            h ^= (data[(length & ~3) + 2] & 0xff) << 16
            h &= 0xffffffff
        if extra_bytes >= 2:
            h ^= (data[(length & ~3) + 1] & 0xff) << 8
            h &= 0xffffffff
        if extra_bytes >= 1:
            h ^= (data[length & ~3] & 0xff)
            h &= 0xffffffff
            h *= m
            h &= 0xffffffff

        h ^= (h % 0x100000000) >> 13  # h >>> 13;
        h &= 0xffffffff
        h *= m
        h &= 0xffffffff
        h ^= (h % 0x100000000) >> 15  # h >>> 15;
        h &= 0xffffffff

        return h
