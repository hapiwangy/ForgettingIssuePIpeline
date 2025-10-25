import os
import posixpath as pp
import itertools

SRC_ROOT = "dataset"
OUT_ROOT = pp.join("files_to_server", "dataset")

os.makedirs(pp.join(OUT_ROOT, 'jobs'), exist_ok=True)

train_prompt = ""
with open(pp.join('config', 'train.txt'), "r", encoding="utf-8") as fp:
    train_prompt = fp.read()

def make_train_yaml(base_dataset, base_model, train_dataset, val_dataset, output_model):
    yaml_path = pp.join(OUT_ROOT, base_dataset, f'train_{output_model}.yaml')
    with open(yaml_path, "w+", encoding="utf-8", newline="\n") as fp:
        fp.write(
            train_prompt.format(
                base_model=base_model,
                train_dataset=train_dataset,
                val_dataset=val_dataset,
                output_model=pp.join('output', output_model),
            )
        )
    return pp.join('dataset', base_dataset, f'train_{output_model}.yaml')

jobs_prompt = ""
with open(pp.join('config', 'job.txt'), "r", encoding="utf-8") as fp:
    jobs_prompt = fp.read()

org_dataset = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        org_dataset.extend(dirs)
        break

pair_list = list(itertools.permutations(org_dataset, 2))

last_pair = None  # 保留最後一次迭代到的 pair（等同於原本在 for 外使用 pair[0]/pair[1] 的效果）
for dataset in org_dataset:
    current_path = pp.join(OUT_ROOT, dataset)  # target dataset（未更動邏輯，即使此變數未直接使用）

    querylists = ""

    # finetune the first dataset
    first_output = f"fir_on_{dataset}"
    yaml1 = make_train_yaml(dataset, 'meta-llama/Llama-3.2-1B-Instruct', dataset, dataset, first_output)
    querylists += f"FORCE_TORCHRUN=1 lmf train {yaml1}\n"

    for pair in pair_list:
        if pair[0] == dataset:
            last_pair = pair
            target = pair[1]

            # 第二階段的 base model 放在 output/ 下
            base_after_first = pp.join('output', first_output)

            # train on no 1 % and 1 % dataset
            yaml2 = make_train_yaml(dataset, base_after_first, f"{target}", target, f"fir_on_{dataset}_{target}")
            querylists += f"FORCE_TORCHRUN=1 lmf train {yaml2}\n"

            yaml3 = make_train_yaml(
                dataset,
                base_after_first,
                f"{target}1percent{dataset}",
                target,
                f"fir_on_{dataset}_{target}1percent{dataset}",
            )
            querylists += f"FORCE_TORCHRUN=1 lmf train {yaml3}\n"

    # 將 querylists 寫入對應的 job 檔
    job_path = pp.join('files_to_server', 'dataset', 'jobs', f'1_traing_{dataset}.job')

    with open(job_path, "w+", encoding="utf-8", newline="\n") as fp:
        fp.write(jobs_prompt.format(querylists=querylists, dataset=dataset, state='train'))
