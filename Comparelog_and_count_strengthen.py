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
parser.add_argument('--commands', nargs='*', help='Commands to execute (e.g., sdr sel).')
args = parser.parse_args()

# 設定父目錄路徑
parent_dir = r"/home/Scott.PY/Check_info_log"
diff_dir = os.path.join(parent_dir, "different")

# 確保父目錄存在
os.makedirs(parent_dir, exist_ok=True)
os.makedirs(diff_dir, exist_ok=True)

# 子目錄列表
subdirs = ["sdr", "sel", "sel-vvv", "fru", "pcie info", "mc info", "dmidecode"]

# 創建子目錄
for subdir in subdirs:
    os.makedirs(os.path.join(parent_dir, subdir), exist_ok=True)

# 讀取當前的 cycle 數量，或設置為 0
count_file_path = os.path.join(parent_dir, "count.txt")
if os.path.exists(count_file_path):
    with open(count_file_path, 'r') as count_file:
        cycle_count = int(count_file.read().strip())
else:
    cycle_count = 0

# 更新 cycle 數量
cycle_count += 1
with open(count_file_path, 'w') as count_file:
    count_file.write(str(cycle_count))

# 獲取當前日期
current_date = datetime.now().strftime("%Y-%m-%d")

# 執行命令並將輸出記錄到對應的 log 檔案
def execute_command(command, subdir_name):
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        log_file_path = os.path.join(parent_dir, subdir_name, f"log-{current_date}-cycle-{cycle_count}.txt")
        
        with open(log_file_path, 'w') as log_file:
            log_file.write(output.stdout)
            log_file.write(output.stderr)

    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed with error: {e}")
        with open(os.path.join(parent_dir, 'error.log'), 'a') as error_file:
            error_file.write(f"Cycle {cycle_count} - Command: {' '.join(command)} - Error: {e}\n")

# 比較日誌文件
def compare_logs(subdir_name):
    first_cycle_log_path = os.path.join(parent_dir, subdir_name, "log-{}-cycle-1.txt".format(current_date))
    current_cycle_log_path = os.path.join(parent_dir, subdir_name, f"log-{current_date}-cycle-{cycle_count}.txt")
    
    if os.path.exists(first_cycle_log_path) and os.path.exists(current_cycle_log_path):
        with open(first_cycle_log_path, 'r') as first_file, open(current_cycle_log_path, 'r') as current_file:
            first_lines = set(first_file.readlines())
            current_lines = set(current_file.readlines())
        
        differences = current_lines.difference(first_lines)
        
        if differences:
            diff_log_path = os.path.join(diff_dir, f"difference-{subdir_name}-cycle-{cycle_count}.txt")
            with open(diff_log_path, 'w') as diff_file:
                diff_file.writelines(differences)

# 執行對應的命令
commands = {
    "sdr": ["ipmitool", "sdr"],
    "sel": ["ipmitool", "sel"],
    "sel-vvv": ["ipmitool", "sel", "-vvv"],
    "fru": ["ipmitool", "fru"],
    "pcie info": ["lspci"],
    "mc info": ["ipmitool", "mc", "info"],
    "dmidecode": ["dmidecode"]
}

# 逐個執行命令
for subdir in subdirs:
    if subdir in commands and (args.commands is None or subdir in args.commands):
        execute_command(commands[subdir], subdir)
        if cycle_count > 1:
            compare_logs(subdir)

logging.info(f"Cycle {cycle_count} completed on {current_date} and logs are stored in {parent_dir}.")

