# Automation_Script

### [README_English_version](README_en.md)

## 簡介 

這個 repo 是我在工作中經常使用的各類自動化腳本的合集，主要針對伺服器管理和系統運維場景。隨著 IT 基礎設施日益複雜，利用自動化工具不僅能有效提升工作效率，還能減少潛在的人為錯誤，並確保系統操作的一致性。無論你是管理數百台伺服器的系統管理員，還是處理日常維護的技術人員，本 repository 內的工具都能助你一臂之力！💡

## 背景
在現代企業中，無論是大規模的數據中心還是分佈式伺服器管理，自動化的腳本都是至關重要的技術工具。手動操作可能容易出錯，尤其是在進行批量操作時，任何小錯誤都可能導致系統不穩定或宕機。因此，這些腳本旨在幫助技術人員簡化常見的任務，包括伺服器的遠程管理、監控和日常系統維護等。

本 repository 涵蓋了 IPMI OOB 和 inband 操作腳本、Python 和 Shell 腳本，它們能夠解決日常工作中的許多挑戰，並在自動化過程中提供靈活性與可擴展性。

## 包含內容
### IPMI OOB 自動化腳本
IPMI OOB (Out-Of-Band) 自動化腳本專門針對伺服器的遠程管理，即使在操作系統宕機或無法連接的情況下，仍然可以對伺服器進行遠程操控。這些腳本允許我們進行諸如伺服器重啟、硬體健康狀態檢查及診斷等操作，非常適合用於緊急狀況下的維護工作。

功能亮點：
- 遠程伺服器電源管理 
- 伺服器重啟和關機命令 
- 硬體監控（溫度、風扇、電壓等） 

### IPMI IB 自動化腳本
這類腳本通過伺服器的內部網絡接口進行操作，適合在伺服器系統運行良好時進行的管理和維護操作。相比 OOB 操作，inband 管理可以進行更細緻的操作，如檢查伺服器的日誌、更新 BIOS、管理伺服器組態等。

功能亮點：
- 日常健康檢查 
- 更新系統 BIOS 或固件 
- 系統性能監控和報告 

### Python 腳本
Python 作為強大的自動化和系統集成工具，提供了靈活性和可擴展性，這些腳本能夠幫助我們快速完成如 API 調用、自動化報告生成、數據處理等任務。Python 腳本設計簡單，易於修改，可以根據需求快速進行擴展，並且能與其他工具無縫集成。

功能亮點：
- 自動化 API 調用 
- 報告生成 
- 數據分析工具 

### Shell 腳本
Shell scripts 是系統管理中必不可少的工具，特別適合於 Linux 或 UNIX 環境中的各種自動化操作。這些腳本能夠幫助技術人員進行常見的任務，比如文件備份與恢復、系統監控和日誌分析。Shell scripts 直觀且功能強大，能夠將多個系統命令串聯起來進行自動化操作。

功能亮點：
- 文件備份與還原 
- 系統日誌分析 
- 自動化維護任務 

## 使用場景
這些自動化腳本適用於許多場景，無論是大型數據中心的伺服器管理，還是日常運維中的重複性任務，這些工具都能為你節省寶貴的時間和精力。

- 伺服器管理： 遠程重啟、電源管理、硬體監控等操作。
- 運維監控： 系統性能檢測和日誌分析，有效掌握伺服器的健康狀況。
- 自動化數據處理： 利用 Python 腳本進行大規模數據處理和報告生成。

## 貢獻指南
歡迎所有有興趣的人對此 repository 做出貢獻。如果你有任何改進腳本的建議、想添加新的腳本，或是發現任何問題，請隨時提交 Pull Request。我們會定期審查並整合社群的回饋，以確保這個 repository 不斷改進，並為更多用戶提供便利。

提交前請確保腳本運行正常 
添加清晰的註解和使用說明 
若新增腳本，請補充相應的README說明 

## 安裝與使用
克隆 repository：

bash
複製程式碼
```
git clone https://github.com/your_username/automation_script.git
```
瀏覽不同的腳本文件夾，找到合適的腳本： 每個腳本文件夾都包含了詳細的說明文件，幫助你理解和使用這些工具。

運行腳本： 根據腳本類型，使用合適的運行環境。例如，Shell 腳本需要在 UNIX 系統中運行，而 Python 腳本則需要安裝 Python 環境。

