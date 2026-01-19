from datetime import datetime
from typing import List, Dict
from .parser import InputParser

class ReportGenerator:
    """周报生成器"""
    
    @staticmethod
    def generate_weekly_report(logs: List[Dict], stats: Dict, start_date: str, end_date: str) -> str:
        """
        生成周报 Markdown 格式
        
        参数:
            logs: 日志列表
            stats: 统计信息
            start_date: 开始日期
            end_date: 结束日期
        """
        # 按项目分组日志
        projects_logs = {}
        for log in logs:
            project = log.get('project', '未分类')
            if project not in projects_logs:
                projects_logs[project] = []
            projects_logs[project].append(log)
        
        # 构建周报
        report_lines = []
        
        # 标题
        report_lines.append(f"# 周报（{start_date} ～ {end_date}）")
        report_lines.append("")
        
        # 本周完成
        report_lines.append("## 一、本周完成")
        report_lines.append("")
        
        if not projects_logs:
            report_lines.append("本周无工作记录")
            report_lines.append("")
        else:
            for project, project_logs in sorted(projects_logs.items()):
                report_lines.append(f"### {project}")
                for log in project_logs:
                    content = log.get('content', '')
                    if content:
                        report_lines.append(f"- {content}")
                report_lines.append("")
        
        # 本周数据
        report_lines.append("## 二、本周数据")
        report_lines.append("")
        
        report_lines.append(f"- 总记录数：{stats.get('total_count', 0)}")
        
        projects = stats.get('projects', [])
        if projects:
            projects_str = " / ".join(projects)
            report_lines.append(f"- 涉及项目：{projects_str}")
        
        # 项目统计详情
        project_stats = stats.get('project_stats', [])
        if project_stats:
            report_lines.append("- 项目分布：")
            for project, count in project_stats:
                report_lines.append(f"  - {project}: {count} 条")
        
        report_lines.append("")
        
        # 下周计划（预留部分）
        report_lines.append("## 三、下周计划")
        report_lines.append("")
        report_lines.append("- [请填写下周计划]")
        report_lines.append("")
        
        # 生成时间
        generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_lines.append(f"*生成时间：{generated_time}*")
        
        return "\n".join(report_lines)
    
    @staticmethod
    def export_to_file(report_content: str, filepath: str = "export/week_report.md"):
        """将周报导出到文件"""
        import os
        
        # 确保导出目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return filepath
    
    @staticmethod
    def generate_and_export_weekly_report(db, start_date: str = None, end_date: str = None):
        """生成并导出周报"""
        # 如果没有提供日期，使用本周
        if not start_date or not end_date:
            start_date, end_date = InputParser.extract_week_dates()
        
        # 获取日志和统计
        logs = db.get_logs_by_date_range(start_date, end_date)
        stats = db.get_weekly_stats(start_date, end_date)
        
        # 生成周报
        report = ReportGenerator.generate_weekly_report(logs, stats, start_date, end_date)
        
        # 导出到文件
        filename = f"export/week_report_{start_date}_to_{end_date}.md"
        filepath = ReportGenerator.export_to_file(report, filename)
        
        return filepath, report
