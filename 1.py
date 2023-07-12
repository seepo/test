import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QAction, QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QColor, QTextCharFormat, QFont
from PyQt5.QtCore import Qt
import difflib


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化UI
        self.initUI()

        # 初始化文件路径
        self.file1_path = ''
        self.file2_path = ''

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('比对工具')

        # 设置窗口大小
        self.setGeometry(100, 100, 1000, 600)

        # 创建菜单栏
        menubar = self.menuBar()

        # 创建文件菜单
        file_menu = menubar.addMenu('文件')

        # 创建打开文件1的动作
        open_file1_action = QAction('打开文件1', self)
        open_file1_action.triggered.connect(self.open_file1)
        file_menu.addAction(open_file1_action)

        # 创建打开文件2的动作
        open_file2_action = QAction('打开文件2', self)
        open_file2_action.triggered.connect(self.open_file2)
        file_menu.addAction(open_file2_action)

        # 创建比对动作
        compare_action = QAction('比对', self)
        compare_action.triggered.connect(self.compare)
        file_menu.addAction(compare_action)

        # 创建文本框
        self.text_edit1 = QTextEdit()
        self.text_edit2 = QTextEdit()

        # 创建标签
        label1 = QLabel('文件1')
        label2 = QLabel('文件2')

        # 创建网格布局
        grid_layout = QGridLayout()
        grid_layout.addWidget(label1, 0, 0)
        grid_layout.addWidget(label2, 0, 1)
        grid_layout.addWidget(self.text_edit1, 1, 0)
        grid_layout.addWidget(self.text_edit2, 1, 1)

        # 创建中心窗口
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)

        # 设置中心窗口
        self.setCentralWidget(central_widget)

    def open_file1(self):
        # 打开文件1
        file_path, _ = QFileDialog.getOpenFileName(self, '打开文件1', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            self.file1_path = file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text_edit1.setText(f.read())

    def open_file2(self):
        # 打开文件2
        file_path, _ = QFileDialog.getOpenFileName(self, '打开文件2', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            self.file2_path = file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text_edit2.setText(f.read())

    def compare(self):
        # 比对文件1和文件2
        if self.file1_path and self.file2_path:
            with open(self.file1_path, 'r', encoding='utf-8') as f1, open(self.file2_path, 'r', encoding='utf-8') as f2:
                text1 = f1.readlines()
                text2 = f2.readlines()

            # 使用difflib库比对文本
            diff = difflib.unified_diff(text1, text2, lineterm='', n=0)

            # 标注差异
            for line in diff:
                if line.startswith(' '):
                    # 相同行
                    self.add_text(self.text_edit1, line[2:], Qt.black)
                    self.add_text(self.text_edit2, line[2:], Qt.black)
                elif line.startswith('-'):
                    # 文件1中的行
                    self.add_text(self.text_edit1, line[2:], Qt.red)
                    self.add_text(self.text_edit2, '', Qt.red)
                elif line.startswith('+'):
                    # 文件2中的行
                    self.add_text(self.text_edit1, '', Qt.green)
                    self.add_text(self.text_edit2, line[2:], Qt.green)

    def add_text(self, text_edit, text, color):
        # 在文本框中添加文本，并设置颜色
        cursor = text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.insertText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())