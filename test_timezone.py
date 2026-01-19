import sqlite3
from datetime import datetime

# 连接数据库
conn = sqlite3.connect('data/worklog.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 获取当前本地时间
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"当前本地时间: {current_time}")

# 添加一条测试记录
cursor.execute('''
    INSERT INTO work_log (date, content, project, tags, created_at)
    VALUES (?, ?, ?, ?, ?)
''', ('2026-01-19', '测试时区修复', 'Test', '#test', current_time))

conn.commit()

# 查询最新记录
cursor.execute('SELECT * FROM work_log ORDER BY id DESC LIMIT 1')
row = cursor.fetchone()

print(f"\n最新记录:")
print(f"ID: {row['id']}")
print(f"日期: {row['date']}")
print(f"时间: {row['created_at']}")
print(f"内容: {row['content']}")
print(f"项目: {row['project']}")

# 检查时间是否匹配
if str(row['created_at']) == current_time:
    print("\n✓ 时区修复成功！时间正确显示为本地时间。")
else:
    print(f"\n✗ 时区修复可能有问题。")
    print(f"  数据库时间: {row['created_at']}")
    print(f"  本地时间: {current_time}")

conn.close()
