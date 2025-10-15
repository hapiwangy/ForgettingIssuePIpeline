'''
    we read the datasetname in dataset and update the help_script
    the number of lines in the helpr_script should be (# of dataset) * (# of dataset - 1)
'''

import os
import itertools
SRC_ROOT = "dataset"
OUT_ROOT = "files_to_server/dataset"
template = "python helper_combinexpercent.py --datadirectory \"dataset\" --from_dataset {fromdataset} --to_dataset {todataset} --percent {percent}"
dataset_names = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        dataset_names.extend(dirs)
        break

pair_list = list(itertools.permutations(dataset_names, 2))
final_words = ""
for pair in pair_list:
    final_words += f"{template.format(fromdataset=pair[0], todataset=pair[1], percent=1)}\n"
with open("3_help_script.sh", "w+") as fp:
    fp.write(final_words)