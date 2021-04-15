import numpy as np
import starwrap as sw

from partitioner import current_directory
from partitioner.hash_functions.partition_base_class import PartitionBase


class StarSpacePartition(PartitionBase):
    name = "StarSpace"

    def __init__(self, partition_count, model_params):
        # Import model
        arg = sw.args()
        arg.trainMode = 2
        arg.thread = 20
        arg.verbose = True

        self.sp = sw.starSpace(arg)
        self.sp.initFromTsv(f'{current_directory}/../data/StarSpace_data/models/{model_params}/model.tsv')
        self.proj_mat = np.load(f'{current_directory}/../data/StarSpace_data/models/{model_params}/projection_matrix.npy')
        super().__init__(partition_count)

    def calculate_partition(self, sentence: str) -> int:
        # normalized_sentence = self.__normalize_text(sentence)
        vec = np.array(self.sp.getDocVector(sentence, ' '))[0]
        bits = vec.dot(self.proj_mat) > 0

        partition = 0
        if bits[0]:
            partition = 1

        return partition

    @staticmethod
    def __normalize_text(text: str):
        """
        We categorize longer strings into the following buckets:

        1. All punctuation-and-numeric. Things in this bucket get
           their numbers flattened, to prevent combinatorial explosions.
           They might be specific numbers, prices, etc.

        2. All letters: case-flattened.

        3. Mixed letters and numbers: a product ID? Flatten case and leave
           numbers alone.

        The case-normalization is state-machine-driven.
        :param text: incoming string to normalize
        :return: lower case string or flatten number
        """
        if text.isnumeric():
            return '0'
        if text.isalnum():
            return text.lower()
