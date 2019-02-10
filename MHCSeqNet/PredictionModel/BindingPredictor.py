import os

import numpy as np
from MHCSeqNet.PredictionModel.Utility.EmbeddingLayerManager import EmbeddingLayerManager
from keras.callbacks import EarlyStopping
from keras.models import load_model
from sklearn.model_selection import KFold


# Parent class of BindingPredictor.
class BindingPredictor:

    utility = ""
    models = []

    def __init__(self):
        pass

        # Override This method to create model for one-hot, sequence based model or other models.
    def create_model_for_training(self,
                                  output_model_path,
                                  alleles,
                                  configuration=None,
                                  all_possible_alleles=None):
        return None

    # Override This method to prepare data for one-hot, sequence based model or other models.
    def prepare_training_data(self,
                              peptides,
                              alleles,
                              labels):
        return None, None

    # Override This method to initialize Utility instance which is different on each model.
    def create_utility(self,
                       model_path):
        return None

    def load_model(self, model_path):
        """ Load models along with its supporting allele. After the model is loaded. the model can be trained further or
        can predict binding probabilities.

        :param model_path: (str) The path at which the model located.
        :return:

        """
        assert os.path.isdir(model_path), "Model directory does not exist."

        self.utility = self.create_utility(model_path)
        files = os.listdir(model_path)
        index = 1
        while "model_%d.h5" % index in files:
            self.models.append(load_model(model_path + "model_%d.h5" %(index)))
            index += 1
        assert index != 1, "No model file found"

    def train_model(self,
                    output_model_path,
                    peptides,
                    alleles,
                    labels,
                    configuration=None,
                    amino_acid_representation_path="",
                    all_possible_alleles=None):
        """ Load up amino acid representation and train the model with the specified configuration.

        :param output_model_path: (str) A path to save the trained model(s).
        :param peptides: (list of str) List of peptides in the training data. The size of this list should be equal to
                size of alleles list and labels list. Also, the unclear amino acids such as 'X' are not supported.
        :param alleles: (list of str) List of alleles in the training data. The format of an allele is not strict.
                However, the model predict binding probability based on allele name specified here. So, make sure it has
                the same format.
        :param labels: (list of str) List of labels in the training data.
        :param configuration: (dict of <str,float>)The configuration of the model. The example of a configuration is in
                    - PredictionModel/Utility/OnehotBasedModel.py for one-hot based model
                    - PredictionModel/Utility/SequenceBasedModel.py for sequence based model
                Also, to modify the model further, Just directly edit the function in those files directly
        :param amino_acid_representation_path: (str) The trained amino acid representation to load into the model. To
                train new representation, see example in Sample/AminoAcidRepresentationTrainingExample.py
        :param all_possible_alleles: (list of str) The list of all possible allele.
                - For one-hot based model, the model can support only alleles from these parameters. The trained model
                cannot be trained further to support new alleles. The only way to make a one-hot model support new
                allele is to trained a new model from scratch.
                - For sequence based model, this parameter is not necessary since the model can support all alleles as
                long as the sequence are known. The complete list of allele sequence is in
                PredictionModel/UtilityAlleleInformation.txt.
        :return:
        """
        if os.path.isdir(output_model_path):
            print("Output model directory already exist.")
        else:
            try:
                print("Making output model directory")
                os.makedirs(output_model_path)
            except OSError:
                print("Cannot create new directory")
                return

        assert len(peptides) == len(alleles), "Length of the list of peptides is not equal to the length of the" \
                                              " list of alleles"
        assert len(peptides) == len(labels), "Length of the list of peptides is not equal to the length of" \
                                             " the list of labels"

        if len(self.models) != 0:
            print("Model already loaded. Continue training from the loaded model.")
            if configuration is None:
                raise(ValueError("Cannot trained the loaded model because there is no configuration specified"))
        else:
            configuration = self.create_model_for_training(output_model_path,
                                                           alleles,
                                                           configuration,
                                                           all_possible_alleles)

        peptides_converted, alleles_converted, labels_converted = self.utility.process_data(peptides=peptides,
                                                                                            alleles=alleles,
                                                                                            labels=labels)

        np.random.shuffle([peptides_converted, alleles_converted, labels_converted])

        try:
            for model in self.models:
                EmbeddingLayerManager.load_embedded_weight(model,
                                                           amino_acid_representation_path,
                                                           configuration['embedded_dim'],
                                                           len(self.utility.get_acceptable_amino_acid()))
        except OSError:
            raise OSError("Cannot load peptide representation")

        kf = KFold(n_splits=configuration['num_model'])
        fold_index = 1
        for train_indexes, test_indexes in kf.split(peptides_converted):
            peptides_training_converted = peptides_converted[train_indexes]
            alleles_training_converted = alleles_converted[train_indexes]
            labels_training_converted = labels_converted[train_indexes]

            X, y = self.prepare_training_data(peptides_training_converted,
                                              alleles_training_converted,
                                              labels_training_converted)

            print("Loading peptide representation")
            print("Peptide representation loaded")
            early_stopper = EarlyStopping(monitor='val_loss',
                                          min_delta=0,
                                          patience=7,
                                          verbose=2, mode='auto')
            callbacks = [early_stopper]
            self.models[fold_index - 1].fit(X,
                                      y,
                                      epochs=configuration['max_num_epoch'],
                                      shuffle=True,
                                      validation_split=0.2,
                                      batch_size=1024,
                                      callbacks=callbacks,
                                      verbose=1)
            self.models[fold_index - 1].save(output_model_path + "/model_%d.h5" % fold_index)
            fold_index += 1

    def get_supported_alleles(self):
        """ Get list of all supported alleles

        :return: (list of str). List of all supported alleles
        """
        supported_alleles = self.utility.get_acceptable_types()
        return supported_alleles

    def predict(self,
                peptides,
                alleles):
        """ Predict binding probability from list of peptides and list of alleles

        :param peptides: (list of str) List of peptides. The size of this list should be equal to size of alleles list
                and labels list. Also, the unclear amino acids such as 'X' are not supported.
        :param alleles: (list of str) List of alleles. The list of all supported alleles in a model is in
                [MODEL PATH]/supported_alleles.txt.
        :return: (list of float): List of binding probabilities.
        """
        assert len(self.models) != 0, "Model is not loaded or trained yet."
        labels = []
        for _ in peptides:
            labels.append(0.0)
        # print(peptides_converted, alleles_converted, labels_converted)
        peptides_converted, alleles_converted, labels_converted = self.utility.process_data(peptides=peptides,
                                                                                            alleles=alleles,
                                                                                            labels=labels)
        print(peptides_converted, alleles_converted, labels_converted)
        X, y = self.prepare_training_data(peptides_converted,
                                          alleles_converted,
                                          labels_converted)

        result = []
        print("Starting Prediction")
        for index, model in enumerate(self.models):
            print("Predict from model %d" % index)
            result.append(model.predict(X, verbose=2))
        result = np.array(result)
        return np.median(result, axis=0)
