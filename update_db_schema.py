import sqlite3
import os

def update_database_schema():
    """更新数据库表结构，移除DEFAULT CURRENT_TIMESTAMP约束"""
    
    db_path = "data/worklog.db"
    
    if not os.path.exists(db_path):
        print("数据库文件不存在，无需更新")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 创建新表（不带DEFAULT约束）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_log_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                content TEXT NOT NULL,
                project TEXT,
                tags TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # 2. 复制数据到新表
        cursor.execute('''
            INSERT INTO work_log_new (id, date, content, project, tags, created_at)
            SELECT id, date, content, project, tags, created_at
            FROM work_log
        ''')
        
        # 3. 删除旧表
        cursor.execute('DROP TABLE work_log')
        
        # 4. 重命名新表为旧表名
        cursor.execute('ALTER TABLE work_log_new RENAME TO work_log')
        
        # 5. 重新创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON work_log(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_project ON work_log(project)')
        
        conn.commit()
        print("数据库表结构更新成功！")
        
        # 显示更新后的表结构
        cursor.execute('PRAGMA table_info(work_log)')
        print("\n更新后的表结构:")
        for col in cursor.fetchall():
            print(f"  {col[1]} ({col[2]})")
            
    except Exception as e:
        conn.rollback()
        print(f"更新失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_database_schema()
