'''
    Args:
        --datadirectory: str // where the datasetA and datasetB is put at
        --datasetA: str
        --datasetB: str
        --percent: int
        --outpath: str
    adding x percent of datasetA into datasetB > output the datasetAxpercentdatasetB/train.csv // usually be used in the train.csv only
    example script
        python helper_combinexpercent.py --datadirectory "dataset" --from_dataset cti-mcq --to_dataset sentiment-reasoning --percent 1
'''

import os
import json
import random
import argparse
parser = argparse.ArgumentParser(description="combine tow dataset")
parser.add_argument("--datadirectory")
parser.add_argument("--from_dataset")
parser.add_argument("--to_dataset")
parser.add_argument("--percent")
args = parser.parse_args()
# mock the datadictory, dataseta, datasetb , x percent and output directory_path
datadirectory = args.datadirectory
from_dataset = args.from_dataset
to_dataset = args.to_dataset
percent = args.percent
output_directory_path = os.path.join("files_to_server", datadirectory)

def read_data(root_path, source_file):
    '''
        read path and return the files in it 
    '''
    with open(os.path.join(root_path, source_file, "train.jsonl"), "r", encoding="utf-8") as fp:
        data = [json.loads(line) for line in fp]
    return data
# read data``
from_dataset_data = read_data(output_directory_path, from_dataset)
to_dataset_data = read_data(output_directory_path, to_dataset)
# sample data
sample_size = max(1, int((int(percent) / 100) * len(from_dataset_data)))
sample_data = random.sample(from_dataset_data, sample_size)
merged_data = to_dataset_data + sample_data
# shuffle data
random.shuffle(merged_data)
# build the directory
newsetname = f"{to_dataset}{percent}percent{from_dataset}"
os.makedirs(os.path.join(output_directory_path, newsetname), exist_ok=True)

with open(os.path.join(output_directory_path, newsetname, "train.jsonl"), "w+", encoding="utf-8") as fp:
    for element in merged_data:
        fp.write(json.dumps(element, ensure_ascii=True) + "\n")

print(f"✅ 已從 {from_dataset} 隨機抽取 {sample_size} 筆資料，合併到 {to_dataset}。")
print(f"📊 原始資料數：{len(to_dataset_data)}，合併後總數：{len(merged_data)}")