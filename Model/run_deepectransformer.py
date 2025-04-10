import os
import shutil
import logging

import numpy as np
import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F

from deepec.process_data import read_EC_actual_Fasta
from deepec.data_loader import DeepECDataset
from deepec.utils import argument_parser, run_neural_net, save_dl_result
from deepec.homology import run_blastp, read_best_blast_result, merge_predictions

import codecs
import pickle

# ========== BEGIN legacy alias patch ==========
import sys #JLK
import types #JLK
import transformers.models.bert.modeling_bert as new_bert_module #JLK
import transformers.models.bert.configuration_bert as configuration_bert #JLK
import transformers.models.bert.tokenization_bert as tokenization_bert #JLK

sys.modules['transformers.modeling_bert'] = new_bert_module #JLK
sys.modules['transformers.configuration_bert'] = configuration_bert #JLK
sys.modules['transformers.tokenization_bert'] = tokenization_bert #JLK
# ========== END legacy alias patch ============

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')


if __name__ == '__main__':
    parser = argument_parser()
    options = parser.parse_args()

    output_dir = options.output_dir
    input_data_file = options.seq_file
    print("Raw GPU option:", repr(options.gpu))
    print("Type:", type(options.gpu))
    gpu_raw = options.gpu
    gpu_clean = gpu_raw.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    gpu_clean = gpu_clean.strip()
    device = torch.device(gpu_clean)
   # device = options.gpu
   # device = torch.device(options.gpu)
    batch_size = options.batch_size
    num_cpu = options.cpu_num

    torch.set_num_threads(num_cpu)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(output_dir + '/tmp'):
        os.makedirs((output_dir+'/tmp'))
 
    model = torch.load('/home/smallikao/DeepProZyme/model/model.pth') # JLK: torch.load -> torch.jit.load
    #model = torch.jit.load('/home/smallikao/DeepProZyme/model/model.pth')
    #with open ('/home/smallikao/DeepProZyme/model.pkl', 'rb') as f:
        #model = pickle.load(f)
    model = model.to(device)
    explainECs = model.explainECs
    pred_thrd = model.thresholds
    
    input_seqs, input_ids = read_EC_actual_Fasta(input_data_file)
    id2ind = {seq_id: i for i, seq_id in enumerate(input_ids)}
    pseudo_labels = np.zeros((len(input_seqs)))

    proteinDataset = DeepECDataset(data_X=input_seqs, data_Y=pseudo_labels, explainECs=explainECs, pred=True)
    proteinDataloader = DataLoader(proteinDataset, batch_size=batch_size, shuffle=False)

    y_pred, y_score = run_neural_net(model, proteinDataloader, pred_thrd, device=device)
    failed_cases = save_dl_result(y_pred, y_score, input_ids, explainECs, output_dir+'/tmp')

    if len(failed_cases) > 0:
        blastp_input = f'{output_dir}/tmp/temp_seq.fa'
        blastp_tmp_output = f'{output_dir}/tmp/blast_tmp_result.txt'
        blastp_output = f'{output_dir}/tmp/blast_result.txt'

        with open(blastp_input, 'w') as fp:
            for seq_id in failed_cases:
                idx = id2ind[seq_id]
                seq = input_seqs[idx]
                fp.write(f'>{seq_id}\n{seq}\n')

        run_blastp(blastp_input, blastp_tmp_output, '/home/smallikao/DeepProZyme/model/swissprot_enzyme_diamond', threads=num_cpu)
        blastp_pred = read_best_blast_result(blastp_tmp_output)
        
        with open(blastp_output, 'w') as fp:
            fp.write('sequence_ID\tprediction\n')
            for seq_id in blastp_pred:
                ec = blastp_pred[seq_id][0]
                fp.write(f'{seq_id}\t{ec}\n')

        merge_predictions(f'{output_dir}/tmp/DL_prediction_result.txt', blastp_output, output_dir)
    
    else:
        shutil.copy(output_dir+'/tmp/DL_prediction_result.txt', output_dir)
        os.rename(output_dir+'/DL_prediction_result.txt', output_dir+'/DeepECv2_result.txt')
