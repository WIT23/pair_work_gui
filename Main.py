# copyright by LX in 2023
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox
from PyQt5.QtWidgets import QLabel, QPushButton, QLCDNumber, QLineEdit, QTextEdit, QWidget

letters = [chr(i + ord("a")) for i in range(26)]
letters.insert(0, "NO NEED!")


class MyCheckBox(QCheckBox):
    def __init__(self, name):
        super(MyCheckBox, self).__init__()
        self.setText(name)
        self.setObjectName(name)


class MyComboBox(QComboBox):
    def __init__(self, name):
        super(MyComboBox, self).__init__()
        self.setObjectName(name)
        self.addItems(letters)
        self.setCurrentText("NO NEED!")


class MyTextLabel(QLabel):
    def __init__(self, name, position=0):  # position: 0 --> center, 1 --> left, 2 --> right
        super(MyTextLabel, self).__init__()
        self.setText(name)
        self.setObjectName(name)
        if position == 0:
            self.setAlignment(QtCore.Qt.AlignCenter)
        elif position == 1:
            self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        else:
            self.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)


class MyPushButton(QPushButton):
    def __init__(self, name):
        super(MyPushButton, self).__init__()
        self.setText(name)
        self.setObjectName(name)


class PairWorkWindow(QMainWindow):
    def __init__(self):
        super(PairWorkWindow, self).__init__()
        self.basic_setting()
        self.layout_init()
        self.running_part()
        self.para_part()
        self.input_part()
        self.output_part()
        self.layout_setting()

    @staticmethod
    def layout_to_widget(layout):
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def basic_setting(self):
        self.setObjectName("MainWindow")
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()
        self.setFixedSize(int(0.5 * self.screenwidth), int(0.5 * self.screenheight))
        print("screenheight:{:d}, screenwidth:{:d}".format(self.screenheight, self.screenwidth))

    def layout_init(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.whole_layout = QGridLayout()

        self.input_layout = QVBoxLayout()
        self.output_layout = QVBoxLayout()
        self.para_layout = QVBoxLayout()
        self.running_layout = QHBoxLayout()
        self.console_layout = QHBoxLayout()

    def layout_setting(self):
        self.whole_layout.addWidget(self.layout_to_widget(self.running_layout))
        self.whole_layout.addWidget(self.layout_to_widget(self.para_layout))

        self.console_layout.addWidget(self.layout_to_widget(self.input_layout))
        self.console_layout.addWidget(self.layout_to_widget(self.output_layout))

        self.whole_layout.addWidget(self.layout_to_widget(self.console_layout))

        self.main_widget.setLayout(self.whole_layout)

    def running_part(self):
        running_button = MyPushButton("Start Running")
        running_button.setStyleSheet('''
        QPushButton{background:#FFE4E1;border-radius:5px;}
        QPushButton:hover{background:yellow;}''')
        running_button.setFixedHeight(int(0.05 * self.screenheight))

        running_time_label = MyTextLabel("Running Time(ms)", 2)
        lcd = QLCDNumber()
        lcd.setObjectName("lcdNumber")
        self.running_layout.addWidget(running_button)
        self.running_layout.addWidget(running_time_label)
        self.running_layout.addWidget(lcd)

    def para_part(self):
        must, choose = ["-n", "-w", "-c"], ["-h", "-t", "-j", "-r"]
        must_layout = QHBoxLayout()
        choose_layout = QHBoxLayout()
        must_widget = []
        choose_widget = []
        choose_labels = []
        must_layout.addWidget(MyTextLabel("必选参数（单选）", 1))
        choose_layout.addWidget(MyTextLabel("可选参数", 1))
        for i in range(len(must)):
            check_box = MyCheckBox(must[i])
            must_widget.append(check_box)
            must_layout.addWidget(check_box)
        for i in range(2):
            combo_box = MyComboBox(choose[i])
            label = MyTextLabel(choose[i], 1)
            choose_widget.append(combo_box)
            choose_labels.append(label)
            choose_layout.addWidget(combo_box)
            choose_layout.addWidget(label)
        for i in range(2):
            check_box = MyCheckBox(choose[i + 2])
            choose_widget.append(check_box)
            choose_layout.addWidget(check_box)
        self.para_layout.addWidget(self.layout_to_widget(must_layout))
        self.para_layout.addWidget(self.layout_to_widget(choose_layout))

    def input_part(self):
        input_controller_layout = QHBoxLayout()
        input_address_edit = QLineEdit()
        input_address_edit.setPlaceholderText("如需导入txt文件则先输入文件路径")
        input_path_button = MyPushButton("导入文件")
        input_controller_layout.addWidget(input_address_edit)
        input_controller_layout.addWidget(input_path_button)
        input_text_edit = QTextEdit()
        input_text_edit.setPlaceholderText("输入控制台")

        self.input_layout.addWidget(self.layout_to_widget(input_controller_layout))
        self.input_layout.addWidget(input_text_edit)

    def output_part(self):
        output_controller_layout = QHBoxLayout()
        output_address_edit = QLineEdit()
        output_address_edit.setPlaceholderText("如需导出txt文件则先输入文件路径")
        output_path_button = MyPushButton("导出文件")
        output_controller_layout.addWidget(output_address_edit)
        output_controller_layout.addWidget(output_path_button)
        output_text_edit = QTextEdit()
        output_text_edit.setPlaceholderText("输出控制台")

        self.output_layout.addWidget(self.layout_to_widget(output_controller_layout))
        self.output_layout.addWidget(output_text_edit)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PairWorkWindow()
    window.show()
    sys.exit(app.exec_())
