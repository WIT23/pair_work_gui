# copyright by LX in 2023
import os
import sys
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox
from PyQt5.QtWidgets import QLabel, QPushButton, QLCDNumber, QLineEdit, QTextEdit, QWidget, QFileDialog

letters = [chr(i + ord("a")) for i in range(26)]
letters.insert(0, "NO NEED!")

must, choose = ["-n", "-w", "-c"], ["-h", "-t", "-j", "-r"]


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
            self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


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
        running_button.clicked.connect(self.running)
        running_button.setStyleSheet('''
        QPushButton{background:#FFE4E1;border-radius:5px;}
        QPushButton:hover{background:yellow;}''')
        running_button.setFixedHeight(int(0.05 * self.screenheight))

        running_time_label = MyTextLabel("Running Time(ms)", 2)
        self.lcd = QLCDNumber()
        self.lcd.setObjectName("lcdNumber")
        self.running_layout.addWidget(running_button)
        self.running_layout.addWidget(running_time_label)
        self.running_layout.addWidget(self.lcd)

    def para_part(self):
        must_layout = QHBoxLayout()
        choose_layout = QHBoxLayout()
        self.must_widget = []
        self.choose_widget = []
        must_layout.addWidget(MyTextLabel("必选参数（单选）", 1))
        choose_layout.addWidget(MyTextLabel("可选参数", 1))
        for i in range(len(must)):
            check_box = MyCheckBox(must[i])
            self.must_widget.append(check_box)
            must_layout.addWidget(check_box)
        for i in range(2):
            combo_box = MyComboBox(choose[i])
            label = MyTextLabel(choose[i], 1)
            self.choose_widget.append(combo_box)
            choose_layout.addWidget(combo_box)
            choose_layout.addWidget(label)
        for i in range(2):
            check_box = MyCheckBox(choose[i + 2])
            self.choose_widget.append(check_box)
            choose_layout.addWidget(check_box)
        self.para_layout.addWidget(self.layout_to_widget(must_layout))
        self.para_layout.addWidget(self.layout_to_widget(choose_layout))

    def input_part(self):
        input_controller_layout = QHBoxLayout()
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("导入txt文件则先输入文件路径")
        input_path_button = MyPushButton("导入文件")
        input_path_button.clicked.connect(self.file_import)
        input_controller_layout.addWidget(self.input_path_edit)
        input_controller_layout.addWidget(input_path_button)
        self.input_text_edit = QTextEdit()
        self.input_text_edit.setPlaceholderText("输入控制台")

        self.input_layout.addWidget(self.layout_to_widget(input_controller_layout))
        self.input_layout.addWidget(self.input_text_edit)

    def output_part(self):
        output_controller_layout = QHBoxLayout()
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("导出txt文件则先输入文件夹路径")
        output_path_button = MyPushButton("导出文件")
        output_path_button.clicked.connect(self.file_export)
        output_controller_layout.addWidget(self.output_path_edit)
        output_controller_layout.addWidget(output_path_button)
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setPlaceholderText("输出控制台")

        self.output_layout.addWidget(self.layout_to_widget(output_controller_layout))
        self.output_layout.addWidget(self.output_text_edit)

    def file_import(self):
        dir = QFileDialog.getOpenFileName(self, "Open File", "./", "Txt (*.txt)")[0]
        self.input_path_edit.setText(dir)

    def file_export(self):
        dir = QFileDialog.getExistingDirectory()
        if len(dir) != 0:
            dir = os.path.join(dir, "output.txt")
        self.output_path_edit.setText(dir)

    def running(self):
        paras = []
        must_index = self.must_para_get()
        if must_index < 0:
            return
        paras.append(must[must_index])
        paras = paras + self.choose_para_get()
        print(paras)
        input_path = self.input_path_edit.text()
        if len(input_path) == 0:
            text = self.input_text_edit.toPlainText()
            with open("standard_input.txt", "w") as f:
                f.write(text)
            input_path = "./standard_input.txt"
        output_path = self.output_path_edit.text()
        if len(output_path) == 0:
            output_path = "./standard_output.txt"
        command = "./test.exe "
        for para in paras:
            command += para + " "
        command += input_path + " "
        command += ">> " + output_path
        print(command)
        start_time = time.time()
        # command
        end_time = time.time()
        running_time = end_time - start_time
        with open(output_path, "r") as f:
            for i in f.readlines():
                self.output_text_edit.append(i)
        self.lcd.display(running_time)
    def must_para_get(self):
        flag = False
        pos = -1
        for i, box in enumerate(self.must_widget):
            state = box.isChecked()
            if state and flag:
                pos = -1
            elif state:
                pos = i
                flag = True
        if pos < 0:
            strT = '<span style=\" color: #ff0000;\">%s</span>' % ('必须选择唯一的必选参数')
            self.output_text_edit.setText("%s" % (strT))
        return pos

    def choose_para_get(self):
        choose_paras = []
        for i in range(2):
            string = self.choose_widget[i].currentText()
            if string == "NO NEED!":
                continue
            else:
                choose_paras.append(choose[i] + " " + string)
        for i in range(2):
            if self.choose_widget[i + 2].isChecked():
                choose_paras.append(choose[i + 2])
        return choose_paras


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PairWorkWindow()
    window.show()
    sys.exit(app.exec_())
