import subprocess
import time
import os

# 設定 IPMI 參數
log_dir = "/home/Scott.PY/Check_info"

# 確保日誌目錄存在
os.makedirs(log_dir, exist_ok=True)

# 執行 DC cycle 命令
def dc_cycle(cycle_number):
    # DC cycle 命令
    command = [
        "ipmitool",
        "-I", "lanplus",  # 這一行可以根據你的環境修改為其他適合的選項
        "power", "cycle"
    ]

    try:
        # 執行 DC cycle 命令並捕獲輸出
        result = subprocess.run(command, capture_output=True, text=True)
        # 紀錄日誌
        with open(os.path.join(log_dir, "dc_cycle.log"), 'a') as log_file:
            log_file.write(f"DC Cycle #{cycle_number}:\n")
            log_file.write(f"Command output:\n{result.stdout}\n")
            log_file.write(f"Error (if any):\n{result.stderr}\n")
            log_file.write(f"Command executed: {' '.join(command)}\n")
            log_file.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # 抓取額外資訊
        capture_info(cycle_number)

        # 等待 180 秒
        time.sleep(180)

    except Exception as e:
        with open(os.path.join(log_dir, "dc_cycle.log"), 'a') as log_file:
            log_file.write(f"An error occurred: {str(e)}\n")

def capture_info(cycle_number):
    # 抓取 SDR
    sdr_output = subprocess.run(["ipmitool", "sdr"], capture_output=True, text=True).stdout
    with open(os.path.join(log_dir, f"SDR/sdr_cycle_{cycle_number}.log"), 'w') as sdr_log:
        sdr_log.write(sdr_output)

    # 抓取 SEL
    sel_output = subprocess.run(["ipmitool", "sel"], capture_output=True, text=True).stdout
    with open(os.path.join(log_dir, f"SEL/sel_cycle_{cycle_number}.log"), 'w') as sel_log:
        sel_log.write(sel_output)

    # 抓取 PCIe info
    pcie_output = subprocess.run(["lspci"], capture_output=True, text=True).stdout
    with open(os.path.join(log_dir, f"PCIe_info/pcie_cycle_{cycle_number}.log"), 'w') as pcie_log:
        pcie_log.write(pcie_output)

    # 抓取 MC info
    mc_info_output = subprocess.run(["ipmitool", "mc", "info"], capture_output=True, text=True).stdout
    with open(os.path.join(log_dir, f"MC_info/mc_info_cycle_{cycle_number}.log"), 'w') as mc_log:
        mc_log.write(mc_info_output)

    # 抓取 DMI 資訊
    dmidecode_output = subprocess.run(["sudo", "dmidecode"], capture_output=True, text=True).stdout
    with open(os.path.join(log_dir, f"DMI/dmidecode_cycle_{cycle_number}.log"), 'w') as dmi_log:
        dmi_log.write(dmidecode_output)

if __name__ == "__main__":
    # 確保子資料夾存在
    os.makedirs(os.path.join(log_dir, "SDR"), exist_ok=True)
    os.makedirs(os.path.join(log_dir, "SEL"), exist_ok=True)
    os.makedirs(os.path.join(log_dir, "PCIe_info"), exist_ok=True)
    os.makedirs(os.path.join(log_dir, "MC_info"), exist_ok=True)
    os.makedirs(os.path.join(log_dir, "DMI"), exist_ok=True)

    for i in range(1, 101):  # 執行 100 次 DC cycle
        dc_cycle(i)
