# MHCSeqNet

MHCSeqNet is a MHC ligand prediction python package. Current release was trained using only MHC class I data but we have demonstrated that the model architecture of MHCSeqNet can generalize to MHC class II data (https://www.biorxiv.org/content/early/2018/07/18/371591).

## Installation (From Source)
MHCSeqNet supports only Python 3.4+.
We have plan to make MHCSeqNet available via 'pip install' but for now installing from source is the only way.
1. Clone this repository 
2. MHCSeqNet is developed using these exact version of external packages. We cannot guarantee if MHCSeqNet works on older version of these packages.
```
numpy==1.14.3
Keras==2.2.0
tensorflow==1.6.0
scipy==1.1.0
scikit-learn==0.19.1
```
3. Install setuptools using pip (if your system's default Python is Python3) or pip3 (if your system contains both Python2 and Python3 and the default is Python2) to setup MHCSeqNet to be able to import system-wide. (Also ensure that you install the latest version)
```
pip install setuptools
pip3 install setuptools
```
4. Run Setup.py to install MHCSeqNet.
```
python Setup.py install
python3 Setup.py install
```

## How to use MHCSeqNet
### Models
There are two version of the models.
- One-hot based model: This model supports only a limited set of MHC alleles that are present in the training dataset. The full list of the supported alleles can be found in 
```
PredictionModel/Pretrained Models/one_hot_model/supported_alleles.txt
```
- Sequence based model: This model is trained on the same set of alleles as one-hot based model but is able to predict any MHC alleles as long as the amino acid sequence is known. Please consult our preprint The full list of known MHC allele sequences can be found in
```
PredictionModel/Pretrained Models/sequence_model/supported_alleles.txt
```

### Input
- Peptide: We supports peptide of length 8 - 15 consisted of these amino acids:
```
'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', and 'Y'.
```
- MHC Protein: As described above, there are two version of the models supporting different set of MHC allele.
### Output
- Binding probability: Rather than binding affinity, these models predict binding probability ranging from 0.0 to 1.0 where 0.0 indicates a non-binder and 1.0 indicates a strong binder.

### Sample
Sample scripts of how to use MHCSeqNet to predict binding probability is in sample/
  - For prediction using one-hot based model, follow an example in ```sample/OnehotModelPredictionExample.py```
  - For prediction using sequence based model, follow an example in ```sample/SequenceModelPredictionExample.py```
