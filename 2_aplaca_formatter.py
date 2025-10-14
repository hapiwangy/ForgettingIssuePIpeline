'''
    convert the file in the dataset into aplaca format
'''


import os
import pandas as pd

SRC_ROOT = "dataset"
OUT_ROOT = "files_to_server/dataset"

dataset_names = []
for root, dirs, files in os.walk(SRC_ROOT):
    if root == SRC_ROOT:
        dataset_names.extend(dirs)
        break

# check if the final file exist
os.makedirs(OUT_ROOT, exist_ok=True)

for dn in dataset_names:
    in_dir  = os.path.join(SRC_ROOT, dn)
    out_dir = os.path.join(OUT_ROOT, dn)
    os.makedirs(out_dir, exist_ok=True)

    for split in ("train", "test", "val"):
        csv_path  = os.path.join(in_dir, f"{split}.csv")
        if not os.path.isfile(csv_path):
            continue

        df = pd.read_csv(csv_path)

        out_df = pd.DataFrame({
            "instruction": df["prompt"],
            "input": "",                     
            "output": df["label"]
        })

        jsonl_path = os.path.join(out_dir, f"{split}.jsonl")
        out_df.to_json(
            jsonl_path,
            orient="records",
            lines=True,
            force_ascii=False
        )

print(f"transfer {",".join(dataset_names)} into aplaca format.")
