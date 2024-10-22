import os
import subprocess
import logging
import argparse
from datetime import datetime

# 設定日誌
logging.basicConfig(
    filename='/home/Scott.PY/cycle_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 參數解析
parser = argparse.ArgumentParser(description='Cycle test automation script.')
parser.add_argument('--commands', nargs='*', help='Commands to execute (e.g., sdr sel).', default=[])
args = parser.parse_args()

# 設定父目錄路徑
parent_dir = r"/home/Scott.PY/Check_info_log"
diff_dir = os.path.join(parent_dir, "different")

# 確保父目錄存在
try:
    os.makedirs(parent_dir, exist_ok=True)
    os.makedirs(diff_dir, exist_ok=True)
except Exception as e:
    logging.error(f"Failed to create directories: {e}")
    exit(1)  # 停止腳本執行

# 子目錄列表
subdirs = ["sdr", "sel", "sel-vvv", "fru", "pcie_info", "mc_info", "dmidecode"]

# 創建子目錄
for subdir in subdirs:
    os.makedirs(os.path.join(parent_dir, subdir), exist_ok=True)

# 讀取當前的 cycle 數量，或設置為 0
count_file_path = os.path.join(parent_dir, "count.txt")
cycle_count = 0
if os.path.exists(count_file_path):
    with open(count_file_path, 'r') as count_file:
        try:
            cycle_count = int(count_file.read().strip())
        except ValueError:
            logging.error("Invalid cycle count in count.txt. Resetting to 0.")
            cycle_count = 0

# 更新 cycle 數量
cycle_count += 1
with open(count_file_path, 'w') as count_file:
    count_file.write(str(cycle_count))

# 獲取當前日期
current_date = datetime.now().strftime("%Y-%m-%d")

def write_log(log_file_path, content):
    """寫入日誌文件"""
    with open(log_file_path, 'w') as log_file:
        log_file.write(content)

# 執行命令並將輸出記錄到對應的 log 檔案
def execute_command(command, subdir_name):
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        log_file_path = os.path.join(parent_dir, subdir_name, f"log-{current_date}-cycle-{cycle_count}.txt")
        write_log(log_file_path, output.stdout + output.stderr)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed with error: {e}")
        with open(os.path.join(parent_dir, 'error.log'), 'a') as error_file:
            error_file.write(f"Cycle {cycle_count} - Command: {' '.join(command)} - Error: {e}\n")

# 比較日誌文件
def compare_logs(subdir_name):
    first_cycle_log_path = os.path.join(parent_dir, subdir_name, f"log-{current_date}-cycle-1.txt")
    current_cycle_log_path = os.path.join(parent_dir, subdir_name, f"log-{current_date}-cycle-{cycle_count}.txt")
    
    if os.path.exists(first_cycle_log_path) and os.path.exists(current_cycle_log_path):
        with open(first_cycle_log_path, 'r') as first_file, open(current_cycle_log_path, 'r') as current_file:
            first_lines = set(first_file.readlines())
            current_lines = set(current_file.readlines())
        
        differences = current_lines.difference(first_lines)
        
        if differences:
            diff_log_path = os.path.join(diff_dir, f"difference-{subdir_name}-cycle-{cycle_count}.txt")
            write_log(diff_log_path, ''.join(differences))

# 定義命令映射
commands = {
    "sdr": ["ipmitool", "sdr"],
    "sel": ["ipmitool", "sel"],
    "sel-vvv": ["ipmitool", "sel", "-vvv"],
    "fru": ["ipmitool", "fru"],
    "pcie_info": ["lspci"],
    "mc_info": ["ipmitool", "mc", "info"],
    "dmidecode": ["sudo", "dmidecode"]
}

# 逐個執行命令
for subdir in subdirs:
    if subdir in commands and (not args.commands or subdir in args.commands):
        execute_command(commands[subdir], subdir)
        if cycle_count > 1:
            compare_logs(subdir)

logging.info(f"Cycle {cycle_count} completed on {current_date} and logs are stored in {parent_dir}.")

print("Log file created successfully.")