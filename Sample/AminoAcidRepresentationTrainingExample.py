from MHCSeqNet.AminoAcidRepresentationModel.Utility import AminoAcidRepresentationModel

aminoAcidRepresentationModel = AminoAcidRepresentationModel(data_filename="Data/HumanProtein_cleaned.txt",
                                                            window_size=3,
                                                            embedding_dim=6,
                                                            model_filename="Model/Dummy_Model")
aminoAcidRepresentationModel.train(step_size=1024,
                                   step_per_epoch=4,
                                   max_num_epoch=250)
