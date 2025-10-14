import os
from pathlib import Path
import json
target_directory = os.path.join('files_to_server', 'dataset')

root = Path(target_directory)
datainfos = {}
for subdir in [p for p in root.iterdir() if p.is_dir()]:
    files = [f for f in subdir.iterdir() if f.is_file()]
    name = str(subdir).split('/')[-1]
    datainfos[name] = []
    for f in files:
        datainfos[name].append(f.name)

# build the datasetinfo based on the dictionary
final_result = {}
for k, vs in datainfos.items():
    for v in vs:
        final_result[f"{k}_{v.split(".")[0]}"] = {
            "file_name": f"{k}/{v}",
            "formatting": "alpaca"
        }

# write the json file
with open(os.path.join(target_directory, "dataset_info.json"), "w+", encoding="utf-8") as f:
    json.dump(final_result, f, ensure_ascii=False, indent=2)