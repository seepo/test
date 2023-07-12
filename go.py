import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QHBoxLayout, QVBoxLayout, QMessageBox


class SerialTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口大小和标题
        self.setGeometry(300, 200, 100,200)
        self.setWindowTitle('嵌入式2.4基线go命令')

        # 创建控件
        self.com_label = QLabel('COM口:')
        self.com_combo = QComboBox()
        self.baud_label = QLabel('波特率:')
        self.baud_edit = QLineEdit()
        self.connect_button = QPushButton('连接')
        self.send_edit = QLineEdit()
        self.send_button = QPushButton('发送')
        self.recv_edit = QTextEdit()
        self.custom_button1 = QPushButton('关闭老化测试')
        self.custom_button2 = QPushButton('开启老化测试')
        self.custom_button3 = QPushButton('下发500个事件')
        self.custom_button4 = QPushButton('下发500个消息')
        self.custom_button5 = QPushButton('320x240屏弹窗')
        self.custom_button6 = QPushButton('160x128屏弹窗')
        self.custom_button7 = QPushButton('反复重启测试')
        self.custom_button8 = QPushButton('参数保存tf卡')
        self.custom_button9 = QPushButton('屏幕截图')
        self.custom_button10 = QPushButton('开始录像')
        self.custom_button11 = QPushButton('结束录像')
        self.custom_button12 = QPushButton('拍照')

        # 设置控件的默认值
        self.baud_edit.setText('115200')
        self.recv_edit.setReadOnly(True)

        # 创建布局
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.com_label)
        hbox1.addWidget(self.com_combo)
        hbox1.addWidget(self.baud_label)
        hbox1.addWidget(self.baud_edit)
        hbox1.addWidget(self.connect_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.send_edit)
        hbox2.addWidget(self.send_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.recv_edit)
        vbox.addWidget(self.custom_button1)
        vbox.addWidget(self.custom_button2)
        vbox.addWidget(self.custom_button3)
        vbox.addWidget(self.custom_button4)
        vbox.addWidget(self.custom_button5)
        vbox.addWidget(self.custom_button6)
        vbox.addWidget(self.custom_button7)
        vbox.addWidget(self.custom_button8)
        vbox.addWidget(self.custom_button9)
        vbox.addWidget(self.custom_button10)
        vbox.addWidget(self.custom_button11)
        vbox.addWidget(self.custom_button12)

        # 设置主布局
        self.setLayout(vbox)

        # 绑定事件
        self.connect_button.clicked.connect(self.connect)
        self.send_button.clicked.connect(self.send)
        self.custom_button1.clicked.connect(lambda: self.send_custom('custom1'))
        self.custom_button2.clicked.connect(lambda: self.send_custom('custom2'))
        self.custom_button3.clicked.connect(lambda: self.send_custom('custom3'))
        self.custom_button4.clicked.connect(lambda: self.send_custom('custom4'))
        self.custom_button5.clicked.connect(lambda: self.send_custom('custom5'))
        self.custom_button6.clicked.connect(lambda: self.send_custom('custom6'))
        self.custom_button7.clicked.connect(lambda: self.send_custom('custom7'))
        self.custom_button8.clicked.connect(lambda: self.send_custom('custom8'))
        self.custom_button9.clicked.connect(lambda: self.send_custom('custom9'))
        self.custom_button10.clicked.connect(lambda: self.send_custom('custom10'))
        self.custom_button11.clicked.connect(lambda: self.send_custom('custom11'))
        self.custom_button12.clicked.connect(lambda: self.send_custom('custom12'))

        # 自动获取COM口
        self.update_com_ports()

    def update_com_ports(self):
        # 获取可用的COM口
        com_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.com_combo.clear()
        self.com_combo.addItems(com_ports)

    def connect(self):
        # 连接/断开串口
        if self.connect_button.text() == '连接':
            # 获取串口参数
            com_port = self.com_combo.currentText()
            baud_rate = int(self.baud_edit.text())

            # 打开串口
            try:
                self.ser = serial.Serial(com_port, baud_rate, timeout=1)
                self.connect_button.setText('断开')
            except serial.SerialException:
                QMessageBox.warning(self, '警告', '无法连接串口')
        else:
            # 关闭串口
            self.ser.close()
            self.connect_button.setText('连接')

    def send(self):
        # 发送数据
        if self.ser.isOpen():
            data = self.send_edit.text() + '\r\n'
            self.ser.write(data.encode())
            self.recv_edit.setText(data)

        else:
            QMessageBox.warning(self, '警告', '串口未连接')

    def send_custom(self, cmd):
        # 发送自定义命令
        if cmd == 'custom1':
            data = 'go 46 0\r\n'
        elif cmd == 'custom2':
            data = 'go 46 1\r\n'
        elif cmd == 'custom3':
            data = 'go 75 500 name addr info\r\n'
        elif cmd == 'custom4':
            data = 'go 74 500 info\r\n'
        elif cmd == 'custom5':
            data = 'go 61 2\r\n'
        elif cmd == 'custom6':
            data = 'go 62 2\r\n'
        elif cmd == 'custom7':
            data = 'go 77 10 60\r\n'
        elif cmd == 'custom8':
            data = 'go 41\r\n'
        elif cmd == 'custom9':
            data = 'go 60\r\n'
        elif cmd == 'custom10':
            data = 'go 63 1\r\n'
        elif cmd == 'custom11':
            data = 'go 63 0\r\n'
        elif cmd == 'custom12':
            data = 'go 65\r\n'
        self.recv_edit.setText(data)

        if self.ser.isOpen():
            self.ser.write(data.encode())
        else:
            QMessageBox.warning(self, '警告', '串口未连接')
        

    def closeEvent(self, event):
        # 关闭窗口时关闭串口
        if self.ser.isOpen():
            self.ser.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tool = SerialTool()
    tool.show()
    sys.exit(app.exec_())