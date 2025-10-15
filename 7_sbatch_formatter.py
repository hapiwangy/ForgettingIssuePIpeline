import os

SRC_ROOT = "dataset"
OUT_ROOT = "files_to_server/dataset"
import itertools
template = "sbatch dataset/{dataset1}/happy_{dataset1}_{dataset2}.job"
dataset_names = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        dataset_names.extend(dirs)
        break
pair_list = list(itertools.permutations(dataset_names, 2))    
final_word = "mkdir -p \"ft_logs\"\n"
for pair in pair_list:
    final_word += f"{template.format(dataset1=pair[0], dataset2=pair[1])}\n"
with open(os.path.join(OUT_ROOT, 'happy_jobs.sh'), "w+", encoding="utf-8", newline='\n') as fp:
    fp.write(final_word)
