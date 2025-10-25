#!/usr/bin/env bash
set -euo pipefail

# ---- robust bash script for Windows Git Bash / PowerShell ----
# 1) 總是先切到腳本所在目錄（避免空白路徑踩雷）
cd "$(dirname -- "${BASH_SOURCE[0]}")"

# 2) 初始化 conda（兩條路：有 conda 指令就用 hook；否則明確 source conda.sh）
if command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
else
  # 依你的安裝目錄調整（常見是 /d/anaconda3）
  source "/d/anaconda3/etc/profile.d/conda.sh"
fi

# 3) 啟用環境（換成你的環境名）
ENV_NAME="llamatest"
# 若環境不存在就明確報錯
conda env list | awk '{print $1}' | grep -qx "$ENV_NAME" || {
  echo "ERROR: conda env '$ENV_NAME' 不存在。請先建立：conda create -n $ENV_NAME python=3.11 -y"
  exit 1
}
conda activate "$ENV_NAME"

# 4) 基本診斷資訊
python -V
which python || true
echo "PWD=$(pwd)"

# 5) 確保副腳本有可執行權限且是 Unix 換行
#    （若沒有 dos2unix 可改用 sed）
chmod +x 3_help_script.sh || true
# dos2unix 3_help_script.sh 2>/dev/null || sed -i 's/\r$//' 3_help_script.sh

# 6) 依序執行（-u：即時輸出；所有相對路徑都以此目錄為基準）
python -u "2_aplaca_formatter.py"
python -u "3_1_make_helperscript.py"
bash       "./3_help_script.sh"
python -u "4_dataset_info.py"
python -u "5_finetune_config_maker.py"
python -u "6_inference_config_maker.py"

echo "✅ flow.sh 完成。"
