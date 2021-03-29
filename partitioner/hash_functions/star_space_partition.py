import numpy as np
import starwrap as sw

from partitioner import current_directory
from partitioner.hash_functions.partition_base_class import PartitionBase


class StarSpacePartition(PartitionBase):
    name = "StarSpace"

    def __init__(self, partition_count):
        # Import model
        arg = sw.args()
        arg.trainMode = 2
        arg.thread = 20
        arg.normalizeText = True
        arg.verbose = True

        self.sp = sw.starSpace(arg)
        self.sp.initFromTsv(f'{current_directory}/../data/StarSpace_data/models/model.tsv')
        self.proj_mat = np.load(f'{current_directory}/../data/StarSpace_data/projection_matrix.npy')
        super().__init__(partition_count)

    def calculate_partition(self, sentences) -> int:
        vec = np.array(self.sp.getDocVector(sentences, ' '))[0]
        bits = vec.dot(self.proj_mat) > 0

        partition = 0
        if bits[0]:
            partition = 1

        return partition
