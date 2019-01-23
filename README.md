## What is MHCSeqNet?

MHCSeqNet is a MHC ligand prediction python package developed by the [Computational Molecular Biology Group](http://cmb.md.chula.ac.th/) at Chulalongkorn University, Bangkok, Thailand. MHCSeqNet utilizes recurrent neural networks to process input ligand's and MHC allele's amino acid sequences and therefore can be to extended to handle peptide of any length and any MHC allele with known amino acid sequence. 

The current release was trained using only data from MHC class I and supports peptides ranging from 8 to 15 amino acids in length, but the model can be re-trained to support more alleles and wider ranges of peptide length. 

Please see our [preprint on bioRxiv](https://www.biorxiv.org/content/early/2018/11/08/371591) for more information.

### Models
MHCSeqNet offers two versions of prediction models
1. One-hot model: This model uses data from each MHC allele to train a separate predictor for that allele. The list of supported MHC alleles for the current release can be found [here](https://github.com/cmbcu/MHCSeqNet/blob/master/MHCSeqNet/PredictionModel/Pretrained%20Models/one_hot_model/supported_alleles.txt) 

2. Sequence-based model: This model use data from all MHC alleles to train a single predictor that can handle any MHC allele whose amino acid sequence is known. For more information on how our model learns MHC allele information in the form of amino acid sequence, please see our [preprint on bioRxiv](https://www.biorxiv.org/content/early/2018/11/08/371591). The list of MHC alleles used to train this model can be found [here](https://github.com/cmbcu/MHCSeqNet/blob/master/MHCSeqNet/PredictionModel/Pretrained%20Models/sequence_model/supported_alleles.txt)

## How to install?
MHCSeqNet requires Python 3 (>= 3.4) and the following Python packages:
```
numpy (>= 1.14.3)
Keras (>= 2.2.0)
tensorflow (>= 1.6.0)
scipy (>= 1.1.0)
scikit-learn (>= 0.19.1)
```
If your system has both Python 2 and Python 3, please make sure that Python 3 is being used when following these instructions.
Note that we cannot guarantee whether MHCSeqNet will work with older versions of these packages.

To install MHCSeqNet:
1. Clone this repository
```
git clone https://github.com/cmbcu/MHCSeqNet
```
Or you may find other methods for cloning a GitHub repository [here](https://help.github.com/articles/cloning-a-repository/)

2. Install the latest version of 'pip' and 'setuptools' packages for Python 3 if your system does not already have them
```
python -m ensurepip --default-pip
pip install setuptools
```
If you have trouble with this step, more information can be found [here](https://packaging.python.org/tutorials/installing-packages/#install-pip-setuptools-and-wheel)

3. Run Setup.py inside MHCSeqNet directory to install MHCSeqNet.
```
cd MHCSeqNet
python Setup.py install
```

## How to use MHCSeqNet?
We are in the process of making MHCSeqNet more user-friendly. For now, some basic understanding of computer programming is required to adjust our sample scripts for personal uses.

### Examples
Sample scripts for running MHCSeqNet in either the 'one-hot' mode or 'sequence-based' can be found in the 'Sample' directory.
Continuing from the installation process, you may test the installation of MHCSeqNet through the following commands:
```
python Sample/OnehotModelPredictionExample.py
python Sample/SequenceModelPredictionExample.py
```

To run the sample scripts from different locations on your system, please edit the path to pretrained model in the respective script.
```
bindingOnehotPredictor.load_model('./MHCSeqNet/PredictionModel/Pretrained Models/one_hot_model/')
bindingSequencePredictor.load_model('./MHCSeqNet/PredictionModel/Pretrained Models/sequence_model/')
```

To replace sample peptides and MHC alleles with your own lists, please edit the 'sample_data' accordingly.
```
sample_data = np.array([['TYIGSLPGK', 'HLA-B*58:01'],
                        ['TYIHALDNGLF', 'HLA-A*24:02'],
                        ['AAAWICGEF', 'HLA-B*15:01'],
                        ['TWLTYHGAI', 'HLA-A*30:02'],
                        ['TWLVNSAAHLF', 'HLA-A*24:02']])
```

To adjust the behavior of how prediction results are output (e.g. print results to file rather than on the screen), please edit the following line:
```
print(result)
```

### Input format
Peptide: The current release supports peptides of length 8 - 15 and does not accept ambiguous amino acids.

MHC allele: For alleles included in the training set (i.e. supported alleles listed in the [models](https://github.com/cmbcu/MHCSeqNet#models) section), the model requires the 'HLA-A\*XX:YY' format. 

To add new MHC alleles to the sequence-based model, the names and amino acid sequences of the new alleles must first be added to the [AlleleInformation.txt and supported_alleles.txt](https://github.com/cmbcu/MHCSeqNet/tree/master/MHCSeqNet/PredictionModel/Pretrained%20Models/sequence_model) in the sequence-based model's directory.

### Output
MHCSeqNet output binding probability ranging from 0.0 to 1.0 where 0.0 indicates an unlikely ligand and 1.0 indicates a likely ligand.
