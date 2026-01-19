import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton, QLabel,
    QMenu, QSystemTrayIcon, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QPoint, QSize
from PySide6.QtGui import QIcon, QAction, QFont, QKeyEvent, QColor
import os
from datetime import datetime

# 导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import Database
from service.parser import InputParser


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化数据库
        self.db = Database()
        
        # 窗口设置
        self.setWindowTitle("WorkTag - 工作日志")
        self.setFixedSize(400, 500)
        
        # 无边框、置顶窗口
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # 半透明效果
        self.setWindowOpacity(0.95)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 8px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QListWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: none;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #3c3c3c;
            }
            QListWidget::item:selected {
                background-color: #3c3c3c;
            }
            QPushButton {
                background-color: #4a9cff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5ca8ff;
            }
            QPushButton:pressed {
                background-color: #3a8cff;
            }
            QLabel {
                color: #aaaaaa;
                font-size: 12px;
            }
        """)
        
        # 初始化UI
        self.init_ui()
        
        # 加载今天的数据
        self.load_today_logs()
        
        # 系统托盘
        self.init_tray_icon()
        
        # 拖拽相关
        self.dragging = False
        self.drag_position = QPoint()
    
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # 标题栏
        title_bar = QHBoxLayout()
        
        title_label = QLabel("📝 WorkTag")
        title_label.setStyleSheet("color: #4a9cff; font-size: 16px; font-weight: bold;")
        
        # 关闭按钮
        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c;
                color: white;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff7c7c;
            }
        """)
        close_btn.clicked.connect(self.hide_window)
        
        title_bar.addWidget(title_label)
        title_bar.addStretch()
        title_bar.addWidget(close_btn)
        
        layout.addLayout(title_bar)
        
        # 日期显示
        today = datetime.now().strftime("%Y年%m月%d日 %A")
        date_label = QLabel(f"📅 {today}")
        date_label.setStyleSheet("color: #888888; font-size: 13px; margin-bottom: 10px;")
        layout.addWidget(date_label)
        
        # 输入框
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入工作内容，例如：[Unity][Ads] 修复激励广告回调 #bug")
        self.input_field.returnPressed.connect(self.add_log)
        layout.addWidget(self.input_field)
        
        # 按钮行
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("添加记录")
        add_button.clicked.connect(self.add_log)
        
        clear_button = QPushButton("清空输入")
        clear_button.clicked.connect(self.clear_input)
        
        report_button = QPushButton("生成周报")
        report_button.clicked.connect(self.generate_report)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(report_button)
        
        layout.addLayout(button_layout)
        
        # 今日记录标题
        logs_label = QLabel("今日记录：")
        logs_label.setStyleSheet("color: #aaaaaa; font-size: 14px; margin-top: 10px;")
        layout.addWidget(logs_label)
        
        # 日志列表
        self.log_list = QListWidget()
        self.log_list.itemDoubleClicked.connect(self.delete_log_item)
        layout.addWidget(self.log_list)
        
        # 状态栏
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #666666; font-size: 11px; margin-top: 5px;")
        layout.addWidget(self.status_label)
    
    def init_tray_icon(self):
        """初始化系统托盘图标"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # 设置托盘图标
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("隐藏窗口", self)
        hide_action.triggered.connect(self.hide_window)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        report_action = QAction("生成周报", self)
        report_action.triggered.connect(self.generate_report)
        tray_menu.addAction(report_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("WorkTag - 工作日志工具")
        self.tray_icon.show()
        
        # 托盘图标点击事件
        self.tray_icon.activated.connect(self.tray_icon_activated)
    
    def tray_icon_activated(self, reason):
        """托盘图标被激活"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide_window()
            else:
                self.show_window()
    
    def mousePressEvent(self, event):
        """鼠标按下事件（用于窗口拖拽）"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件（用于窗口拖拽）"""
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.dragging = False
    
    def keyPressEvent(self, event: QKeyEvent):
        """键盘事件"""
        if event.key() == Qt.Key_Escape:
            self.hide_window()
        elif event.key() == Qt.Key_Delete and self.log_list.currentItem():
            self.delete_log_item(self.log_list.currentItem())
        else:
            super().keyPressEvent(event)
    
    def add_log(self):
        """添加工作日志"""
        text = self.input_field.text().strip()
        if not text:
            self.show_status("请输入内容", "warning")
            return
        
        # 解析输入
        parsed = InputParser.parse_input(text)
        
        # 添加到数据库
        try:
            log_id = self.db.add_log(
                content=parsed["content"],
                project=parsed["project"],
                tags=parsed["tags"]
            )
            
            # 清空输入框
            self.input_field.clear()
            
            # 重新加载日志
            self.load_today_logs()
            
            # 显示成功状态
            self.show_status(f"已添加记录 #{log_id}", "success")
            
        except Exception as e:
            self.show_status(f"添加失败: {str(e)}", "error")
    
    def clear_input(self):
        """清空输入框"""
        self.input_field.clear()
        self.input_field.setFocus()
        self.show_status("输入框已清空", "info")
    
    def load_today_logs(self):
        """加载今天的工作日志"""
        self.log_list.clear()
        
        try:
            logs = self.db.get_today_logs()
            
            if not logs:
                item = QListWidgetItem("今天还没有记录，开始添加吧！")
                item.setForeground(QColor("#888888"))
                self.log_list.addItem(item)
                return
            
            for log in logs:
                # 格式化显示
                display_text = InputParser.format_for_display(log)
                
                # 添加时间信息
                created_at = log.get('created_at', '')
                if created_at:
                    if isinstance(created_at, str):
                        time_str = created_at.split()[1][:5] if ' ' in created_at else ''
                    else:
                        time_str = created_at.strftime("%H:%M")
                    
                    if time_str:
                        display_text = f"[{time_str}] {display_text}"
                
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, log.get('id'))
                self.log_list.addItem(item)
            
            # 更新状态
            self.show_status(f"已加载 {len(logs)} 条记录", "info")
            
        except Exception as e:
            self.show_status(f"加载失败: {str(e)}", "error")
    
    def delete_log_item(self, item):
        """删除日志项"""
        if not item:
            return
        
        log_id = item.data(Qt.UserRole)
        if not log_id:
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self, '确认删除',
            '确定要删除这条记录吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.db.delete_log(log_id)
                if success:
                    self.log_list.takeItem(self.log_list.row(item))
                    self.show_status("记录已删除", "success")
                else:
                    self.show_status("删除失败", "error")
            except Exception as e:
                self.show_status(f"删除失败: {str(e)}", "error")
    
    def generate_report(self):
        """生成周报"""
        try:
            from service.report import ReportGenerator
            
            filepath, report = ReportGenerator.generate_and_export_weekly_report(self.db)
            
            # 显示成功消息
            QMessageBox.information(
                self, 
                "周报生成成功",
                f"周报已生成并保存到：\n{os.path.abspath(filepath)}"
            )
            
            self.show_status("周报生成成功", "success")
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "周报生成失败",
                f"生成周报时出错：\n{str(e)}"
            )
            self.show_status(f"周报生成失败: {str(e)}", "error")
    
    def show_status(self, message: str, status_type: str = "info"):
        """显示状态消息"""
        colors = {
            "info": "#666666",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336"
        }
        
        color = colors.get(status_type, "#666666")
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 11px; margin-top: 5px;")
        
        # 3秒后清除状态
        QTimer.singleShot(3000, lambda: self.status_label.setText("就绪"))
    
    def show_window(self):
        """显示窗口"""
        self.show()
        self.raise_()
        self.activateWindow()
    
    def hide_window(self):
        """隐藏窗口"""
        self.hide()
        self.show_status("窗口已隐藏到托盘", "info")
    
    def quit_app(self):
        """退出应用程序"""
        self.db.close()
        self.tray_icon.hide()
        QApplication.quit()


def main():
    """应用程序入口"""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
