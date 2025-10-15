#!/usr/bin/env bash
set -euo pipefail

# 讓 conda 在非互動式腳本可用
eval "$(conda shell.bash hook)"
conda activate llamatest

python 2_aplaca_formatter.py
python 3_1_make_helperscript.py
bash 3_help_script.sh
python 4_dataset_info.py
python 5_1_trainconfigmaker.py
bash 5_train_config.sh
python 6_makeing_job.py
python 7_sbatch_formatter.py