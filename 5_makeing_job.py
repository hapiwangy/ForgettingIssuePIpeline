'''
    in this file we make the .job files for each files.
'''
import os

SRC_ROOT = "dataset"
OUT_ROOT = "files_to_server/dataset"

dataset_names = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        dataset_names.extend(dirs)
        break

with open(os.path.join('config', 'job.txt'), "r") as f:
    jobtemplate = f.read()
for dn in dataset_names:
    with open(os.path.join('files_to_server', 'dataset', dn, f"happy_{dn}.job"), "w+") as fp:
        fp.write(jobtemplate.format(dataset=dn))