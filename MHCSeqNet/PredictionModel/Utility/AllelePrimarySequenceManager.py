import csv


class AllelePrimarySequenceManager:
    AMINO_ACIDS_WITH_UNKNOWN = ['^', '-', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R',
                                'S', 'T', 'V', 'W', 'Y', 'X']
    NUM_AMINO_ACID = len(AMINO_ACIDS_WITH_UNKNOWN)
    sequence_index_dict = {}
    sequence_char_dict = {}

    sequence_lengths = []

    def __init__(self,
                 allele_primary_sequence_information_filename):
        with open(allele_primary_sequence_information_filename, "r") as file:
            csv_data = csv.reader(file, delimiter=',', quotechar="|")
            for row in csv_data:
                self.sequence_lengths = [len(row[1]), len(row[2]), len(row[3])]
                #print(len(row))
                assert(len(row) == 4)
                self.sequence_char_dict[row[0]] = row[1:4]
                self.sequence_index_dict[row[0]] = [self._char_to_index(row[1]),
                                                    self._char_to_index(row[2]),
                                                    self._char_to_index(row[3])]
                assert(len(self.sequence_char_dict[row[0]]) == 3)
                assert(len(self.sequence_index_dict[row[0]]) == 3)

    def _char_to_index(self,
                       peptide):
        indexes = []
        for ac in peptide:
            indexes.append(self.AMINO_ACIDS_WITH_UNKNOWN.index(ac))
        return indexes

    def get_char_sequence(self,
                        type_name):
        return self.sequence_char_dict[type_name]

    def get_index_sequence(self,
                           type_name):
        try:
            return self.sequence_index_dict[type_name]
        except KeyError:
            print("Error:", type_name)
            return self.sequence_index_dict["HLA-A*01:01"]

    def get_type_list(self):
        _types = []
        for _type in self.sequence_index_dict:
            _types.append(_type)
        return _types

    def get_sequence_length(self):
        return self.sequence_lengths
