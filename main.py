# importing libraries
import datetime
import random
import sys
import time
import os

import keyboard

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import playsound
import winsound

opener = None

time_set = None
disp_gear = 'D'
input_cnt = 1

error_cnt = 0
total_cnt = 1

start_gear = ''

react_time_list = []

# class for scrollable label
class ScrollLabel(QScrollArea):
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 4px solid black;"
                                 "background : white;"
                                 "}")

        # adding label to the layout
        lay.addWidget(self.label)

        # setting font
        self.label.setFont(QFont('Arial', 15))

        self.label.setText("Waiting for start...")

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

    def text(self):
        return self.label.text()


class Window(QWidget):
    key_p = '9'
    key_r = '6'
    key_n = '3'
    key_d = 'decimal'
    key_set_list = []

    # key_set_list = [{'P': '8', 'R': '9', 'N': '6', 'D': '3'},
    #                 {'P': '4', 'R': '8', 'N': '5', 'D': '2'},
    #                 {'P': '9', 'R': '6', 'N': '3', 'D': 'decimal'},
    #                 {'P': '4', 'R': '5', 'N': '6', 'D': '+'},
    #                 {'P': '8', 'R': '3', 'N': '6', 'D': '9'},
    #                 {'P': '4', 'R': '2', 'N': '5', 'D': '8'},
    #                 {'P': '9', 'R': 'decimal', 'N': '3', 'D': '6'},
    #                 {'P': '4', 'R': '+', 'N': '6', 'D': '5'}]

    subject_index = 1

    def __init__(self):
        super().__init__()

        f = open("./Task/key_set.txt", 'r')

        key_set_str = f.read()

        f.close()

        key_str_sap1 = key_set_str.split('|')

        for i in range(0, len(key_str_sap1)):
            key_str_sap2 = key_str_sap1[i].split(',')

            key_set_seg = {'P': key_str_sap2[0], 'R': key_str_sap2[1], 'N': key_str_sap2[2], 'D': key_str_sap2[3]}

            self.key_set_list.append(key_set_seg)

        # setting title
        self.setWindowTitle("Test Window")

        # setting geometry
        self.setGeometry(100, 100, 600, 700)

        # calling method
        self.uiComponents()

        # showing all the widgets
        self.show()

        global opener
        opener = PicWindow()
        opener.show()

    def keyboardEventReceived(self, event):
        global time_set
        global error_cnt

        if time_set is not None:
            if event.event_type == 'down':
                now = datetime.datetime.now()
                global disp_gear
                global input_cnt
                global total_cnt
                global react_time_list

                time_diff = now - time_set

                #playsound.playsound('./Ring.wav`')
                winsound.PlaySound('./Ring.wav', winsound.SND_ASYNC)
                self.label.setText(self.label.text() + "\n 테스트 입니다. 입력 키: " + event.name)

                if event.name == self.key_p:
                    if disp_gear == 'P' and input_cnt == 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "기어: P단 | 반응 시간: " + "%02d.%02d" % (
                        time_diff.seconds, time_diff.microseconds / 1000))

                        react_time_list.append(float("%02d.%02d" % (time_diff.seconds, time_diff.microseconds / 1000)))

                        input_cnt = input_cnt + 1
                        total_cnt = total_cnt + 1

                    elif disp_gear != 'P':
                        text = self.label.text()
                        self.label.setText(
                            text + "\n" + "올바르지 않은 기어 입력입니다. 입력 키: " + event.name + "\n 반응 시간: " + "%02d.%02d" % (
                            time_diff.seconds, time_diff.microseconds / 1000))
                        error_cnt = error_cnt + 1
                        total_cnt = total_cnt + 1

                        self.label.setText(self.label.text() + "\n" + "누적 오입력 횟수: " + str(error_cnt) + " 회")
                    elif input_cnt > 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "이미 올바른 기어 변경을 했습니다.")

                    self.p_btn.setEnabled(True)
                    self.r_btn.setEnabled(False)
                    self.n_btn.setEnabled(False)
                    self.d_btn.setEnabled(False)
                elif event.name == self.key_r:
                    if disp_gear == 'R' and input_cnt == 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "기어: R단 | 반응 시간: " + "%02d.%02d" % (
                        time_diff.seconds, time_diff.microseconds / 1000))
                        react_time_list.append(float("%02d.%02d" % (time_diff.seconds, time_diff.microseconds / 1000)))
                        input_cnt = input_cnt + 1
                        total_cnt = total_cnt + 1

                    elif disp_gear != 'R':
                        text = self.label.text()
                        self.label.setText(
                            text + "\n" + "올바르지 않은 기어 입력입니다. 입력 키: " + event.name + "\n 반응 시간: " + "%02d.%02d" % (
                            time_diff.seconds, time_diff.microseconds / 1000))

                        error_cnt = error_cnt + 1
                        total_cnt = total_cnt + 1
                        self.label.setText(self.label.text() + "\n" + "누적 오입력 횟수: " + str(error_cnt) + " 회")
                    elif input_cnt > 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "이미 올바른 기어 변경을 했습니다.")

                    self.p_btn.setEnabled(False)
                    self.r_btn.setEnabled(True)
                    self.n_btn.setEnabled(False)
                    self.d_btn.setEnabled(False)
                elif event.name == self.key_n:
                    if disp_gear == 'N' and input_cnt == 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "기어: N단 | 반응 시간: " + "%02d.%02d" % (
                        time_diff.seconds, time_diff.microseconds / 1000))
                        react_time_list.append(float("%02d.%02d" % (time_diff.seconds, time_diff.microseconds / 1000)))
                        input_cnt = input_cnt + 1
                        total_cnt = total_cnt + 1

                    elif disp_gear != 'N':
                        text = self.label.text()
                        self.label.setText(
                            text + "\n" + "올바르지 않은 기어 입력입니다. 입력 키: " + event.name + "\n 반응 시간: " + "%02d.%02d" % (
                            time_diff.seconds, time_diff.microseconds / 1000))

                        total_cnt = total_cnt + 1
                        error_cnt = error_cnt + 1

                        self.label.setText(self.label.text() + "\n" + "누적 오입력 횟수: " + str(error_cnt) + " 회")
                    elif input_cnt > 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "이미 올바른 기어 변경을 했습니다.")

                    self.p_btn.setEnabled(False)
                    self.r_btn.setEnabled(False)
                    self.n_btn.setEnabled(True)
                    self.d_btn.setEnabled(False)
                elif event.name == self.key_d:
                    if disp_gear == 'D' and input_cnt == 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "기어: D단 | 반응 시간: " + "%02d.%02d" % (
                        time_diff.seconds, time_diff.microseconds / 1000))
                        react_time_list.append(float("%02d.%02d" % (time_diff.seconds, time_diff.microseconds / 1000)))
                        input_cnt = input_cnt + 1
                        total_cnt = total_cnt + 1

                    elif disp_gear != 'D':
                        text = self.label.text()
                        self.label.setText(
                            text + "\n" + "올바르지 않은 기어 입력입니다. 입력 키: " + event.name + "\n 반응 시간: " + "%02d.%02d" % (
                            time_diff.seconds, time_diff.microseconds / 1000))

                        error_cnt = error_cnt + 1
                        total_cnt = total_cnt + 1
                        self.label.setText(self.label.text() + "\n" + "누적 오입력 횟수: " + str(error_cnt) + " 회")
                    elif input_cnt > 0:
                        text = self.label.text()
                        self.label.setText(text + "\n" + "이미 올바른 기어 변경을 했습니다.")

                    self.p_btn.setEnabled(False)
                    self.r_btn.setEnabled(False)
                    self.n_btn.setEnabled(False)
                    self.d_btn.setEnabled(True)

    def setGrabbing(self, enable):

        key_set_index = self.key_set_combo.currentIndex()

        key_set = self.key_set_list[key_set_index]

        self.key_p = key_set.get('P')
        self.key_r = key_set.get('R')
        self.key_n = key_set.get('N')
        self.key_d = key_set.get('D')

        global opener

        if enable:
            opener.start()

            self.start_btn.setText('stop')
            # on_press returns a hook that can be used to "disconnect" the callback
            # function later, if required

            self.label.setText("Test Start: Subject_%d" % self.subject_index)

            self.hook = keyboard.on_press(self.keyboardEventReceived)

        else:
            opener.end()

            self.start_btn.setText('start')

            label_input_text = self.label.text()

            global error_cnt
            global total_cnt
            global react_time_list

            error_rate = round(error_cnt / total_cnt, 3)

            label_input_text = label_input_text + "\n" + "오입력 비율: " + str(error_rate * 100) + "% (" + str(
                error_cnt) + "/" + str(total_cnt) + ")\n"

            react_time_sum = 0.00

            for i in range(0, len(react_time_list)):
                react_time_sum = react_time_sum + react_time_list[i]

            label_input_text = label_input_text + "평균 반응 시간: " + str(round(react_time_sum / 6, 3)) + "s"
            self.label.setText("Waiting for start...")

            now = time.localtime()
            time_format_to_min = "%04d년%02d월%02d일_%02d시%02d분_%s" % (
                now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, self.key_set_combo.currentText())

            new_dir_path = "./INU_test"

            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)

            f = open("./INU_test/" + time_format_to_min + "_subject_%d.txt" % self.subject_index, 'w')

            f.write(label_input_text)

            f.close()

            self.subject_index = self.subject_index + 1

            keyboard.unhook(self.hook)

            error_cnt = 0

    def uiComponents(self):

        self.label = ScrollLabel(self)

        # setting geometry to the label
        self.label.setGeometry(5, 5, 400, 500)

        # setting alignment to the label
        self.label.setAlignment(Qt.AlignLeft)

        self.start_btn = QPushButton("START", self)
        self.start_btn.resize(400, 100)

        c_effect = QGraphicsColorizeEffect()
        c_effect.setColor(Qt.blue)
        self.start_btn.setGraphicsEffect(c_effect)

        self.start_btn.setCheckable(True)
        self.start_btn.toggled.connect(self.setGrabbing)

        self.p_btn = QPushButton("P", self)
        self.p_btn.setCheckable(True)
        self.p_btn.setMaximumWidth(100)
        self.p_btn.setMaximumHeight(100)

        self.r_btn = QPushButton("R", self)
        self.r_btn.setCheckable(True)
        self.r_btn.setMaximumWidth(100)
        self.r_btn.setMaximumHeight(100)

        self.n_btn = QPushButton("N", self)
        self.n_btn.setCheckable(True)
        self.n_btn.setMaximumWidth(100)
        self.n_btn.setMaximumHeight(100)

        self.d_btn = QPushButton("D", self)
        self.d_btn.setCheckable(True)
        self.d_btn.setMaximumWidth(100)
        self.d_btn.setMaximumHeight(100)

        self.key_set_combo = QComboBox()

        for i in range(1, len(self.key_set_list) + 1):
            self.key_set_combo.addItem("%d번 버튼 세팅" % i)

        self.h_sub_wrap2 = QHBoxLayout()
        self.h_sub_wrap2.addWidget(self.key_set_combo)

        self.v_wrap1 = QVBoxLayout()
        self.v_wrap1.addWidget(self.label)
        self.v_wrap1.addWidget(self.start_btn)
        self.v_wrap1.addLayout(self.h_sub_wrap2)

        self.v_wrap2 = QVBoxLayout()
        self.v_wrap2.addLayout(self.h_sub_wrap2)

        self.v_sub_wrap1 = QVBoxLayout()
        self.v_sub_wrap1.addWidget(self.p_btn)
        self.v_sub_wrap1.addWidget(self.r_btn)
        self.v_sub_wrap1.addWidget(self.n_btn)
        self.v_sub_wrap1.addWidget(self.d_btn)

        self.h_sub_wrap = QHBoxLayout()
        self.h_sub_wrap.addLayout(self.v_sub_wrap1)

        self.v_wrap2.addLayout(self.h_sub_wrap)

        self.h_wrap = QHBoxLayout()
        self.h_wrap.addLayout(self.v_wrap1)
        self.h_wrap.addLayout(self.v_wrap2)

        self.setLayout(self.h_wrap)


