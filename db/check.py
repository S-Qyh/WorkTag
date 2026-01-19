
import sqlite3
conn = sqlite3.connect(r'D:\WorkTag\data\worklog.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM work_log ORDER BY created_at DESC')
rows = cursor.fetchall()
for row in rows:
    print(f'ID: {row[0]}, 日期: {row[1]}, 时间: {row[5]}, 内容: {row[2]}, 项目: {row[3]}')
conn.close()
