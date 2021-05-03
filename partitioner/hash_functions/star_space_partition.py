import numpy as np
import starwrap as sw
from numpy.lib import math

from partitioner import current_directory
from partitioner.hash_functions.partition_base_class import PartitionBase


class StarSpacePartition(PartitionBase):
    name = "star-space"

    def __init__(self, partition_count, model_folder):
        # Import model
        arg = sw.args()
        arg.trainMode = 2
        arg.thread = 20
        arg.verbose = True

        self.sp = sw.starSpace(arg)
        self.sp.initFromTsv(f'{current_directory}/../data/StarSpace_data/models/{model_folder}/model.tsv')
        self.proj_mat = np.load(
            f'{current_directory}/../data/StarSpace_data/models/{model_folder}/projection_matrix.npy')
        super().__init__(partition_count)

    def calculate_partition(self, sentence: str) -> int:
        normalized_sentence = self.__normalize_text(sentence)
        vec = np.array(self.sp.getDocVector(normalized_sentence, ' '))[0]
        bits = vec.dot(self.proj_mat) > 0

        number_of_bits = int(math.log2(self.partition_count))
        bits = bits[:number_of_bits].astype(int)
        partition = int("".join(str(i) for i in bits), 2)

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
        res = []
        for char in text.split():
            if char.isspace():
                continue
            elif char.isalpha():
                res.append(char.lower())
            elif char.isnumeric():
                res.append('0')
            elif char.isalnum():
                res.append(char.lower())
            elif char.isascii():
                res.append(char.lower())
            else:
                res.append(char)
        return ' '.join(res)
