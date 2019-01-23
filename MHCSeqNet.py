######################################
import numpy as np
import sys

argv = sys.argv

######################################
### test whether the user provided valid arguments
def invalid_argument(arg):
    invalid_flag = False
    if not '-p' in arg and not '--path' in arg:
        invalid_flag = True
        print('Error: -p/--path argument is required')
    if not '-m' in arg and not '--model' in arg:
        invalid_flag = True
        print('Error: -m/--model argument is required')
    if not '-i' in arg and not '--input-mode' in arg:
        invalid_flag = True
        print('Error: -i/--input-mode argument is required')
    
    ## print detected error
    if invalid_flag:
        print('Please see help information below:')
        
    return invalid_flag
    
### print help statement
def print_help():
    print('MHCSeqNet - a tool for predicting MHC ligand\n' + \
          'usage: python MHCSeqNet.py [options] peptide_file allele_file output_file\n' + \
          '         \'peptide_file\' and \'allele_file\' should each contains only one column, without header row\n' + \
          '  options:\n' + \
          '    -p, --path                             REQUIRED: Speficy the path to pre-trained model directory\n' + \
          '                                           This should be either the \'one_hot_model\' or the \'sequence_model\'\n' + \
          '                                            directory located in \'PATH/PretrainedModels/\' where PATH is where\n' + \
          '                                            MHCSeqNet was downloaded to\n' + \
          '    -m, --model        [onehot sequence]   REQUIRED: Specify whether the one-hot model or sequence-based model will be used\n' + \
          '    -i, --input-mode   [paired complete]   REQUIRED: Specify whether the prediction should be made for each pair of peptide\n' + \
          '                                            and allele on the same row of each input file [paired] or for all\n' + \
          '                                            combinations of peptides and alleles [complete]\n' + \
          '    -h, --help                             Print this message')    

### extract argument values
def extract_required_arg(arg):
    if '-p' in arg:
        path_loc = arg.index('-p')
    else:
        path_loc = arg.index('--path')
    
    if '-m' in arg:
        model_loc = arg.index('-m')
    else:
        model_loc = arg.index('--model')
    
    if '-i' in arg:
        input_loc = arg.index('-i')
    else:
        input_loc = arg.index('--input-mode')
    
    return arg[path_loc + 1], arg[model_loc + 1], arg[input_loc + 1]

######################################
## first check for -h or --help flag
if '-h' in argv or '--help' in argv or invalid_argument(argv):
    print_help()

else:
    ######################################
    ### if everything checks out, extract all arguments
    model_path, model_mode, input_mode = extract_required_arg(argv)
    peptide_file = argv[-3]
    allele_file = argv[-2]
    output_file = argv[-1]

    ### import predictor
    if model_mode == 'onehot':
        from MHCSeqNet.PredictionModel.BindingOnehotPredictor import BindingOnehotPredictor as LocalPredictor
    else:
        from MHCSeqNet.PredictionModel.BindingSequencePredictor import BindingSequencePredictor as LocalPredictor

    localPredictor = LocalPredictor()
    localPredictor.load_model(model_path)

    ### load peptides and alleles data
    peptides = []
    with open(peptide_file, 'rt') as fin:
        for line in fin.readlines():
            if not len(line.strip()) == 0:
                peptides.append(line.strip())

    alleles = []
    with open(allele_file, 'rt') as fin:
        for line in fin.readlines():
            if not len(line.strip()) == 0:
                alleles.append(line.strip())

    ### setup input array
    if input_mode == 'paired':
        assert len(peptides) == len(alleles), 'PAIRED input mode is specified but the numbers of input peptides and alleles are different'
        input_data = np.array([[peptides[i], alleles[i]] for i in range(len(peptides))])
    else:
        input_data = []

        for p in peptides:
            for a in alleles:
                input_data.append([p, a])

        input_data = np.array(input_data)

    ### make prediction
    result = localPredictor.predict(peptides=input_data[:, 0], alleles=input_data[:, 1])

    ### output results
    with open(output_file, 'w') as fout:
        for i in range(len(result)):
            fout.write('\t'.join([input_data[i, 0], input_data[i, 1], str(result[i][0])]) + '\n')

    print('Done! Wrote output to ' + output_file)
