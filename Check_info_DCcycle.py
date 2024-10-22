import os
import subprocess
import time

# 設定主資料夾路徑
main_log_dir = "/home/Scott.PY/Check_info_DCcycle"  

# 子資料夾名稱
subfolders = ["SEL_VVV", "SEL", "DMI", "PCIe_info", "FRU_info", "SDR_info"]

# 確保主資料夾和子資料夾存在
os.makedirs(main_log_dir, exist_ok=True)

for subfolder in subfolders:
    folder_path = os.path.join(main_log_dir, subfolder)
    os.makedirs(folder_path, exist_ok=True)

    # 獲取目前的日誌編號
    log_files = [f for f in os.listdir(folder_path) if f.startswith("log-")]
    log_number = len(log_files) + 1

    # 抓取 SEL -vvv
    if subfolder == "SEL_VVV":
        sel_vvv_output = subprocess.run(["ipmitool", "sel", "-vvv"], capture_output=True, text=True).stdout
        with open(os.path.join(folder_path, f"log-{log_number}.txt"), 'w') as log_file:
            log_file.write(sel_vvv_output)

    # 抓取 SEL
    elif subfolder == "SEL":
        sel_output = subprocess.run(["ipmitool", "sel"], capture_output=True, text=True).stdout
        with open(os.path.join(folder_path, f"log-{log_number}.txt"), 'w') as log_file:
            log_file.write(sel_output)

    # 抓取 DMI 資訊
    elif subfolder == "DMI":
        dmidecode_output = subprocess.run(["sudo", "dmidecode"], capture_output=True, text=True).stdout
        with open(os.path.join(folder_path, f"log-{log_number}.txt"), 'w') as log_file:
            log_file.write(dmidecode_output)

    # 抓取 PCIe 資訊
    elif subfolder == "PCIe_info":
        pcie_output = subprocess.run(["lspci"], capture_output=True, text=True).stdout
        with open(os.path.join(folder_path, f"log-{log_number}.txt"), 'w') as log_file:
            log_file.write(pcie_output)

    # 抓取 FRU 資訊
    elif subfolder == "FRU_info":
        fru_output = subprocess.run(["ipmitool", "fru"], capture_output=True, text=True).stdout
        with open(os.path.join(folder_path, f"log-{log_number}.txt"), 'w') as log_file:
            log_file.write(fru_output)

    # 抓取 SDR 資訊
    elif subfolder == "SDR_info":
        sdr_output = subprocess.run(["ipmitool", "sdr", "elist"], capture_output=True, text=True).stdout
        with open(os.path.join(folder_path, f"log-{log_number}.txt"), 'w') as log_file:
            log_file.write(sdr_output)

print("Log files created successfully.")
