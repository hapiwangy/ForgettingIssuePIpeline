'''
here we only need to check the script is contain Combination (number of dataset, 2)
'''
import os
import pandas as pd
import itertools
SRC_ROOT = "dataset"
OUT_ROOT = "files_to_server/dataset"
template = "python helper_configcreater.py --dataset1 {dataset1} --dataset2 {dataset2} --percent {percent}"
dataset_names = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        dataset_names.extend(dirs)
        break
pair_list = list(itertools.combinations(dataset_names, 2))    
final_words = ""
for pair in pair_list:
    final_words += f"{template.format(dataset1=pair[0], dataset2=pair[1], percent=1)}\n"
with open('5_train_config.sh', 'w+') as fp:
    fp.write(final_words)