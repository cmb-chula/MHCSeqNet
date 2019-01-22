import numpy as np
from MHCSeqNet.PredictionModel.BindingSequencePredictor import BindingSequencePredictor

# Sample data to predict
sample_data = np.array([['TYIGSLPGK','HLA-B*58:01'],
                        ['TYIHALDNGLF','HLA-A*24:02'],
                        ['AAAWICGEF','HLA-B*15:01'],
                        ['TWLTYHGAI','HLA-A*30:02'],
                        ['TWLVNSAAHLF','HLA-A*24:02']])

# Initialize model instance
bindingSequencePredictor = BindingSequencePredictor()

# Load model from path. Please replace [path to project] to the path to the root of this project in your machine.
bindingSequencePredictor.load_model('./MHCSeqNet/PredictionModel/Pretrained Models/sequence_model/')

# Predict binding probability in the pair of a peptide and an MHC allele.
result = bindingSequencePredictor.predict(peptides=sample_data[:, 0],
                                          alleles=sample_data[:, 1])
print(result)
''' The output should be
TYIGSLPGK, HLA-B*58:01 -> 0.00414377
TYIHALDNGLF, HLA-A*24:02 -> 0.9999896 
AAAWICGEF, HLA-B*15:01 -> 0.9537278 
TWLTYHGAI, HLA-A*30:02 -> 0.11183099
TWLVNSAAHLF, HLA-A*24:02 -> 0.9995604 
'''
