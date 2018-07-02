import numpy as np
from PredictionModel.Utility.AllelePrimarySequenceManager import AllelePrimarySequenceManager
from PredictionModel.Utility.DataProcessingUtility import DataProcessingUtility
from PredictionModel.Utility.SequenceBasedModel import SequenceBasedModel

from MHCSeqNet.PredictionModel.BindingPredictor import BindingPredictor


class BindingSequencePredictor(BindingPredictor):
    allelePrimarySequenceManager = None

    def __init__(self):
        super(BindingSequencePredictor, self).__init__()

    def create_model_for_training(self,
                                  output_model_path,
                                  alleles,
                                  configuration=None,
                                  all_possible_alleles=None):
        if configuration is None:
            print("Model configuration parameter is empty. Using default parameters.")
            configuration = SequenceBasedModel.get_default_configuration()

        print("For sequence based model, Supported allele(s) for prediction is all alleles listed in Utility/AlleleInformation.txt.")
        self.allelePrimarySequenceManager = AllelePrimarySequenceManager("Utility/AlleleInformation.txt")
        all_possible_alleles = self.allelePrimarySequenceManager.get_type_list()

        supported_allele_file = open(output_model_path + "/supported_alleles.txt", "w")
        supported_allele_file.write("sequence model" + "\n")
        for allele in all_possible_alleles:
            supported_allele_file.write(allele + "\n")
        supported_allele_file.close()

        self.utility = DataProcessingUtility(acceptable_types_filename=output_model_path + "/supported_alleles.txt",
                                             allele_primary_sequence_manager=self.allelePrimarySequenceManager)

        for _ in range(configuration['num_model']):
            self.models.append(SequenceBasedModel.get_sequence_based_model(
                    configuration,
                    self.utility.MAX_PEPTIDE_LENGTH,
                    self.utility.NUM_ACCEPTABLE_TYPE,
                    self.allelePrimarySequenceManager.get_sequence_length()))
        return configuration

    def prepare_training_data(self,
                              peptides_training_converted,
                              alleles_training_converted,
                              labels_training_converted):
        allele_first = np.array(alleles_training_converted[:, 0].tolist())
        allele_middle = np.array(alleles_training_converted[:, 1].tolist())
        allele_last = np.array(alleles_training_converted[:, 2].tolist())
        return [peptides_training_converted, allele_middle, allele_last], labels_training_converted

    def create_utility(self,
                       model_path):
        self.allelePrimarySequenceManager = AllelePrimarySequenceManager(model_path + "/AlleleInformation.txt")
        return DataProcessingUtility(acceptable_types_filename=model_path + "/supported_alleles.txt",
                                     allele_primary_sequence_manager=self.allelePrimarySequenceManager)
