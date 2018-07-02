import csv
import numpy as np
from keras.utils import to_categorical


class DataProcessingUtility:
    AMINO_ACIDS = ['^', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W',
                   'Y']
    NUM_AMINO_ACID = len(AMINO_ACIDS)
    AMINO_ACID_TO_INDEX = {}
    TYPE_TO_INDEX = {}

    ACCEPTABLE_TYPES = []
    allelePrimarySequenceManager = None
    NUM_ACCEPTABLE_TYPE = 0

    MAX_PEPTIDE_LENGTH = 15
    MODEL_TYPE = ""

    def __init__(self,
                 acceptable_types_filename="Acceptable_Type.txt",
                 allele_primary_sequence_manager=None,
                 max_peptide_length=15):
        self.MAX_PEPTIDE_LENGTH = max_peptide_length
        self.ACCEPTABLE_TYPES, self.NUM_ACCEPTABLE_TYPE = self.get_acceptable_types_from_file(
            acceptable_types_filename)
        if self.MODEL_TYPE == "sequence":
            self.allelePrimarySequenceManager = allele_primary_sequence_manager

        for index, amino_acid in enumerate(self.AMINO_ACIDS):
            self.AMINO_ACID_TO_INDEX[amino_acid] = index
        for index, acceptable_type in enumerate(self.ACCEPTABLE_TYPES):
            self.TYPE_TO_INDEX[acceptable_type] = index

    def get_acceptable_amino_acid(self):
        return self.AMINO_ACIDS

    def get_acceptable_types(self):
        return self.ACCEPTABLE_TYPES

    def get_acceptable_types_from_file(self, acceptable_types_filename):
        with open(acceptable_types_filename,
                  "r") as file:
            acceptable_types = []
            csv_data = csv.reader(file, delimiter=',', quotechar='|')
            for i, row in enumerate(csv_data):
                if i == 0:
                    if row[0] == "sequence model":
                        self.MODEL_TYPE = "sequence"
                        print("Using Sequence Model")
                    elif row[0] == "onehot model":
                        self.MODEL_TYPE = "onehot"
                        print("Using One-hot Model")
                    else:
                        raise(ValueError("No Model Type Specified"))
                    continue
                acceptable_types += row
            num_acceptable_type = len(acceptable_types)
            return acceptable_types, num_acceptable_type

    def process_data(self,
                     peptides,
                     alleles,
                     labels):
        X_raw = []
        for index in range(len(peptides)):
            X_raw.append([peptides[index], alleles[index], labels[index]])
        X_peptide, X_allele, y = self.convert_data(X_raw)

        data_x_1 = np.array(X_peptide)
        data_x_2 = X_allele
        if self.MODEL_TYPE == "onehot":
            data_x_2 = to_categorical(data_x_2, num_classes=self.NUM_ACCEPTABLE_TYPE)
        elif self.MODEL_TYPE == "sequence":
            data_x_2 = self._type_index_to_sequence(data_x_2)
        return data_x_1, data_x_2, np.array(y)

    def _type_index_to_sequence(self,
                                type_indexes):
        index_sequences_array = []
        type_indexes = np.array(type_indexes).astype(int)
        for index in type_indexes:
            index_sequences = self.allelePrimarySequenceManager.get_index_sequence(self.ACCEPTABLE_TYPES[index])
            index_sequences_array.append([index_sequences[0], index_sequences[1], index_sequences[2]])
        index_sequences_array = np.array(index_sequences_array)
        return index_sequences_array

    def convert_peptide(self, peptide):
        try:
            idx_list = []
            for p in peptide:
                idx = self.AMINO_ACIDS.index(p)
                idx_list.append(idx)
            return idx_list
        except ValueError:
            raise ValueError("Peptide %s consist of not supported amino acid." % peptide)

    def convert_allele(self, allele):
        try:
            idx = self.ACCEPTABLE_TYPES.index(allele)
            return idx
        except ValueError:
            raise ValueError("Allele %s is not supported" % allele)

    def convert_data(self, rows):
        X_peptide = []
        X_alelle = []
        y_data = []
        for index, row in enumerate(rows):
            X_row = []
            converted_peptide = self.convert_peptide(row[0])
            converted_allele = self.convert_allele(row[1])
            converted_label = float(row[2])
            if(converted_label < 0.0 or converted_label > 1.0):
                raise ValueError("Label is not in range between 0.0 and 1.0")

            X_peptide.append(converted_peptide)
            X_alelle.append(converted_allele)
            y_data.append(converted_label)

        for index, val in enumerate(X_peptide):
            X_peptide[index] = ([0] * (self.MAX_PEPTIDE_LENGTH - len(X_peptide[index]))) + X_peptide[index]
        return X_peptide, X_alelle, y_data

    def convert_type_to_bucket(self, t):
        bucket_list = [0] * self.NUM_ACCEPTABLE_TYPE
        bucket_list[self.TYPE_TO_INDEX[t]] += 1
        return bucket_list

    def convert_amino_acid_to_bucket(self, protein):
        bucket_list = [0] * self.NUM_AMINO_ACID
        for p in protein:
            bucket_list[self.AMINO_ACID_TO_INDEX[p]] += 1
        return bucket_list
