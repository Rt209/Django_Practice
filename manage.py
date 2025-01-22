#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path  # 使用 pathlib 動態處理路徑

# 設定專案的根目錄
BASE_DIR = Path(__file__).resolve().parent  # 使用 pathlib 動態解析路徑

def main():
    """Run administrative tasks."""
    # 設定 Django 的設定檔環境變數
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # 執行 Django 的管理命令
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # 動態加入專案路徑，確保跨平台兼容
    print(f"BASE_DIR: {BASE_DIR}")  # 用於除錯，打印路徑
    sys.path.append(str(BASE_DIR))  # 確保 BASE_DIR 為字串
    main()
