import re
from typing import Dict, Optional, Tuple

class InputParser:
    """解析用户输入，提取项目、标签和内容"""
    
    @staticmethod
    def parse_input(text: str) -> Dict[str, Optional[str]]:
        """
        解析输入文本，提取项目、标签和内容
        
        输入格式示例：
        - "[Unity][Ads] 修复激励广告回调 #bug #hook"
        - "分析 BillingClient 卡死"
        - "[AOSP] 绕过 OAID 校验"
        
        规则：
        1. [项目名] 表示 project（可以有多个，用逗号分隔）
        2. #xxx 表示标签（可以有多个，用逗号分隔）
        3. 剩余文本作为 content
        """
        if not text or not text.strip():
            return {"content": "", "project": None, "tags": None}
        
        text = text.strip()
        project = None
        tags = None
        
        # 提取项目（[项目名] 格式）
        project_pattern = r'\[([^\]]+)\]'
        projects = re.findall(project_pattern, text)
        
        if projects:
            # 移除项目部分
            text = re.sub(project_pattern, '', text).strip()
            # 如果有多个项目，用逗号连接
            project = ', '.join(projects)
        
        # 提取标签（#标签 格式）
        tag_pattern = r'#([a-zA-Z0-9_\-]+)'
        tag_matches = re.findall(tag_pattern, text)
        
        if tag_matches:
            # 移除标签部分
            text = re.sub(tag_pattern, '', text).strip()
            # 用逗号连接标签
            tags = ', '.join(tag_matches)
        
        # 清理多余的空格
        content = ' '.join(text.split())
        
        return {
            "content": content,
            "project": project if project else None,
            "tags": tags if tags else None
        }
    
    @staticmethod
    def format_for_display(log_entry: Dict) -> str:
        """格式化日志条目用于显示"""
        parts = []
        
        if log_entry.get('project'):
            projects = log_entry['project'].split(', ')
            for proj in projects:
                parts.append(f"[{proj}]")
        
        parts.append(log_entry.get('content', ''))
        
        if log_entry.get('tags'):
            tags = log_entry['tags'].split(', ')
            for tag in tags:
                parts.append(f"#{tag}")
        
        return ' '.join(parts)
    
    @staticmethod
    def extract_week_dates() -> Tuple[str, str]:
        """获取本周的起始和结束日期（周一到周日）"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        # 获取本周一（0=周一，6=周日）
        weekday = today.weekday()  # 0=周一，6=周日
        start_date = today - timedelta(days=weekday)
        end_date = start_date + timedelta(days=6)
        
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