###主要功能###
設定日誌
python
Copy code
logging.basicConfig(
    filename='/home/Scott.PY/cycle_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
這段代碼設定了日誌的基本配置：

filename：指定日誌文件的存儲位置。
level：設置日誌記錄的嚴重性級別，這裡設置為 INFO，表示記錄信息性消息及以上級別的訊息（如錯誤和警告）。
format：設置日誌消息的格式，包含時間戳、日誌級別和消息內容。
2. 參數解析
python
Copy code
parser = argparse.ArgumentParser(description='Cycle test automation script.')
parser.add_argument('--commands', nargs='*', help='Commands to execute (e.g., sdr sel).')
args = parser.parse_args()
argparse 模組用於解析命令行參數，這樣用戶可以在執行腳本時指定要執行的命令。
nargs='*' 允許用戶輸入零個或多個命令，這些命令將作為列表存儲在 args.commands 中。
3. 目錄管理
python
Copy code
parent_dir = r"/home/Scott.PY/Check_info_log"
diff_dir = os.path.join(parent_dir, "different")

os.makedirs(parent_dir, exist_ok=True)
os.makedirs(diff_dir, exist_ok=True)
parent_dir：指定父目錄的路徑，用於存放所有日誌文件。
diff_dir：指定差異日誌目錄的路徑，用於存放日誌比較的結果。
os.makedirs：確保父目錄和差異目錄存在，如果不存在則自動創建。
4. 創建子目錄
python
Copy code
subdirs = ["sdr", "sel", "sel-vvv", "fru", "pcie info", "mc info", "dmidecode"]

for subdir in subdirs:
    os.makedirs(os.path.join(parent_dir, subdir), exist_ok=True)
定義了需要創建的子目錄名稱，這些子目錄將存放各自命令的日誌文件。
迴圈遍歷子目錄名稱，使用 os.makedirs 創建每個子目錄，exist_ok=True 確保如果目錄已存在則不報錯。
5. 循環計數
python
Copy code
count_file_path = os.path.join(parent_dir, "count.txt")
if os.path.exists(count_file_path):
    with open(count_file_path, 'r') as count_file:
        cycle_count = int(count_file.read().strip())
else:
    cycle_count = 0

cycle_count += 1
with open(count_file_path, 'w') as count_file:
    count_file.write(str(cycle_count))
設定循環計數的文件路徑 count.txt，用於記錄當前的循環次數。
如果文件存在，則讀取當前的循環次數；如果不存在，則初始化為 0。
將循環計數加 1，並將新值寫回 count.txt 文件中，以便下次執行時可以從最新的循環次數開始。
6. 獲取當前日期
python
Copy code
current_date = datetime.now().strftime("%Y-%m-%d")
使用 datetime 模組獲取當前日期，並將其格式化為 YYYY-MM-DD 格式，以便用於日誌文件名稱。
7. 執行命令並記錄
python
Copy code
def execute_command(command, subdir_name):
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        log_file_path = os.path.join(parent_dir, subdir_name, f"log-{current_date}-cycle-{cycle_count}.txt")
        
        with open(log_file_path, 'w') as log_file:
            log_file.write(output.stdout)
            log_file.write(output.stderr)

    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed with error: {e}")
        with open(os.path.join(parent_dir, 'error.log'), 'a') as error_file:
            error_file.write(f"Cycle {cycle_count} - Command: {' '.join(command)} - Error: {e}\n")
execute_command 函數用來執行傳入的命令。
subprocess.run：執行命令並捕獲輸出。如果命令執行成功，將其標準輸出和錯誤輸出寫入日誌文件，日誌文件名中包含當前日期和循環計數。
如果命令執行失敗，則記錄錯誤信息到主日誌文件和錯誤日誌文件。
8. 比較日誌文件
python
Copy code
def compare_logs(subdir_name):
    first_cycle_log_path = os.path.join(parent_dir, subdir_name, "log-{}-cycle-1.txt".format(current_date))
    current_cycle_log_path = os.path.join(parent_dir, subdir_name, f"log-{current_date}-cycle-{cycle_count}.txt")
    
    if os.path.exists(first_cycle_log_path) and os.path.exists(current_cycle_log_path):
        with open(first_cycle_log_path, 'r') as first_file, open(current_cycle_log_path, 'r') as current_file:
            first_lines = set(first_file.readlines())
            current_lines = set(current_file.readlines())
        
        differences = current_lines.difference(first_lines)
        
        if differences:
            diff_log_path = os.path.join(diff_dir, f"difference-{subdir_name}-cycle-{cycle_count}.txt")
            with open(diff_log_path, 'w') as diff_file:
                diff_file.writelines(differences)
compare_logs 函數比較當前循環的日誌文件和第一個循環的日誌文件。
如果兩個日誌文件都存在，則讀取它們的內容並轉換為集合，方便進行差異比較。
使用 set.difference() 方法獲取當前循環日誌中的新行，並將這些差異寫入差異日誌文件中。
9. 執行命令
python
Copy code
commands = {
    "sdr": ["ipmitool", "sdr"],
    "sel": ["ipmitool", "sel"],
    "sel-vvv": ["ipmitool", "sel", "-vvv"],
    "fru": ["ipmitool", "fru"],
    "pcie info": ["lspci"],
    "mc info": ["ipmitool", "mc", "info"],
    "dmidecode": ["dmidecode"]
}

for subdir in subdirs:
    if subdir in commands and (args.commands is None or subdir in args.commands):
        execute_command(commands[subdir], subdir)
        if cycle_count > 1:
            compare_logs(subdir)
定義了一個字典 commands，映射每個子目錄名稱到對應的命令。
逐個遍歷子目錄，如果該子目錄在命令字典中，且用戶未指定命令或指定的命令包含該子目錄，則執行命令。
如果循環次數大於 1，則調用比較函數。
10. 記錄循環完成信息
python
Copy code
logging.info(f"Cycle {cycle_count} completed on {current_date} and logs are stored in {parent_dir}.")
在所有命令執行完畢後，記錄一條信息，表明循環已成功完成，並指明日誌存儲的目錄。
