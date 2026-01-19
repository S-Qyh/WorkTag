#!/usr/bin/env python3
"""
WorkTag - 打包脚本
用于将Python应用程序打包为Windows可执行文件
"""

import os
import sys
import shutil
import PyInstaller.__main__

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理spec文件
    spec_file = 'WorkTag.spec'
    if os.path.exists(spec_file):
        print(f"清理文件: {spec_file}")
        os.remove(spec_file)

def collect_data_files():
    """收集数据文件（图标、数据库等）"""
    data_files = []
    
    # 图标文件
    icon_path = 'ui/icon.png'
    if os.path.exists(icon_path):
        data_files.append((icon_path, 'ui'))
    
    # 数据库文件（如果需要初始数据库）
    db_dir = 'data'
    if os.path.exists(db_dir):
        for root, dirs, files in os.walk(db_dir):
            for file in files:
                if file.endswith('.db'):
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, '.')
                    data_files.append((src_path, rel_path))
    
    return data_files

def build_exe():
    """构建可执行文件"""
    print("=" * 50)
    print("WorkTag - 打包为Windows可执行文件")
    print("=" * 50)
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    # 收集数据文件
    data_files = collect_data_files()
    
    # PyInstaller参数
    pyinstaller_args = [
        'main.py',  # 主程序入口
        '--name=WorkTag',  # 可执行文件名称
        '--onefile',  # 打包为单个exe文件
        '--windowed',  # 窗口程序（不显示控制台）
        '--clean',  # 清理临时文件
        '--noconfirm',  # 覆盖输出目录而不确认
    ]
    
    # 添加图标
    icon_path = 'ui/icon.png'
    if os.path.exists(icon_path):
        pyinstaller_args.append(f'--icon={icon_path}')
        print(f"使用图标: {icon_path}")
    
    # 添加数据文件
    for src, dst in data_files:
        pyinstaller_args.append(f'--add-data={src};{dst}')
        print(f"添加数据文件: {src} -> {dst}")
    
    # 添加隐藏导入（PySide6可能需要）
    pyinstaller_args.extend([
        '--hidden-import=PySide6',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=sqlite3',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=datetime',
    ])
    
    # 添加排除模块（减少体积）
    pyinstaller_args.extend([
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
    ])
    
    print("\n开始打包...")
    print(f"PyInstaller参数: {pyinstaller_args}")
    print("-" * 50)
    
    try:
        # 运行PyInstaller
        PyInstaller.__main__.run(pyinstaller_args)
        
        print("\n" + "=" * 50)
        print("打包完成！")
        print("=" * 50)
        
        # 显示输出信息
        dist_dir = 'dist'
        if os.path.exists(dist_dir):
            exe_files = [f for f in os.listdir(dist_dir) if f.endswith('.exe')]
            if exe_files:
                exe_path = os.path.join(dist_dir, exe_files[0])
                exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"生成的可执行文件: {exe_path}")
                print(f"文件大小: {exe_size:.2f} MB")
                print(f"完整路径: {os.path.abspath(exe_path)}")
                
                # 复制图标到dist目录（方便用户查看）
                if os.path.exists(icon_path):
                    shutil.copy2(icon_path, dist_dir)
                    print(f"图标已复制到: {os.path.join(dist_dir, 'icon.png')}")
        
        print("\n使用说明:")
        print("1. 可执行文件位于 'dist' 目录")
        print("2. 首次运行会在程序所在目录创建 'data' 文件夹")
        print("3. 程序会常驻系统托盘")
        print("4. 右键点击托盘图标可以退出程序")
        
    except Exception as e:
        print(f"\n打包失败: {e}")
        sys.exit(1)

def create_standalone_package():
    """创建独立发布包（包含exe和必要文件）"""
    print("\n" + "=" * 50)
    print("创建独立发布包")
    print("=" * 50)
    
    dist_dir = 'dist'
    package_dir = 'WorkTag_Package'
    
    if not os.path.exists(dist_dir):
        print("错误: dist目录不存在，请先运行打包")
        return
    
    # 创建发布包目录
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # 复制exe文件
    exe_files = [f for f in os.listdir(dist_dir) if f.endswith('.exe')]
    if not exe_files:
        print("错误: 未找到exe文件")
        return
    
    for exe_file in exe_files:
        src = os.path.join(dist_dir, exe_file)
        dst = os.path.join(package_dir, exe_file)
        shutil.copy2(src, dst)
        print(f"复制: {exe_file}")
    
    # 复制图标
    icon_src = 'ui/icon.png'
    if os.path.exists(icon_src):
        shutil.copy2(icon_src, package_dir)
        print("复制: icon.png")
    
    # 创建说明文件
    readme_content = """WorkTag - 工作日志工具
=======================

这是一个Windows桌面应用程序，用于记录日常工作日志。

使用方法：
1. 双击运行 WorkTag.exe
2. 程序启动后会显示在系统托盘中
3. 点击托盘图标可以显示/隐藏主窗口
4. 在主窗口中输入工作内容，按Enter键保存
5. 双击记录可以删除

功能特点：
- 无边框可拖拽窗口
- 系统托盘常驻
- 自动分类和标签
- 周报生成
- 数据存储在本地SQLite数据库

注意事项：
- 首次运行会自动创建data文件夹
- 数据文件位于程序所在目录的data文件夹中
- 右键点击托盘图标可以退出程序

作者：Qyh
版本：1.0.0
"""
    
    with open(os.path.join(package_dir, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"\n发布包已创建: {package_dir}")
    print(f"包含文件: {os.listdir(package_dir)}")

if __name__ == "__main__":
    # 构建exe
    build_exe()
    
    # 创建发布包
    create_standalone_package()
    
    print("\n" + "=" * 50)
    print("全部完成！")
    print("=" * 50)
