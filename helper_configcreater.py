'''
    getting two dataset from the cmd line prompt, and produce both config file for finetuning for each training sets.    
    Args:
        --dataset1: str
        --dataset2: str
    exlpanation:
        we need to produce six file with every dataset we input in the comand line prompt
        dataset_config1:
            - input: base model
            - output: output/finetune_dataset1
        dataset_config2:
            - input: output/finetune_dataset1
            - output: output/finetune_dataset1_dataset2
        dataset_config3:
            - input: output/finetune_dataset1
            - output: output/finetune_dataset1_dataset2x%dataset1
    example:
        python 4_train_configcreater.py --dataset1 --dataset2 --percent
'''


import argparse
import os

parser = argparse.ArgumentParser(description="produce the training config between two dataset")
parser.add_argument('--dataset1')
parser.add_argument('--dataset2')
parser.add_argument('--percent')
args = parser.parse_args()

dataset1 = args.dataset1
dataset2 = args.dataset2
percent = args.percent

with open(os.path.join('config', 'train.txt'), "r", encoding="utf-8") as f:
    config_template = f.read()

with open(os.path.join('config', 'eval.txt'), 'r', encoding="utf-8") as f:
    eval_template = f.read()

## 原本只有兩個dataset所以不用紀錄用哪個來做test，現在多一個就要了
def create_files(base_dataset, second_dataset, percent):
    # record use which two dataset to finetune
    which_two_set = f"use_{base_dataset}_and_{second_dataset}"
    # config1.yaml > use base_dataset to do the finetune on the base model
    with open(os.path.join('files_to_server', 'dataset', f"{base_dataset}" ,f"{base_dataset}_{which_two_set}_config1.yaml"), "w+") as fp:
        fp.write(config_template.format(
            base_model = 'meta-llama/Llama-3.2-1B-Instruct',
            train_dataset = base_dataset,
            val_dataset = base_dataset,
            output_model = f'output/{which_two_set}_{base_dataset}'
        ))
    
    # config2.yaml > use result on first dataset and finetune on second dataset
    with open(os.path.join('files_to_server', 'dataset', f"{base_dataset}", f"{base_dataset}_{which_two_set}_config2.yaml"), "w+") as fp:
        fp.write(config_template.format(
            base_model = f'output/{which_two_set}_{base_dataset}',
            train_dataset = second_dataset,
            val_dataset = second_dataset,
            output_model = f'output/{which_two_set}_{base_dataset}_{second_dataset}'
        ))
    # config3.yaml > use result on first dataset and train on thrid dataset, but eval on second dataset
    with open(os.path.join('files_to_server', 'dataset', f"{base_dataset}", f"{base_dataset}_{which_two_set}_config3.yaml"), "w+") as fp:
        fp.write(config_template.format(
            base_model = f'output/{which_two_set}_{base_dataset}',
            train_dataset = f"{second_dataset}{percent}percent{base_dataset}",
            val_dataset = second_dataset,
            output_model = f'output/{which_two_set}_{base_dataset}_{second_dataset}{percent}percent{base_dataset}'
        ))
    # use eval on first dataset on different model
    ## result for zero shot is make from other files(if needed)
    with open(os.path.join('files_to_server', 'dataset', f"{base_dataset}", f'{base_dataset}_{which_two_set}_inference1.yaml'), "w+") as fp:
        fp.write(eval_template.format(
            eval_model = f'output/{which_two_set}_{base_dataset}',
            dataset1 = base_dataset,
            output_dir = f'infer_outputs/{which_two_set}_{base_dataset}_finetune1'
        ))
    with open(os.path.join('files_to_server', 'dataset', f"{base_dataset}", f'{base_dataset}_{which_two_set}_inference2.yaml'), "w+") as fp:
        fp.write(eval_template.format(
            eval_model = f'output/{which_two_set}_{base_dataset}_{second_dataset}',
            dataset1 = base_dataset,
            output_dir = f'infer_outputs/{which_two_set}_{base_dataset}_{second_dataset}_finetune2'
        ))
    with open(os.path.join('files_to_server', 'dataset', f"{base_dataset}", f'{base_dataset}_{which_two_set}_inference3.yaml'), "w+") as fp:
        fp.write(eval_template.format(
            eval_model = f'output/{which_two_set}_{base_dataset}_{second_dataset}{percent}percent{base_dataset}',
            dataset1 = base_dataset,
            output_dir = f'infer_outputs/{which_two_set}_{base_dataset}_{second_dataset}{percent}percent{base_dataset}_finetune3'
        ))
create_files(dataset1, dataset2, percent)
create_files(dataset2, dataset1, percent)
