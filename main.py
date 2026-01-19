#!/usr/bin/env python3
"""
WorkTag - Windows 桌面工作日志工具
主程序入口
"""

import sys
import os
from PySide6.QtWidgets import QApplication

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import main as ui_main


def check_dependencies():
    """检查依赖是否安装"""
    try:
        import PySide6
        print("✓ PySide6 已安装")
    except ImportError:
        print("✗ PySide6 未安装，正在安装...")
        os.system("pip install PySide6")
        print("✓ PySide6 安装完成")
    
    try:
        import sqlite3
        print("✓ SQLite3 已安装（Python 内置）")
    except ImportError:
        print("✗ SQLite3 未安装")


def main():
    """主函数"""
    print("=" * 50)
    print("WorkTag - Windows 桌面工作日志工具")
    print("=" * 50)
    
    # 检查依赖
    check_dependencies()
    
    print("\n启动应用程序...")
    print("提示：")
    print("  • 按 Enter 键提交工作记录")
    print("  • 按 Esc 键隐藏窗口")
    print("  • 双击记录可删除")
    print("  • 窗口可拖拽移动位置")
    print("  • 程序会常驻系统托盘")
    print("=" * 50)
    
    # 启动 UI
    ui_main()


if __name__ == "__main__":
    main()
