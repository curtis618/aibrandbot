import os
import sys

# 這是為了滿足 Zeabur 預設尋找 main.py 的行為
# 如果 Procfile 沒有生效，Zeabur 會執行這個檔案

if __name__ == "__main__":
    # 切換到 Django 專案目錄 (因為 manage.py 在 linegemini 資料夾內)
    if os.path.exists("linegemini"):
        os.chdir("linegemini")
    
    print("Starting Gunicorn from main.py...")
    
    # 執行 Gunicorn
    # 注意：Zeabur 會自動分配 PORT 環境變數，但 Gunicorn 預設 8000
    # 我們這裡直接綁定 0.0.0.0:8000，Zeabur Service Port 設定也要記得設為 8000
    os.system("gunicorn linegemini.wsgi --bind 0.0.0.0:8000 --log-file -")
