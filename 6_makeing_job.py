'''
    in this file we make the .job files for each files.
'''
import os

SRC_ROOT = "dataset"
OUT_ROOT = "files_to_server/dataset"
import itertools
dataset_names = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        dataset_names.extend(dirs)
        break

with open(os.path.join('config', 'job.txt'), 'r', encoding='utf-8', newline='') as f:
    jobtemplate = f.read().replace('\r\n', '\n').replace('\r', '\n')
pair_list = list(itertools.permutations(dataset_names, 2))
for pair in pair_list:
    with open(os.path.join('files_to_server', 'dataset', pair[0], f"happy_{pair[0]}_{pair[1]}.job"), "w+", encoding="utf-8", newline='\n' ) as fp:
        fp.write(jobtemplate.format(dataset1=pair[0], dataset2=pair[1]))