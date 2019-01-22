import numpy as np
from MHCSeqNet.PredictionModel.BindingOnehotPredictor import BindingOnehotPredictor

# Sample data to predict
sample_data = np.array([['TYIGSLPGK', 'HLA-B*58:01'],
                        ['TYIHALDNGLF', 'HLA-A*24:02'],
                        ['AAAWICGEF', 'HLA-B*15:01'],
                        ['TWLTYHGAI', 'HLA-A*30:02'],
                        ['TWLVNSAAHLF', 'HLA-A*24:02']])

# Initialize model instance
bindingOnehotPredictor = BindingOnehotPredictor()

# Load model from path. Please replace [path to project] to the path to the root of this project in your machine.
bindingOnehotPredictor.load_model('./MHCSeqNet/PredictionModel/Pretrained Models/one_hot_model/')

# Predict binding probability in the pair of a peptide and an MHC allele.
result = bindingOnehotPredictor.predict(peptides=sample_data[:, 0],
                                        alleles=sample_data[:, 1])

print(result)
''' The output should be
TYIGSLPGK, HLA-B*58:01 -> 1.0439704e-05
TYIHALDNGLF, HLA-A*24:02 -> 9.9997556e-01
AAAWICGEF, HLA-B*15:01 -> 8.0480677e-01
TWLTYHGAI, HLA-A*30:02 -> 1.6523369e-01
TWLVNSAAHLF, HLA-A*24:02 -> 9.9972767e-01
'''
