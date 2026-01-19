import sqlite3

conn = sqlite3.connect('data/worklog.db')
cursor = conn.cursor()

# 获取表结构
cursor.execute('PRAGMA table_info(work_log)')
print("表结构:")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

# 获取创建表的SQL
cursor.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="work_log"')
create_sql = cursor.fetchone()[0]
print(f"\n创建表的SQL:\n{create_sql}")

conn.close()