class PicWindow(QWidget):
    full_screen_toggle = False

    def __init__(self):
        super().__init__()

        # setting title
        self.v_wrap = None
        self.setWindowTitle("Case Window")

        # setting geometry
        self.setGeometry(300, 100, 600, 700)

        self.multi = MultiThread(self)

        self.ui_components()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            if self.full_screen_toggle is False:
                self.showFullScreen()
                self.full_screen_toggle = True

            elif self.full_screen_toggle is True:
                self.setWindowFlag(Qt.WindowTitleHint)
                self.showNormal()
                self.full_screen_toggle = False

    def ui_components(self):
        self.v_wrap = QVBoxLayout(self)

        self.img_label = QLabel()

        self.img_label.setFont(QFont('Arial', 25))

        self.img_label.setText("Waiting for start...")

        self.img_label.setAlignment(Qt.AlignCenter)

        self.v_wrap.addWidget(self.img_label)

        self.setLayout(self.v_wrap)

        self.table_widget = QTableWidget(self)

        self.table_widget.setStyleSheet("QTableWidget"
                                 "{"
                                 "border : 2px solid black;"
                                 "gridline-color: #000000;"
                                 "background : white;"
                                 "}")

        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table_widget.setRowCount(2)
        self.table_widget.setColumnCount(3)

        self.table_widget.resize(300, 80)

        self.table_widget.verticalHeader().hide()
        self.table_widget.horizontalHeader().hide()

        self.table_widget.setColumnWidth(0, 0)
        self.table_widget.setColumnWidth(1, int(self.table_widget.width()/2 - 2))
        self.table_widget.setColumnWidth(2, int(self.table_widget.width()/2 - 2))

        self.table_widget.setRowHeight(0, int(self.table_widget.height() - 52))
        self.table_widget.setRowHeight(1, int(self.table_widget.height() - 32))

        arrow = QPixmap('./arrow.png')
        self.arrow_image = QLabel(self.table_widget)
        self.arrow_image.setPixmap(arrow)
        self.arrow_image.setFixedSize(arrow.size())

        self.arrow_image.move(int(self.table_widget.width()/2 - 30), int(self.table_widget.height() - 50))

        font = QFont('Arial', 14)
        font.setBold(True)

        item1 = QTableWidgetItem("현재 위치")
        item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item1.setFont(font)

        item2 = QTableWidgetItem("다음 위치")
        item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item2.setFont(font)

        item3 = QTableWidgetItem("P [주차]")
        item3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item3.setFont(QFont('Arial', 16))
        item3.setForeground(QBrush(Qt.blue))

        item4 = QTableWidgetItem("N [중립]")
        item4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item4.setFont(QFont('Arial', 16))
        item4.setForeground(QBrush(Qt.red))

        self.table_widget.setItem(0, 1, item1)
        self.table_widget.setItem(0, 2, item2)
        self.table_widget.setItem(1, 1, item3)
        self.table_widget.setItem(1, 2, item4)

        self.table_widget.move(100, 100)


        # self.img_label.setPixmap(QPixmap("C:/Task/Change_D.jpg"))



    def start(self):
        self.multi.start()

        # start_gear_int = random.randrange(1, 4)
        #
        # global start_gear
        #
        # if start_gear_int == 1:
        #     start_gear = 'D'
        # elif start_gear_int == 2:
        #     start_gear = 'R'
        # elif start_gear_int == 3:
        #     start_gear = 'P'
        # else:
        #     start_gear = 'N'
        #
        # file_name = "./Task/Now_" + start_gear + ".PNG"
        #
        # self.img_label.setPixmap(QPixmap(file_name))
        self.img_label.setText("잠시후 테스트가 시작됩니다.")

    def end(self):
        self.multi.end()
        self.img_label.setText("Waiting for start...")


