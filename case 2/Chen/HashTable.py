__author__ = 'Chan'


class HashTable(object):

    __doc__ = """
        Class HashTable use the string hash algorithm 'BKDRHash' because it guarantees satisfactory performance and is
        easy to implement.
        When duplicated data_value emerges, we store it in a list.
        We avoid using built-in type dictionary because it is implemented using hashing itself.
        We assume rids are unique.
        """

    @staticmethod
    def __BKDRHash(string):
        seed = 131  # 31, 131, 1313, 1313131 etc...
        hs = 0
        for letter in string:
            hs = hs * seed + ord(letter)

        return hs & 0x7FFFFFFF  # Hash values are unsigned integers.

    def __init__(self):
        self.buckets_number = 8  # We use 8 buckets here
        self.table = [[] for idx in range(self.buckets_number)]

    def Put(self, key, data_value):
        # Invert the hash value which is a binary string in to integer between [0, 8]
        assert data_value is not None, "Data value must be valid."
        # Most movies are made in 20th century so we abandon first two digit to accelerate our program.
        hash_value = int(bin(self.__BKDRHash(str(data_value)[2:]))[-3:], base=2)
        self.table[hash_value].append((data_value, key))

    def Get(self, data_value):
        assert data_value is not None, "Data value must be valid."
        hash_value = int(bin(self.__BKDRHash(str(data_value)[2:]))[-3:], base=2)
        candidates = self.table[hash_value]
        results = []
        for idx in range(len(candidates)):
            if data_value == candidates[idx][0]:
                results.append(candidates[idx][1])

        return results

    def Remove(self, key):
        assert key is not None, "Key must be valid."
        for idx in range(self.buckets_number):
            for idx2 in self.table[idx]:
                if self.table[idx][idx2] == key:
                    self.table[idx].pop(idx2)
                    return
        print('Key: %d does not exist.' % key)
        return
