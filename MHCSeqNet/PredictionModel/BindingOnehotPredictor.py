from PredictionModel.BindingPredictor import BindingPredictor
from PredictionModel.Utility.DataProcessingUtility import DataProcessingUtility
from MHCSeqNet.PredictionModel.Utility.OnehotBasedModel import OnehotBasedModel


# A class used for training and predicting binding probability using one-hot based model. The example of the usage of
# this class can be found in Sample/OneHotModelTrainingExample.py
class BindingOneHotPredictor(BindingPredictor):

    def __init__(self):
        super(BindingOneHotPredictor, self).__init__()

    def create_model_for_training(self,
                                  output_model_path,
                                  alleles,
                                  configuration=None,
                                  all_possible_alleles=None):
        if configuration is None:
            print("Model configuration parameter is empty. Using default parameters.")
            configuration = OnehotBasedModel.get_default_configuration()

        if all_possible_alleles is None:
            print("All possible allele(s) is not explicitly defined. The model will support alleles only from the "
                  "training data. The model cannot predict or train to predict any new allele.")
            all_possible_alleles = []
            for allele in alleles:
                all_possible_alleles.append(allele)
            all_possible_alleles = set(all_possible_alleles)
            all_possible_alleles = list(all_possible_alleles)
        else:
            print("Getting all possible alleles from the parameters. Note that the model cannot predict or train to "
                  "predict any new allele.")
        supported_allele_file = open(output_model_path + "/supported_alleles.txt", "w")
        supported_allele_file.write("onehot model" + "\n")
        for allele in all_possible_alleles:
            supported_allele_file.write(allele + "\n")
        supported_allele_file.close()

        self.utility = DataProcessingUtility(acceptable_types_filename=output_model_path + "/supported_alleles.txt")

        for _ in range(configuration['num_model']):
            self.models.append(OnehotBasedModel.get_one_hot_based_model(configuration,
                                                                        self.utility.MAX_PEPTIDE_LENGTH,
                                                                        self.utility.NUM_ACCEPTABLE_TYPE))
        return configuration

    def prepare_training_data(self,
                              peptides_training_converted,
                              alleles_training_converted,
                              labels_training_converted):

        return [peptides_training_converted, alleles_training_converted], labels_training_converted

    def create_utility(self,
                       model_path):
        return DataProcessingUtility(acceptable_types_filename=model_path + "/supported_alleles.txt")