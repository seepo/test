import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("请求工具")
        self.resize(800, 600)

        # 创建布局
        self.layout = QVBoxLayout()

        # 创建网址输入框
        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)

        # 创建发送按钮
        self.send_button = QPushButton("发送请求")
        self.send_button.clicked.connect(self.send_request)
        self.layout.addWidget(self.send_button)

        # 创建响应结果文本框
        self.response_text = QTextEdit()
        self.layout.addWidget(self.response_text)

        # 设置布局为主窗口的布局
        self.setLayout(self.layout)

    def send_request(self):
        url = self.url_input.text()

        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.response_text.setText(response.text)
            else:
                self.response_text.setText(f"请求失败，状态码：{response.status_code}")
        except requests.RequestException as e:
            self.response_text.setText(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

