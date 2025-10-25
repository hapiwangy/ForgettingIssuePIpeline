import os
import posixpath as pp
import itertools
SRC_ROOT = "dataset"
OUT_ROOT = pp.join("files_to_server", "dataset")

org_dataset = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        org_dataset.extend(dirs)
        break

jobs_prompt = ""
with open(pp.join('config', 'job.txt'), "r", encoding="utf-8") as fp:
    jobs_prompt = fp.read()

pair_list = list(itertools.permutations(org_dataset, 2))
# infer_outputs/fir_on_allenai-art_cti-mcq 
running_template = """\
python -u scripts/vllm_infer.py \
  --model_name_or_path {model_path} \
  --template llama3 \
  --dataset_dir dataset \
  --dataset {basedataset}_test \
  --max_new_tokens 512 \
  --per_device_eval_batch_size 8 \
  --do_sample false \
  --bf16 true \
  --repetition_penalty 1.0 \
  --seed 42 \
  --save_name infer_outputs/{basedataset}/{modelpath}/generations.jsonl \
  --output_dir infer_outputs/{basedataset}/{modelpath} \
  --overwrite_output_dir true \
  --report_to none \
  --temperature 0  \
  --do_sample false
"""

last_pair = None  # 保留最後一次迭代到的 pair（等同於原本在 for 外使用 pair[0]/pair[1] 的效果）
for dataset in org_dataset:
    current_path = pp.join(OUT_ROOT, dataset)  # target dataset（未更動邏輯，即使此變數未直接使用）

    querylist = ""
    # first do the zeroshot
    querylist += f"mkdir -p infer_outputs/{dataset}/zero-shot\n{running_template.format(
        model_path = "meta-llama/Llama-3.2-1B-Instruct",
        modelpath = 'zero-shot',
        basedataset = dataset
    )}"
    querylist += f"mkdir -p infer_outputs/{dataset}/fir_on_{dataset}\n{running_template.format(
        model_path = f"output/fir_on_{dataset}",
        modelpath = f"fir_on_{dataset}",
        basedataset = dataset
    )}"
    for pair in pair_list:
        if pair[0] == dataset:
            last_pair = pair
            target = pair[1]


            querylist += f"mkdir -p infer_outputs/{dataset}/fir_on_{dataset}_{target}\n{running_template.format(
                model_path = f"output/fir_on_{dataset}_{target}",
                basedataset = dataset,
                modelpath = f"fir_on_{dataset}_{target}"
            )}"
            querylist += f"mkdir -p infer_outputs/{dataset}/fir_on_{dataset}_{target}1percent{dataset}\n{running_template.format(
                model_path = f"output/fir_on_{dataset}_{target}1percent{dataset}",
                basedataset = dataset,
                modelpath = f"fir_on_{dataset}_{target}1percent{dataset}"
            )}"
    with open(pp.join(OUT_ROOT, 'jobs', f"2_inference_{dataset}.job"), "w+", newline='\n', encoding="utf-8") as fp:
        fp.write(jobs_prompt.format(
            dataset = dataset,
            state = "infer",
            querylists = querylist
        ))