class MultiThread(QThread):
    end_flag = False

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        #gear_array = ['D', 'N', 'R', 'P']
        gear_array = [
            ['P', 'R'], ['R', 'P'],
            ['P', 'N'], ['N', 'P'],
            ['D', 'N'], ['N', 'D'],
            ['P', 'D'], ['D', 'P'],
            ['R', 'N'], ['N', 'R'],
            ['R', 'D'], ['D', 'R']
        ]

        bin_array = []

        try_num = 24

        global start_gear

        last_gear_picked = ''

        time_limit = 60

        while try_num > 0:

            if len(gear_array) == 0:
                gear_array = bin_array

            rand_idx = random.randrange(len(gear_array))

            gear_picked = gear_array[rand_idx]

            if gear_picked[0] == last_gear_picked:
                continue

            bin_array.append(gear_picked)

            # if gear_picked == last_gear_picked:
            #     continue
            # else:
            #     last_gear_picked = gear_picked

            global disp_gear

            for j in gear_picked:
                time.sleep(1)

                inter0 = random.randrange(3, 5)

                time.sleep(inter0)

                disp_gear = j

                self.parent.img_label.setPixmap(QPixmap("./Task/Change_%s.PNG" % disp_gear))

                global input_cnt

                input_cnt = 0

                global time_set

                time_set = datetime.datetime.now()

                while input_cnt == 0:
                    useless = 0

                self.parent.img_label.setPixmap(QPixmap("./Task/Now_%s.PNG" % disp_gear))

                try_num = try_num - 1

            last_gear_picked = gear_picked[1]
            gear_array.pop(rand_idx)

        self.parent.img_label.setText("테스트가 종료되었습니다.")

    def end(self):
        self.end_flag = True
        self.terminate()


if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)

    window = Window()

    pic_window = PicWindow()

    # start the app
    sys.exit(App.exec())
