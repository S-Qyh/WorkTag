import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class Database:
    def __init__(self, db_path: str = "data/worklog.db"):
        """初始化数据库连接"""
        # 确保数据目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # 创建工作日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                content TEXT NOT NULL,
                project TEXT,
                tags TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # 创建索引以提高查询性能
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON work_log(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_project ON work_log(project)')
        
        self.conn.commit()
    
    def add_log(self, content: str, project: Optional[str] = None, tags: Optional[str] = None):
        """添加工作日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO work_log (date, content, project, tags, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (today, content, project, tags, now))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_today_logs(self) -> List[Dict]:
        """获取今天的工作日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, date, content, project, tags, created_at
            FROM work_log
            WHERE date = ?
            ORDER BY created_at DESC
        ''', (today,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_logs_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """获取指定日期范围内的日志"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, date, content, project, tags, created_at
            FROM work_log
            WHERE date BETWEEN ? AND ?
            ORDER BY date, created_at
        ''', (start_date, end_date))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_weekly_stats(self, start_date: str, end_date: str) -> Dict:
        """获取周统计信息"""
        cursor = self.conn.cursor()
        
        # 总记录数
        cursor.execute('''
            SELECT COUNT(*) as total_count
            FROM work_log
            WHERE date BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_count = cursor.fetchone()[0]
        
        # 按项目统计
        cursor.execute('''
            SELECT project, COUNT(*) as count
            FROM work_log
            WHERE date BETWEEN ? AND ? AND project IS NOT NULL
            GROUP BY project
            ORDER BY count DESC
        ''', (start_date, end_date))
        project_stats = cursor.fetchall()
        
        # 获取所有项目列表
        cursor.execute('''
            SELECT DISTINCT project
            FROM work_log
            WHERE date BETWEEN ? AND ? AND project IS NOT NULL
            ORDER BY project
        ''', (start_date, end_date))
        projects = [row[0] for row in cursor.fetchall()]
        
        return {
            'total_count': total_count,
            'project_stats': project_stats,
            'projects': projects
        }
    
    def delete_log(self, log_id: int) -> bool:
        """删除指定ID的日志"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM work_log WHERE id = ?', (log_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
