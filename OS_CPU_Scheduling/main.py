''' 
    
            Copyright 2021 Ryan Christopher D. Bahillo

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
Operating System - CPU Scheduling

    Single Contiguous Memory Management


    Partition Allocation Memory Management{
        Static Partition

        Dynamic Partition
            {
                Best Fit
                First Fit
            }
    }
        


    Process Management{
        Non-Preemptive
            {
                First Come First Serve,
                Shortest Job First,
                Priority
            }

        Preemptive
            {
                Priority,
                Shortest Remaining Time First,
                Round Robin
            }
    }

P.S.: Sorry for the big big chunk of code

'''

from PyQt5 import QtCore, QtGui, QtWidgets
import Data.process_management as pm
import Data.single_contiguous as sc
import Data.static_partition as sp
import Data.dynamic_firstfit as df
import Data.dynamic_bestfit as db
import pandas as pd
import itertools
import json
import sys
import fcn
import os
import re


global dark
default_entry = 5
default_partition_count = 3
usrfile_name = 'Untitled'
global pick
pick = 'fcfs'
global D
global X


file = open('usr_preferences.json')
data = json.load(file)

Theme = data['Theme']
Recent_Files = data['Recent Files']
Style = data['Style']

file.close()

if Theme == 'dark':
    dark = True
else:
    dark = False

def suppress_qt_warnings():
   os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
   os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
   os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
   os.environ["QT_SCALE_FACTOR"] = "1"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UI_MainWindow(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 917, 655))
        self.bg.setText("")
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(-20, 70, 561, 131))

        font = QtGui.QFont()
        font.setFamily("Poppins ExtraBold")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)

        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.title_2 = QtWidgets.QLabel(self.centralwidget)
        self.title_2.setGeometry(QtCore.QRect(-20, 20, 561, 131))
        self.title_2.setFont(font)
        self.title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.title_2.setObjectName("title_2")

        self.single_btn = QtWidgets.QPushButton(self.centralwidget)
        self.single_btn.setGeometry(QtCore.QRect(50, 220, 271, 71))

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(12)

        self.single_btn.setFont(font)
        self.single_btn.setObjectName("single_btn")

        self.partition_btn = QtWidgets.QPushButton(self.centralwidget)
        self.partition_btn.setGeometry(QtCore.QRect(50, 360, 271, 71))
        self.partition_btn.setFont(font)
        
        
        self.partition_btn.setObjectName("partition_btn")
        self.process_btn = QtWidgets.QPushButton(self.centralwidget)
        self.process_btn.setGeometry(QtCore.QRect(50, 500, 271, 71))

        self.process_btn.setFont(font)
        self.process_btn.setObjectName("process_btn")

        self.static_btn = QtWidgets.QPushButton(self.centralwidget)
        self.static_btn.setGeometry(QtCore.QRect(50, 360, 131, 71))

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(12)

        self.static_btn.setFont(font)
        self.static_btn.setObjectName("static_btn")

        self.dynamic_btn = QtWidgets.QPushButton(self.centralwidget)
        self.dynamic_btn.setGeometry(QtCore.QRect(190, 360, 131, 71))
        self.dynamic_btn.setFont(font)
        self.dynamic_btn.setObjectName("dynamic_btn")

        self.theme_btn = QtWidgets.QPushButton(self.centralwidget)
        self.theme_btn.setGeometry(QtCore.QRect(765, 187, 20, 20))
        self.theme_btn.setText("")
        self.theme_btn.setFlat(True)
        self.theme_btn.setObjectName("theme_btn")

        self.bg.raise_()
        self.title.raise_()
        self.title_2.raise_()
        self.single_btn.raise_()
        self.process_btn.raise_()
        self.static_btn.raise_()
        self.dynamic_btn.raise_()
        self.partition_btn.raise_()
        self.theme_btn.raise_()

        global dark
        if dark:
            self.dark_theme()
        else:
            self.light_theme()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CPU Scheduling Simulator"))
        self.title.setText(_translate("MainWindow", "SIMULATOR"))
        self.title_2.setText(_translate("MainWindow", "CPU SCHEDULING"))
        self.single_btn.setText(_translate("MainWindow", "Single Contiguous"))
        self.partition_btn.setText(_translate("MainWindow", "Partitioned Allocation"))
        self.process_btn.setText(_translate("MainWindow", "Process Management"))
        self.static_btn.setText(_translate("MainWindow", "Static"))
        self.dynamic_btn.setText(_translate("MainWindow", "Dynamic"))

        self.bg.installEventFilter(self)
        self.partition_btn.installEventFilter(self)

        self.theme_btn.clicked.connect(self.toggle_theme)

        self.single_btn.clicked.connect(self.goto_single_contiguous)
        self.static_btn.clicked.connect(self.goto_static_partition)
        self.dynamic_btn.clicked.connect(self.goto_dynamic_partition)
        self.process_btn.clicked.connect(self.goto_process_management)

    def dark_theme(self):
        global dark
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette().Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette().AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette().ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette().Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)
        self.theme_btn.setToolTip('---> Set Light')  
        self.bg.setPixmap(QtGui.QPixmap(resource_path("Images\Startup_window_bg_black.png")))

        self.theme_btn.setStyleSheet("QPushButton {border-radius: 10px}\
                                      QPushButton::pressed {background-color : #D0AC5F}")

        self.single_btn.setStyleSheet("QPushButton {background-color: #CF8400; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")

        self.partition_btn.setStyleSheet("QPushButton {background-color: green; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")

        self.static_btn.setStyleSheet("QPushButton {background-color: green; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")

        self.dynamic_btn.setStyleSheet("QPushButton {background-color: green; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")
        
        self.process_btn.setStyleSheet("QPushButton {background-color: #006ECF; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")

        with open("usr_preferences.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["Theme"] = "dark"

        with open("usr_preferences.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)

        self.dark_theme_enabled = True
        dark = True

    def light_theme(self):
        global dark
        palette = QtGui.QPalette()
        app.setPalette(palette)
        self.bg.setPixmap(QtGui.QPixmap(resource_path("Images\Startup_window_bg_white.png")))
        self.theme_btn.setToolTip('---> Set Dark')  

        self.theme_btn.setStyleSheet("QPushButton {border-radius: 10px}\
                                      QPushButton::pressed {background-color : #016BD8}")
        
        self.single_btn.setStyleSheet("QPushButton {background-color: orange; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")
        
        self.partition_btn.setStyleSheet("QPushButton {background-color: lightgreen; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")
        
        self.static_btn.setStyleSheet("QPushButton {background-color: lightgreen; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")

        self.dynamic_btn.setStyleSheet("QPushButton {background-color: lightgreen; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")
        
        self.process_btn.setStyleSheet("QPushButton {background-color: lightblue; border-style: outset; border-width: \
                                        2px; border-radius: 15px; border-color: black; padding: 4px}\
                                        \
                                        QPushButton::pressed {background-color : white}")
        
        with open("usr_preferences.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["Theme"] = "light"

        with open("usr_preferences.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)

        self.dark_theme_enabled = False
        dark = False
    
    def toggle_theme(self):
        global dark
        if dark == True:
            self.light_theme()
        else:
            self.dark_theme()
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter:
            if type(object).__name__ == 'QPushButton':
                self.partition_btn.hide()
            else:
                self.partition_btn.show()
                return False
            return True

        elif event.type() == QtCore.QEvent.Leave:
            if type(object).__name__ == 'QLabel':
                self.partition_btn.show()
        return False
        
    def goto_single_contiguous(self):
        self.new_window = MyWindow()
        self.activate_window = SC_InputWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()
    
    def goto_static_partition(self):
        self.new_window = MyWindow()
        self.activate_window = SP_InputWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()
    
    def goto_dynamic_partition(self):
        self.new_window = MyWindow()
        self.activate_window = DP_InputWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()
    
    def goto_process_management(self):
        self.new_window = MyWindow()
        self.activate_window = PM_InputWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()




# Single Contiguous
class SC_InputWindow:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.job_entries = {}
        self.size_entries = {}
        self.arrival_entries = {}
        self.run_entries = {}
        self.csv_loaded_successful = False
        self.active_file = ''
        self.max_size = 0
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 630)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_job_details = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_job_details.setGeometry(QtCore.QRect(250, 14, 581, 561))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.Group_job_details.setFont(font)
        self.Group_job_details.setObjectName("Group_job_details")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Group_job_details)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(17, 50, 541, 468))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 10, 25, 10)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.job_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.job_label.sizePolicy().hasHeightForWidth())
        self.job_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.job_label.setFont(font)
        self.job_label.setAlignment(QtCore.Qt.AlignCenter)
        self.job_label.setObjectName("job_label")
        self.horizontalLayout_3.addWidget(self.job_label)
        self.size_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_label.sizePolicy().hasHeightForWidth())
        self.size_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.size_label.setFont(font)
        self.size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.size_label.setObjectName("size_label")
        self.horizontalLayout_3.addWidget(self.size_label)
        self.arrival_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_label.sizePolicy().hasHeightForWidth())
        self.arrival_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.arrival_label.setFont(font)
        self.arrival_label.setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_label.setObjectName("arrival_label")
        self.horizontalLayout_3.addWidget(self.arrival_label)
        self.runtime_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runtime_label.sizePolicy().hasHeightForWidth())
        self.runtime_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.runtime_label.setFont(font)
        self.runtime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.runtime_label.setObjectName("runtime_label")
        self.horizontalLayout_3.addWidget(self.runtime_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMouseTracking(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(3)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 516, 405))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setHorizontalSpacing(40)
        self.gridLayout.setVerticalSpacing(55)
        self.gridLayout.setObjectName("gridLayout")

        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.add_entry_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.add_entry_btn.setGeometry(QtCore.QRect(520, 520, 41, 41))
        self.add_entry_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/plus-black-symbol.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_entry_btn.setIcon(icon)
        self.add_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.add_entry_btn.setCheckable(False)
        self.add_entry_btn.setDefault(False)
        self.add_entry_btn.setFlat(True)
        self.add_entry_btn.setObjectName("add_entry_btn")
        self.rmv_entry_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.rmv_entry_btn.setGeometry(QtCore.QRect(470, 520, 41, 41))
        self.rmv_entry_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rmv_entry_btn.setIcon(icon1)
        self.rmv_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.rmv_entry_btn.setCheckable(False)
        self.rmv_entry_btn.setDefault(False)
        self.rmv_entry_btn.setFlat(True)
        self.rmv_entry_btn.setObjectName("rmv_entry_btn")
        self.import_csv_btn = QtWidgets.QPushButton(self.centralwidget)
        self.import_csv_btn.setGeometry(QtCore.QRect(270, 545, 100, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon2)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{job number, job size*, arrival time*, run time*}')
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.line = QtWidgets.QFrame(self.Group_job_details)
        self.line.setGeometry(QtCore.QRect(17, 42, 541, 16))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.Group_job_details)
        self.line_2.setGeometry(QtCore.QRect(8, 50, 20, 40))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.Group_job_details)
        self.line_3.setGeometry(QtCore.QRect(546, 50, 20, 40))
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(3)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.Group_memSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memSize.setGeometry(QtCore.QRect(50, 164, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Group_memSize.setFont(font)
        self.Group_memSize.setObjectName("Group_memSize")
        self.memSize_value = QtWidgets.QSpinBox(self.Group_memSize)
        self.memSize_value.setGeometry(QtCore.QRect(20, 47, 121, 29))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.memSize_value.sizePolicy().hasHeightForWidth())
        self.memSize_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.memSize_value.setFont(font)
        self.memSize_value.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.memSize_value.setAlignment(QtCore.Qt.AlignCenter)
        self.memSize_value.setMaximum(999999999)
        self.memSize_value.setSingleStep(5)
        self.memSize_value.setProperty("value", 0)
        self.memSize_value.setObjectName("memSize_value")
        self.Group_osSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_osSize.setGeometry(QtCore.QRect(50, 314, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Group_osSize.setFont(font)
        self.Group_osSize.setObjectName("Group_osSize")
        self.osSize_value = QtWidgets.QSpinBox(self.Group_osSize)
        self.osSize_value.setGeometry(QtCore.QRect(20, 47, 121, 29))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.osSize_value.sizePolicy().hasHeightForWidth())
        self.osSize_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.osSize_value.setFont(font)
        self.osSize_value.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.osSize_value.setAlignment(QtCore.Qt.AlignCenter)
        self.osSize_value.setMaximum(999999999)
        self.osSize_value.setSingleStep(5)
        self.osSize_value.setProperty("value", 0)
        self.osSize_value.setObjectName("osSize_value")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(783, 590, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_btn.setIcon(icon3)
        self.start_btn.setIconSize(QtCore.QSize(20, 20))
        self.start_btn.setCheckable(False)
        self.start_btn.setAutoDefault(False)
        self.start_btn.setDefault(False)
        self.start_btn.setFlat(True)
        self.start_btn.setObjectName("start_btn")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(0, 590, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.back_btn.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_btn.setIcon(icon4)
        self.back_btn.setIconSize(QtCore.QSize(20, 20))
        self.back_btn.setCheckable(False)
        self.back_btn.setAutoDefault(False)
        self.back_btn.setDefault(False)
        self.back_btn.setFlat(True)
        self.back_btn.setObjectName("back_btn")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 21))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.make_default_entry(default_entry)
        self.button_state()
        self.entry_detail_state()
        self.memSize_value.textChanged.connect(self.entry_detail_state)
        self.osSize_value.textChanged.connect(self.entry_detail_state)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Single Contiguous"))
        self.Group_job_details.setTitle(_translate("MainWindow", "Job Details"))
        self.job_label.setText(_translate("MainWindow", "Job"))
        self.size_label.setText(_translate("MainWindow", "Size"))
        self.arrival_label.setText(_translate("MainWindow", "Arrival time"))
        self.runtime_label.setText(_translate("MainWindow", "Run time"))

        self.import_csv_btn.setText(_translate("MainWindow", "  Import CSV"))
        self.Group_memSize.setTitle(_translate("MainWindow", "Memory Size"))
        self.Group_osSize.setTitle(_translate("MainWindow", "OS Size"))
        self.start_btn.setText(_translate("MainWindow", "  Start"))
        self.back_btn.setText(_translate("MainWindow", "  Back"))

        self.start_btn.clicked.connect(self.start)
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.add_entry_btn.clicked.connect(self.add_entry)
        self.rmv_entry_btn.clicked.connect(self.remove_entry)

        self.back_btn.clicked.connect(self.back_to_start_up)

    def back_to_start_up(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def message_to_user(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setText("Sorry not available right now, we're still working on this.      ")
        info.setWindowTitle("Info")
        info.exec_()

    def make_default_entry(self, default_entry):
        for _ in range(default_entry):
            self.add_entry()

    def add_entry(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Job No.
        self.job_entries[f"job{len(self.job_entries)+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.job_entries[f"job{len(self.job_entries)}"].setText(f"{len(self.job_entries)}")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.job_entries[f"job{len(self.job_entries)}"].sizePolicy().hasHeightForWidth())
        self.job_entries[f"job{len(self.job_entries)}"].setSizePolicy(sizePolicy)
        self.job_entries[f"job{len(self.job_entries)}"].setFont(font)
        self.job_entries[f"job{len(self.job_entries)}"].setScaledContents(False)
        self.job_entries[f"job{len(self.job_entries)}"].setAlignment(QtCore.Qt.AlignCenter)
        self.job_entries[f"job{len(self.job_entries)}"].setObjectName(f"job{len(self.job_entries)}")
        self.gridLayout.addWidget(self.job_entries[f"job{len(self.job_entries)}"], len(self.job_entries), 0, 1, 1)
        
    #Size
        self.size_entries[f'size{len(self.size_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_entries[f'size{len(self.size_entries)}'].sizePolicy().hasHeightForWidth())
        self.size_entries[f'size{len(self.size_entries)}'].setSizePolicy(sizePolicy)
        self.size_entries[f'size{len(self.size_entries)}'].setFont(font)
        self.size_entries[f'size{len(self.size_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.size_entries[f'size{len(self.size_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.size_entries[f'size{len(self.size_entries)}'].setMaximum(self.memSize_value.value() - self.osSize_value.value())
        self.size_entries[f'size{len(self.size_entries)}'].setSingleStep(5)
        self.size_entries[f'size{len(self.size_entries)}'].setProperty("value", 0)
        self.size_entries[f'size{len(self.size_entries)}'].setObjectName(f'size{len(self.size_entries)}')
        self.gridLayout.addWidget(self.size_entries[f'size{len(self.size_entries)}'], len(self.size_entries), 1, 1, 1)
        
    #Arrival
        self.arrival_entries[f'arrival{len(self.arrival_entries)+1}'] = QtWidgets.QTimeEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{len(self.arrival_entries)}'].sizePolicy().hasHeightForWidth())
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setSizePolicy(sizePolicy)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setDisplayFormat("h:mm")
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setFont(font)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setObjectName(f'arrival{len(self.arrival_entries)}')
        self.gridLayout.addWidget(self.arrival_entries[f'arrival{len(self.arrival_entries)}'], len(self.arrival_entries), 2, 1, 1)
        
    #Run
        self.run_entries[f'run{len(self.run_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_entries[f'run{len(self.run_entries)}'].sizePolicy().hasHeightForWidth())
        self.run_entries[f'run{len(self.run_entries)}'].setSizePolicy(sizePolicy)
        self.run_entries[f'run{len(self.run_entries)}'].setFont(font)
        self.run_entries[f'run{len(self.run_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.run_entries[f'run{len(self.run_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.run_entries[f'run{len(self.run_entries)}'].setMaximum(999999999)
        self.run_entries[f'run{len(self.run_entries)}'].setSingleStep(5)
        self.run_entries[f'run{len(self.run_entries)}'].setProperty("value", 0)
        self.run_entries[f'run{len(self.run_entries)}'].setObjectName(f'run{len(self.run_entries)}')
        self.gridLayout.addWidget(self.run_entries[f'run{len(self.run_entries)}'], len(self.run_entries), 3, 1, 1)

        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()

    def remove_entry(self):
        self.job_entries[f"job{len(self.job_entries)}"].hide()
        self.size_entries[f'size{len(self.size_entries)}'].hide()
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].hide()
        self.run_entries[f'run{len(self.run_entries)}'].hide()

        del self.job_entries[f"job{len(self.job_entries)}"]
        del self.size_entries[f'size{len(self.size_entries)}']
        del self.arrival_entries[f'arrival{len(self.arrival_entries)}']
        del self.run_entries[f'run{len(self.run_entries)}']
        
        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()
    
    def scroll(self):
        item = self.ListWidget.findItems('ITEM-0011', QtCore.Qt.MatchRegExp)[0]
        item.setSelected(True)
        self.ListWidget.scrollToItem(item, QtGui.QAbstractItemView.PositionAtTop)

    def button_state(self):
        if len(self.job_entries) == 1:
            self.rmv_entry_btn.setEnabled(False)
        else:
            self.rmv_entry_btn.setEnabled(True)
    
    def make_import_btn(self):
        self.import_csv_btn = QtWidgets.QPushButton(self.centralwidget)
        self.import_csv_btn.setGeometry(QtCore.QRect(270, 535, 100, 20))
        self.import_csv_btn.setText("  Import CSV")
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{job number, job size*, arrival time*, run time*}')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon2)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.import_csv_btn.show()
    
    def make_cancel_csv_btn(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)

        self.file_name_label = QtWidgets.QLabel(self.centralwidget)
        self.file_name_label.setFont(font)
        self.file_name_label.setObjectName('file_name_label')
        self.file_name_label.setGeometry(QtCore.QRect(302, 535, 100, 20))
        self.file_name_label.setText(self.active_file)
        self.file_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_name_label.adjustSize()
        self.file_name_label.show()

        self.cancel_csv_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_csv_btn.setGeometry(QtCore.QRect(270, 528, 32, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_csv_btn.sizePolicy().hasHeightForWidth())
        self.cancel_csv_btn.setSizePolicy(sizePolicy)
        self.cancel_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        
        self.cancel_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon_red.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_csv_btn.setIcon(icon2)
        self.cancel_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.cancel_csv_btn.setCheckable(False)
        self.cancel_csv_btn.setDefault(False)
        self.cancel_csv_btn.setFlat(True)
        self.cancel_csv_btn.setObjectName("cancel_csv_btn")
        self.cancel_csv_btn.clicked.connect(self.cancel_csv)
        self.cancel_csv_btn.show()

    def cancel_csv(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to remove this file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            print('Yes  ')
            self.cancel_csv_btn.hide()
            self.file_name_label.hide()
            del self.cancel_csv_btn
            del self.file_name_label

            for _ in range(len(self.job_entries)):
                    self.remove_entry()
            self.make_default_entry(default_entry)
            self.entry_detail_state()

            self.make_import_btn()
            self.max_size = 0
            self.memSize_value.textChanged.connect(self.entry_detail_state)
            self.osSize_value.textChanged.connect(self.entry_detail_state)
            self.add_entry_btn.setEnabled(True)
            self.rmv_entry_btn.setEnabled(True)
            self.csv_loaded_successful = False

    def getFileDir(self):
        file_filter = '*.csv'
        response = QtWidgets.QFileDialog.getOpenFileNames(
            parent = QtWidgets.QWidget(),
            caption='Select a data file',
            directory = os.getcwd(),
            filter=file_filter
        )
        self.active_file = response[0][0].split('/')[-1]
        return response[0][0]

    def import_csv(self):
        try:
            fileDir = self.getFileDir()
            csv = pd.read_csv(fileDir)
            column_name = list(csv.columns)
            jobs = csv[column_name[0]].tolist()
            job_size = csv[column_name[1]].tolist()
            arrival_time = csv[column_name[2]].tolist()
            run_time = csv[column_name[3]].tolist()

            for _ in range(len(self.job_entries)):
                self.remove_entry()
            self.import_csv_btn.hide()
            del self.import_csv_btn
            self.make_cancel_csv_btn()
            self.load_csv_to_window(jobs, job_size, arrival_time, run_time)

        except IndexError:
            print('No file selected')

    def load_csv_to_window(self, j, s, a, r):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Job No.
        for i in range(len(a)):
            self.job_entries[f"job{i+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.job_entries[f"job{i+1}"].setText(f"{i+1}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.job_entries[f"job{i+1}"].sizePolicy().hasHeightForWidth())
            self.job_entries[f"job{i+1}"].setSizePolicy(sizePolicy)
            self.job_entries[f"job{i+1}"].setFont(font)
            self.job_entries[f"job{i+1}"].setScaledContents(False)
            self.job_entries[f"job{i+1}"].setAlignment(QtCore.Qt.AlignCenter)
            self.job_entries[f"job{i+1}"].setObjectName(f"job{i+1}")
            self.gridLayout.addWidget(self.job_entries[f"job{i+1}"], i+1, 0, 1, 1)
    #Size
        for i in range(len(a)):
            self.size_entries[f'size{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.size_entries[f'size{i+1}'].setText(f"{s[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.size_entries[f'size{i+1}'].sizePolicy().hasHeightForWidth())
            self.size_entries[f'size{i+1}'].setSizePolicy(sizePolicy)
            self.size_entries[f'size{i+1}'].setFont(font)
            self.size_entries[f'size{i+1}'].setScaledContents(False)
            self.size_entries[f'size{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.size_entries[f'size{i+1}'].setObjectName(f"size{i+1}")
            self.gridLayout.addWidget(self.size_entries[f'size{i+1}'], i+1, 1, 1, 1)
    #Arrival
        for i in range(len(a)):
            self.arrival_entries[f'arrival{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.arrival_entries[f'arrival{i+1}'].setText(f"{a[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{i+1}'].sizePolicy().hasHeightForWidth())
            self.arrival_entries[f'arrival{i+1}'].setSizePolicy(sizePolicy)
            self.arrival_entries[f'arrival{i+1}'].setFont(font)
            self.arrival_entries[f'arrival{i+1}'].setScaledContents(False)
            self.arrival_entries[f'arrival{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.arrival_entries[f'arrival{i+1}'].setObjectName(f"arrival{i+1}")
            self.gridLayout.addWidget(self.arrival_entries[f'arrival{i+1}'], i+1, 2, 1, 1)
    #Run
        for i in range(len(a)):
            self.run_entries[f'run{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.run_entries[f'run{i+1}'].setText(f"{r[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.run_entries[f'run{i+1}'].sizePolicy().hasHeightForWidth())
            self.run_entries[f'run{i+1}'].setSizePolicy(sizePolicy)
            self.run_entries[f'run{i+1}'].setFont(font)
            self.run_entries[f'run{i+1}'].setScaledContents(False)
            self.run_entries[f'run{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.run_entries[f'run{i+1}'].setObjectName(f"run{i+1}")
            self.gridLayout.addWidget(self.run_entries[f'run{i+1}'], i+1, 3, 1, 1)

        self.csv_loaded_successful = True
        self.memSize_value.disconnect()
        self.osSize_value.disconnect()

        self.memSize_value.setMaximum(999999999)
        self.osSize_value.setMaximum(999999999)
        self.Group_job_details.setEnabled(True)
        self.add_entry_btn.setEnabled(False)
        self.rmv_entry_btn.setEnabled(False)
        self.max_size = max(s)

    def entry_detail_state(self):
        if self.memSize_value.value() != 0:
            for i in range(len(self.job_entries)):
                list(self.size_entries.values())[i].setMaximum(self.memSize_value.value() - self.osSize_value.value())
                if list(self.size_entries.values())[i].value() < 0:
                    list(self.size_entries.values())[i].setProperty("value", 0)
            self.Group_job_details.setEnabled(True)
        else:
            self.Group_job_details.setEnabled(False)           
        self.osSize_value.setMaximum(self.memSize_value.value())
            
    
    def start(self):
        print(type(self.size_entries['size1']).__name__, '<----------------------')
        # Validate Inputs
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setIcon(QtWidgets.QMessageBox.Information)
        notify_user.setFont(font)

        err_msg = QtWidgets.QMessageBox()
        err_msg.setIcon(QtWidgets.QMessageBox.Information)
        err_msg.setFont(font)
        
        self.validated = True
        for _ in range(1):
            if self.memSize_value.value() <= self.osSize_value.value():
                self.validated = False
                err_msg.setText('Sizes must be:\nMemory size > OS size > 0      ')
                err_msg.setWindowTitle("Memory Error")
                err_msg.exec_()
                self.memSize_value.setFocus()
                self.memSize_value.selectAll()
                self.Group_job_details.setEnabled(False)
                break
                
            elif self.osSize_value.value() <= 0:
                self.validated = False
                err_msg.setText('Sizes must be:\nMemory size > OS size > 0      ')
                err_msg.setWindowTitle("Memory Error")
                err_msg.exec_()
                self.osSize_value.setFocus()
                self.osSize_value.selectAll()
                self.Group_job_details.setEnabled(False)
                break

            elif self.max_size > (self.memSize_value.value() - self.osSize_value.value()):
                self.validated = False
                err_msg.setText(f'Job sizes must fit !\n ~max={self.max_size}                  ')
                err_msg.setWindowTitle("Size Error")
                err_msg.exec_()
                break

            for i in range(len(self.job_entries)):
                if type(self.size_entries['size1']).__name__ == 'QLabel':
                    if list(self.size_entries.values())[i].text() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.size_entries.values())[i].setFocus()
                        list(self.size_entries.values())[i].selectAll()
                        break
                    if list(self.arrival_entries.values())[i].text().split(':')[0] == '0':
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.arrival_entries.values())[i].setFocus()
                        list(self.arrival_entries.values())[i].selectAll()
                        break
                    if list(self.run_entries.values())[i].text() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.run_entries.values())[i].setFocus()
                        list(self.run_entries.values())[i].selectAll()
                        break
                else:
                    if list(self.size_entries.values())[i].value() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.size_entries.values())[i].setFocus()
                        list(self.size_entries.values())[i].selectAll()
                        yloc = list(self.size_entries.values())[i].y() - list(self.size_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
                    if list(self.arrival_entries.values())[i].text().split(':')[0] == '0':
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.arrival_entries.values())[i].setFocus()
                        list(self.arrival_entries.values())[i].selectAll()
                        yloc = list(self.arrival_entries.values())[i].y() - list(self.arrival_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
                    if list(self.run_entries.values())[i].value() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.run_entries.values())[i].setFocus()
                        list(self.run_entries.values())[i].selectAll()
                        yloc = list(self.run_entries.values())[i].y() - list(self.run_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
        
        if self.validated == False and self.csv_loaded_successful == True:
            self.Group_job_details.setEnabled(True)

    # Export JSON
        if self.validated:
            if type(self.size_entries['size1']).__name__ == 'QLabel':
                dictionary ={
                'Memory size' : self.memSize_value.value(),
                'OS size' : self.osSize_value.value(),
                'Job' : [job.text() for job in self.job_entries.values()],
                'Size' : [int(size.text()) for size in self.size_entries.values()],
                'Arrival time' : [arrival.text() for arrival in self.arrival_entries.values()],
                'Run time' : [int(run.text()) for run in self.run_entries.values()]
                }
            else:
                dictionary ={
                'Memory size' : self.memSize_value.value(),
                'OS size' : self.osSize_value.value(),
                'Job' : [job.text() for job in self.job_entries.values()],
                'Size' : [int(size.value()) for size in self.size_entries.values()],
                'Arrival time' : [arrival.text() for arrival in self.arrival_entries.values()],
                'Run time' : [int(run.value()) for run in self.run_entries.values()]
                }

            if dictionary["Arrival time"] != fcn.sort_time(dictionary["Arrival time"]):
                notify_user.setText('Unsorted arrival detected\n~Inputs are now sorted by arrival !      ')
                notify_user.setWindowTitle("Sort by Arrival")
                notify_user.button
                notify_user.setStandardButtons
                notify_user.exec_()

        # Sort by Arrival
            for i in range(len(dictionary['Arrival time'])-1):
                for j in range(0, len(dictionary['Arrival time'])-i-1):
                    if fcn.to_minutes(dictionary['Arrival time'][j]) > fcn.to_minutes(dictionary['Arrival time'][j+1]):
                        dictionary['Arrival time'][j], dictionary['Arrival time'][j+1] = dictionary['Arrival time'][j+1], dictionary['Arrival time'][j]
                        dictionary['Size'][j], dictionary['Size'][j+1] = dictionary['Size'][j+1], dictionary['Size'][j]
                        dictionary['Run time'][j], dictionary['Run time'][j+1] = dictionary['Run time'][j+1], dictionary['Run time'][j]

            with open(f"{usrfile_name}.json", "w") as outfile:
                json.dump(dictionary, outfile, indent=4)

            global D
            global X
            
            D = dictionary
            X = sc.single_contiguous_EXEC(usrfile_name)
            self.next_window(D, X)
            print('VALIDATAED')

        else:
            print('NOT VALIDATED')
            
    
    def next_window(self, inputs, Data):
        self.newWindow = MyWindow()
        self.second_ui = SC_ProcessWindow(self.newWindow, inputs, Data)
        self.newWindow.show()
        self.MainWindow.hide()

class SC_ProcessWindow:
    V_END = 450
    def __init__(self, MainWindow, inputs, D):
        self.mem_map, self.label, self.message, self.start_time, self.finish, self.cpu_wait = D[0], D[1], D[2], D[3], D[4], D[5]
        self.inputs = inputs
        self.MainWindow = MainWindow
        self.idx = 0
        self.fixed = False
        self.d = {}
        self.labels = {}
        self.mem_labels ={}
        self.end_show = False
        self.error_msg_value = 0
        global dark
        self.dark_theme_enabled = dark
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('SC_icon.png')))
        MainWindow.setFixedSize(917, 630)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_memoryMap = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memoryMap.setGeometry(QtCore.QRect(510, 10, 321, 521))

        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Group_memoryMap.setFont(font)
        self.Group_memoryMap.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Group_memoryMap.setObjectName("Group_memoryMap")
        self.Group_job_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_job_table.setGeometry(QtCore.QRect(20, 150, 451, 291))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_job_table.setFont(font)
        self.Group_job_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_job_table.setCheckable(False)
        self.Group_job_table.setChecked(False)
        self.Group_job_table.setObjectName("Group_job_table")
        self.Job_Table = QtWidgets.QTableWidget(self.Group_job_table)
        self.Job_Table.setGeometry(QtCore.QRect(10, 27, 432, 251))
        self.Job_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Job_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Job_Table.setFont(font)
        self.Job_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Job_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Job_Table.verticalHeader().setVisible(False) # Row Index
        self.Job_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.Job_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        
        self.Job_Table.setAutoScroll(True)
        self.Job_Table.setAlternatingRowColors(True)
        self.Job_Table.setObjectName("Job_Table")
        self.Job_Table.setColumnCount(4)
        self.Job_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(0, item)
        self.Job_Table.setItemDelegateForColumn(0, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(1, item)
        self.Job_Table.setItemDelegateForColumn(1, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(2, item)
        self.Job_Table.setItemDelegateForColumn(2, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(3, item)
        self.Job_Table.setItemDelegateForColumn(3, AlignDelegate(self.Job_Table))
        self.Job_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.Job_Table.horizontalHeaderItem(0).setFont(font)
        self.Job_Table.horizontalHeaderItem(1).setFont(font)
        self.Job_Table.horizontalHeaderItem(2).setFont(font)
        self.Job_Table.horizontalHeaderItem(3).setFont(font)
             
        self.Job_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.verticalHeader().setDefaultSectionSize(44)

        self.Group_osSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_osSize.setGeometry(QtCore.QRect(350, 90, 120, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_osSize.setFont(font)
        self.Group_osSize.setObjectName("Group_osSize")
        self.OS_size_label = QtWidgets.QLabel(self.Group_osSize)
        self.OS_size_label.setEnabled(True)
        self.OS_size_label.setGeometry(QtCore.QRect(10, 18, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.OS_size_label.setFont(font)
        self.OS_size_label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.OS_size_label.setMouseTracking(False)
        self.OS_size_label.setTabletTracking(False)
        self.OS_size_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.OS_size_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.OS_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.OS_size_label.setObjectName("OS_size_label")
        self.Group_memSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memSize.setGeometry(QtCore.QRect(30, 90, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_memSize.setFont(font)
        self.Group_memSize.setFlat(False)
        self.Group_memSize.setCheckable(False)
        self.Group_memSize.setObjectName("Group_memSize")
        self.mem_size_label = QtWidgets.QLabel(self.Group_memSize)
        self.mem_size_label.setGeometry(QtCore.QRect(20, 18, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mem_size_label.setFont(font)
        self.mem_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mem_size_label.setObjectName("mem_size_label")
        self.partition_title = QtWidgets.QLabel(self.centralwidget)
        self.partition_title.setGeometry(QtCore.QRect(20, 22, 451, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.partition_title.setFont(font)
        self.partition_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.partition_title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.partition_title.setLineWidth(1)
        self.partition_title.setAlignment(QtCore.Qt.AlignCenter)
        self.partition_title.setObjectName("partition_title")
        self.prev_button = QtWidgets.QPushButton(self.centralwidget)
        self.prev_button.setGeometry(QtCore.QRect(550, 540, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.prev_button.setFont(font)
        self.prev_button.setObjectName("prev_button")
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(700, 540, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.next_button.setFont(font)
        self.next_button.setObjectName("next_button")
        self.simplify_cbx = QtWidgets.QCheckBox(self.centralwidget)
        self.simplify_cbx.setGeometry(QtCore.QRect(775, 580, 65, 19))
        self.simplify_cbx.setFont(font)
        self.simplify_cbx.setObjectName("simplify_cbx")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 470, 451, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.message_label.setFont(font)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setObjectName("message_label")
        self.horizontalLayout.addWidget(self.message_label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 28))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuHelp.setFont(font)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAbout = QtWidgets.QMenu(self.menuHelp)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAbout.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/message.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAbout.setIcon(icon)
        self.menuAbout.setObjectName("menuAbout")
        self.menuDevelopers = QtWidgets.QMenu(self.menuAbout)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuDevelopers.setFont(font)
        self.menuDevelopers.setObjectName("menuDevelopers")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuAppearance = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance.setFont(font)
        self.menuAppearance.setObjectName("menuAppearance")
        self.menuAppearance_2 = QtWidgets.QMenu(self.menuAppearance)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance_2.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/favorite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAppearance_2.setIcon(icon)
        self.menuAppearance_2.setObjectName("menuAppearance_2")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.toolBar.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setAcceptDrops(False)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setMovable(True)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setIconSize(QtCore.QSize(30, 25))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionHome = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/house_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon)
        self.actionHome.setObjectName("actionHome")
        self.actionLyra = QtWidgets.QAction(MainWindow)
        self.actionLyra.setObjectName("actionLyra")
        self.actionRyan = QtWidgets.QAction(MainWindow)
        self.actionRyan.setObjectName("actionRyan")
        self.actionJoshua = QtWidgets.QAction(MainWindow)
        self.actionJoshua.setObjectName("actionJoshua")
        self.actionLyra_2 = QtWidgets.QAction(MainWindow)
        self.actionLyra_2.setObjectName("actionLyra_2")
        self.actionRyan_2 = QtWidgets.QAction(MainWindow)
        self.actionRyan_2.setObjectName("actionRyan_2")
        self.actionJoshua_2 = QtWidgets.QAction(MainWindow)
        self.actionJoshua_2.setObjectName("actionJoshua_2")
        self.actionKent = QtWidgets.QAction(MainWindow)
        self.actionKent.setObjectName("actionKent")
        self.actionGrant = QtWidgets.QAction(MainWindow)
        self.actionGrant.setObjectName("actionGrant")
        self.actionThis_partition = QtWidgets.QAction(MainWindow)
        self.actionThis_partition.setObjectName("actionThis_partition")
        self.actionHow_to_use = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/idea.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHow_to_use.setIcon(icon)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.actionCSV = QtWidgets.QAction(MainWindow)
        self.actionCSV.setObjectName("actionCSV")
        self.actionPNG = QtWidgets.QAction(MainWindow)
        self.actionPNG.setObjectName("actionPNG")
        self.actionJPEG = QtWidgets.QAction(MainWindow)
        self.actionJPEG.setObjectName("actionJPEG")
        self.actionCSV_2 = QtWidgets.QAction(MainWindow)
        self.actionCSV_2.setObjectName("actionCSV_2")
        self.actionPNG_2 = QtWidgets.QAction(MainWindow)
        self.actionPNG_2.setObjectName("actionPNG_2")
        self.actionJPEG_2 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_2.setObjectName("actionJPEG_2")
        self.actionJPEG_3 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_3.setObjectName("actionJPEG_3")
        self.actionSave_image = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/picture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_image.setIcon(icon1)
        self.actionSave_image.setObjectName("actionSave_image")
        self.actionclose = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionclose.setIcon(icon2)
        self.actionclose.setObjectName("actionclose")
        self.actionExport_csv = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/calendar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport_csv.setIcon(icon3)
        self.actionExport_csv.setObjectName("actionExport_csv")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen_Recent = QtWidgets.QAction(MainWindow)
        self.actionOpen_Recent.setObjectName("actionOpen_Recent")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(resource_path("Icons/write.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon5)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.actionNew.setFont(font)
        self.actionNew.setObjectName("actionNew")
        self.actionDark_Mode = QtWidgets.QAction(MainWindow)
        self.actionDark_Mode.setObjectName("actionDark_Mode")
        self.actionLight_Mode = QtWidgets.QAction(MainWindow)
        self.actionLight_Mode.setObjectName("actionLight_Mode")
        self.actionJump_to = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(resource_path("Icons/clock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJump_to.setIcon(icon6)
        self.actionJump_to.setObjectName("actionJump_to")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(resource_path("Icons/turn_off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon7)
        self.actionExit.setObjectName("actionExit")
        self.actionShow_Summary_Table = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(resource_path("Icons/presentation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Summary_Table.setIcon(icon8)
        self.actionShow_Summary_Table.setObjectName("actionShow_Summary_Table")
        self.menuDevelopers.addAction(self.actionLyra_2)
        self.menuDevelopers.addAction(self.actionRyan_2)
        self.menuDevelopers.addAction(self.actionKent)
        self.menuDevelopers.addAction(self.actionJoshua_2)
        self.menuDevelopers.addAction(self.actionGrant)
        self.menuAbout.addAction(self.actionThis_partition)
        self.menuAbout.addAction(self.menuDevelopers.menuAction())
        self.menuHelp.addAction(self.actionHow_to_use)
        self.menuHelp.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_image)
        self.menuFile.addAction(self.actionExport_csv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionclose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAppearance_2.addAction(self.actionLight_Mode)
        self.menuAppearance_2.addAction(self.actionDark_Mode)
        self.menuAppearance.addAction(self.menuAppearance_2.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAppearance.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionJump_to)
        self.toolBar.addAction(self.actionShow_Summary_Table)

        self.label_zero = QtWidgets.QLabel(self.Group_memoryMap)
        self.label_zero.setText('0')
        self.label_zero.adjustSize()
        self.label_zero.setAlignment(QtCore.Qt.AlignRight)
        self.label_zero.setGeometry(QtCore.QRect(0, 30, 43, 13))
        self.label_zero.setObjectName("label_zero")

        self.label_memory_size = QtWidgets.QLabel(self.Group_memoryMap)
        self.label_memory_size.setText(f'{self.mem_map[0][-1]}')
        self.label_memory_size.adjustSize()
        self.label_memory_size.setAlignment(QtCore.Qt.AlignRight)
        self.label_memory_size.setGeometry(QtCore.QRect(0, self.V_END+40, 43, 13))
        self.label_memory_size.setObjectName("label_memory_size")

        self.v_line = QtWidgets.QFrame(self.Group_memoryMap)
        self.v_line.setGeometry(QtCore.QRect(40, 40, 20, self.V_END))
        self.v_line.setLineWidth(2)
        self.v_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.v_line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.v_line.setObjectName("v_line")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.make_lines(len(self.mem_map[self.idx]))
        self.make_labels(len(self.mem_map[self.idx]))
        self.make_memory_labels(self.mem_map[self.idx], self.fixed)
        self.button_state()
        self.load_job_table()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Single Contiguous"))
        self.Group_memoryMap.setTitle(_translate("MainWindow", "Memory Map"))
        self.Group_job_table.setTitle(_translate("MainWindow", "Job Table"))
        item = self.Job_Table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Job"))
        item = self.Job_Table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Size"))
        item = self.Job_Table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Arrival time"))
        item = self.Job_Table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Run time"))
        self.Group_osSize.setTitle(_translate("MainWindow", "OS Size"))
        self.OS_size_label.setText(_translate("MainWindow", f"{self.inputs['OS size']}"))
        self.Group_memSize.setTitle(_translate("MainWindow", "Memory Size"))
        self.mem_size_label.setText(_translate("MainWindow", f"{self.inputs['Memory size']}"))
        self.partition_title.setText(_translate("MainWindow", "Single Contiguous Memory Management"))
        self.prev_button.setText(_translate("MainWindow", "Prev"))
        self.next_button.setText(_translate("MainWindow", "Next"))
        self.simplify_cbx.setText(_translate("MainWindow", "Simplify"))
        self.message_label.setText(_translate("MainWindow", f"{self.message[0]}"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuDevelopers.setTitle(_translate("MainWindow", "Developers"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAppearance.setTitle(_translate("MainWindow", "View"))
        self.menuAppearance_2.setTitle(_translate("MainWindow", "Theme"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Tool Bar"))
        self.actionHome.setText(_translate("MainWindow", "Home"))
        self.actionLyra.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua.setText(_translate("MainWindow", "Joshua"))
        self.actionLyra_2.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan_2.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua_2.setText(_translate("MainWindow", "Joshua"))
        self.actionKent.setText(_translate("MainWindow", "Kent"))
        self.actionGrant.setText(_translate("MainWindow", "Grant"))
        self.actionThis_partition.setText(_translate("MainWindow", "This partition"))
        self.actionHow_to_use.setText(_translate("MainWindow", "How to use"))
        self.actionCSV.setText(_translate("MainWindow", "CSV"))
        self.actionPNG.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG.setText(_translate("MainWindow", "JPEG"))
        self.actionCSV_2.setText(_translate("MainWindow", "CSV"))
        self.actionPNG_2.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG_2.setText(_translate("MainWindow", "JPEG"))
        self.actionJPEG_3.setText(_translate("MainWindow", "JPEG"))
        self.actionSave_image.setText(_translate("MainWindow", "Save Image"))
        self.actionclose.setText(_translate("MainWindow", "Close"))
        self.actionExport_csv.setText(_translate("MainWindow", "Export (.csv)"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen_Recent.setText(_translate("MainWindow", "Open Recent"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionDark_Mode.setText(_translate("MainWindow", "Dark"))
        self.actionLight_Mode.setText(_translate("MainWindow", "Light"))
        self.actionJump_to.setText(_translate("MainWindow", "Jump to"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionShow_Summary_Table.setText(_translate("MainWindow", "Summary"))
        self.next_button.clicked.connect(self.next_clicked)
        self.prev_button.clicked.connect(self.prev_clicked)
        self.actionJump_to.triggered.connect(self.jump_to)
        self.actionShow_Summary_Table.triggered.connect(self.show_summary_table)
        self.simplify_cbx.stateChanged.connect(self.simplify_mem_map)
        self.actionNew.triggered.connect(self.new_input)
        self.actionDark_Mode.triggered.connect(self.dark_theme)
        self.actionLight_Mode.triggered.connect(self.light_theme)
        self.actionExit.triggered.connect(self.quitting)

        
        self.actionSave_image.triggered.connect(self.message_to_user)
        self.actionExport_csv.triggered.connect(self.message_to_user)
        self.actionOpen.triggered.connect(self.message_to_user)
        self.actionHow_to_use.triggered.connect(self.message_to_user)
        self.actionThis_partition.triggered.connect(self.message_to_user)

        self.actionclose.triggered.connect(self.closing)
        self.actionHome.triggered.connect(self.goto_home)
    
    def goto_home(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def message_to_user(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setText("Sorry not available right now, we're still working on this.      ")
        info.setWindowTitle("Info")
        info.exec_()

    def closing(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('This will bring you to the home window, continue?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.goto_home()
            
    def quitting(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to quit?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            sys.exit()

    def dark_theme(self):
        # Palette to switch to dark colors:
        # app.setStyle("Fusion")
        global dark
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette().Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette().AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette().ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette().Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)
        self.Job_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")

        with open("usr_preferences.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["Theme"] = "dark"

        with open("usr_preferences.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)

        self.dark_theme_enabled = True
        dark = True
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
    
    def light_theme(self):
        global dark
        palette = QtGui.QPalette()
        app.setPalette(palette)
        self.Job_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")

        with open("usr_preferences.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["Theme"] = "light"

        with open("usr_preferences.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
            
        self.dark_theme_enabled = False
        dark = False
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

    def load_job_table(self):
        size = self.inputs['Size']
        arrival = self.inputs['Arrival time']
        run = self.inputs['Run time']
        self.Job_Table.setRowCount(len(size))
        for row in range(len(size)):
            self.Job_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
            self.Job_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(size[row])))
            self.Job_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(arrival[row])))
            self.Job_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(run[row])))

    def simplify_mem_map(self):
        if self.simplify_cbx.isChecked():
            if self.fixed == False:
                self.fixed = True
        else:
            if self.fixed == True:
                self.fixed = False
        self.show_line_LOC(self.mem_map[self.idx], self.fixed)
        self.show_label_LOC(self.mem_map[self.idx], self.fixed)
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

    def button_state(self):
        if self.idx == len(self.mem_map)-1:
            self.next_button.setEnabled(False)
            self.end_show = True
            # self.summaryButton.setStyleSheet("color: blue")
        else:
            self.next_button.setEnabled(True)
        
        if self.idx == 0:
            self.prev_button.setEnabled(False)
        else:
            self.prev_button.setEnabled(True)
        
        # self.summaryButton.setEnabled(self.end_show)

    def new_input(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.Yes)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('New file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.new_window = MyWindow()
            self.activate_window = SC_InputWindow(self.new_window)
            self.new_window.show()
            self.MainWindow.hide()

    def next_clicked(self):
        try:
            self.idx += 1
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
        
        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1
        self.button_state()

    def prev_clicked(self):
        try:
            self.idx -= 1
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1
        self.button_state()

    def show_error_message(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setTextFormat(QtCore.Qt.RichText)
        info.setText("Sorry, an error has occured when I begin to process your data. We're still working on this, please try another input. \
                    <a href='https://www.facebook.com/xtnctx'><br><br>Tell me about the error</br></br></a>    ")
        info.setWindowTitle("Developer message")
        info.exec_()
        info.exec_()

    # Make unique objects returning in different memory location (of Python)
    def make_lines(self, length):
        self.new_mem_map = fcn.margin_memory_loc(self.mem_map[self.idx], self.V_END, y=30, fixed=self.fixed)
        for i in range(length-1):
            self.d[f"self.horizontal_line{i}"] = QtWidgets.QFrame(self.Group_memoryMap)
            self.d[f"self.horizontal_line{i}"].setLineWidth(2)
            self.d[f"self.horizontal_line{i}"].setGeometry(QtCore.QRect(50, self.new_mem_map[i]+20, 251, 16))
            self.d[f"self.horizontal_line{i}"].setFrameShape(QtWidgets.QFrame.HLine)
            self.d[f"self.horizontal_line{i}"].setFrameShadow(QtWidgets.QFrame.Raised)
            self.d[f"self.horizontal_line{i}"].setObjectName("horizontal_line")
        return self.d

    def make_labels(self, length):
        self.new_mem_map = fcn.margin_memory_loc(self.mem_map[self.idx], self.V_END, y=30, fixed=self.fixed)
        for i in range(length-1):
            self.labels[f"self.pointer_label{i}"] = QtWidgets.QLabel(self.Group_memoryMap)
            self.labels[f"self.pointer_label{i}"].setText(f"{self.mem_map[self.idx][i]}")
            self.labels[f"self.pointer_label{i}"].adjustSize()
            self.labels[f"self.pointer_label{i}"].setAlignment(QtCore.Qt.AlignRight)
            self.labels[f"self.pointer_label{i}"].setGeometry(QtCore.QRect(0, self.new_mem_map[i]+20, 43, 13))
            self.labels[f"self.pointer_label{i}"].setObjectName("pointer_label")
        return self.labels
    
    def make_memory_labels(self, mem_map, fixed):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        font.setKerning(True)

        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)
        
        length = len(mem_map)
        for i in range(length):
            self.mem_labels[f"self.memory_label{i}"] = QtWidgets.QLabel(self.Group_memoryMap)
            if 'J' in self.label[self.idx][i]:
                self.mem_labels[f"self.memory_label{i}"].setFont(font)
                self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #6FBE28")
            elif 'Wasted' in self.label[self.idx][i]:
                self.mem_labels[f"self.memory_label{i}"].setFont(font)
                self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #E7766C")
            else:
                if self. dark_theme_enabled: 
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #DBDBDB")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #4F4F4F")
            self.mem_labels[f"self.memory_label{i}"].setText(f"{self.label[self.idx][i]}")
            self.mem_labels[f"self.memory_label{i}"].adjustSize()
            self.mem_labels[f"self.memory_label{i}"].setAlignment(QtCore.Qt.AlignCenter)
            self.mem_labels[f"self.memory_label{i}"].setGeometry(QtCore.QRect(50, self.memory_label_yloc[0][i]+20, 270, 13))
            self.mem_labels[f"self.memory_label{i}"].setObjectName("memory_label")
    
    # Configure assigned variables from dictionary
    def show_line_LOC(self, mem_map, fixed):
        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        # Add missing widget
        if len(self.new_mem_map) > len(self.d)+1:
            for missing in range(len(self.d), len(self.new_mem_map)-1):
                self.d[f"self.horizontal_line{missing}"] = QtWidgets.QFrame(self.Group_memoryMap)
                self.d[f"self.horizontal_line{missing}"].setLineWidth(2)
                self.d[f"self.horizontal_line{missing}"].setGeometry(QtCore.QRect(50, self.new_mem_map[missing]+20, 251, 16))
                self.d[f"self.horizontal_line{missing}"].setFrameShape(QtWidgets.QFrame.HLine)
                self.d[f"self.horizontal_line{missing}"].setFrameShadow(QtWidgets.QFrame.Raised)
                self.d[f"self.horizontal_line{missing}"].setObjectName("horizontal_line")
        
        # Show widget
        d = dict(itertools.islice(self.d.items(), len(self.new_mem_map)-1))
        for i in range(len(d)):
            d[f"self.horizontal_line{i}"].setLineWidth(2)
            d[f"self.horizontal_line{i}"].setGeometry(QtCore.QRect(50, self.new_mem_map[i]+20, 251, 16))
            d[f"self.horizontal_line{i}"].setFrameShape(QtWidgets.QFrame.HLine)
            d[f"self.horizontal_line{i}"].setFrameShadow(QtWidgets.QFrame.Raised)
            d[f"self.horizontal_line{i}"].setObjectName("horizontal_line")
            d[f"self.horizontal_line{i}"].show()

        # Hide the excess widget
        for k in range(len(d), len(self.d)):
            self.d[f"self.horizontal_line{k}"].hide()
    
    def show_label_LOC(self, mem_map, fixed):
        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        if len(self.new_mem_map) > len(self.labels)+1:
            for missing in range(len(self.labels), len(self.new_mem_map)-1):
                self.labels[f"self.pointer_label{missing}"] = QtWidgets.QLabel(self.Group_memoryMap)
                self.labels[f"self.pointer_label{missing}"].setText(f"{mem_map[missing]}")
                self.labels[f"self.pointer_label{missing}"].adjustSize()
                self.labels[f"self.pointer_label{missing}"].setAlignment(QtCore.Qt.AlignRight)
                self.labels[f"self.pointer_label{missing}"].setGeometry(QtCore.QRect(0, self.new_mem_map[missing]+20, 43, 13))
                self.labels[f"self.pointer_label{missing}"].setObjectName("pointer_label")

        p = dict(itertools.islice(self.labels.items(), len(self.new_mem_map)-1))
        for i in range(len(p)):
            p[f"self.pointer_label{i}"].setText(f"{mem_map[i]}")
            p[f"self.pointer_label{i}"].adjustSize()
            p[f"self.pointer_label{i}"].setAlignment(QtCore.Qt.AlignRight)
            p[f"self.pointer_label{i}"].setGeometry(QtCore.QRect(0, self.new_mem_map[i]+20, 43, 13))
            p[f"self.pointer_label{i}"].setObjectName("pointer_label")
            p[f"self.pointer_label{i}"].show()
            
        for k in range(len(p), len(self.labels)):
            self.labels[f"self.pointer_label{k}"].hide()
    
    def show_MMlabel_LOC(self, mem_map, fixed):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        font.setKerning(True)

        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)

        if len(self.memory_label_yloc[0]) > len(self.mem_labels):
            for missing in range(len(self.mem_labels), len(self.memory_label_yloc[0])):
                self.mem_labels[f"self.memory_label{missing}"] = QtWidgets.QLabel(self.Group_memoryMap)
                self.mem_labels[f"self.memory_label{missing}"].setText(f"{self.label[self.idx][missing]}")
                self.mem_labels[f"self.memory_label{missing}"].adjustSize()
                self.mem_labels[f"self.memory_label{missing}"].setAlignment(QtCore.Qt.AlignCenter)
                self.mem_labels[f"self.memory_label{missing}"].setGeometry(QtCore.QRect(50, 
                                self.memory_label_yloc[0][missing]+20, 270, 13))
                self.mem_labels[f"self.memory_label{missing}"].setObjectName("memory_label")
        
        elif len(self.memory_label_yloc[0]) < len(self.mem_labels):
            for k in range(len(self.memory_label_yloc[0]), len(self.mem_labels)):
                self.mem_labels[f"self.memory_label{k}"].hide()
                del self.mem_labels[f"self.memory_label{k}"]

        for i in range(len(self.mem_labels)):
            if 'J' in self.label[self.idx][i]:
                self.mem_labels[f"self.memory_label{i}"].setFont(font)
                self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #6FBE28")
            elif 'Wasted' in self.label[self.idx][i]:
                self.mem_labels[f"self.memory_label{i}"].setFont(font)
                self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #E7766C")
            else:
                if self. dark_theme_enabled: 
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #DBDBDB")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #4F4F4F")
            self.mem_labels[f"self.memory_label{i}"].setText(f"{self.label[self.idx][i]}")
            self.mem_labels[f"self.memory_label{i}"].adjustSize()
            self.mem_labels[f"self.memory_label{i}"].setGeometry(QtCore.QRect(50, self.memory_label_yloc[0][i]+20, 270, 13))
            self.mem_labels[f"self.memory_label{i}"].setAlignment(QtCore.Qt.AlignCenter)
            self.mem_labels[f"self.memory_label{i}"].setObjectName("memory_label")
            self.mem_labels[f"self.memory_label{i}"].show()
    
    def show_summary_table(self):
        self.second_ui = SummaryTableWindow([self.start_time, self.finish, self.cpu_wait])
    
    def jump_to(self):
        self.new_window = QtWidgets.QMainWindow()
        self.second_ui = SC_TimeList(self.new_window)
        self.second_ui.pushButton.clicked.connect(self.go_)
        self.new_window.show()
    
    def go_(self):
        if not self.idx == self.second_ui.comboBox.currentIndex():
            self.idx = self.second_ui.comboBox.currentIndex()
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

            self.button_state()

class SC_TimeList:
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Time List")
        MainWindow.setFixedSize(251, 170)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("Icons/clock.png")))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(resource_path("Icons/clock-history.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(91, 111, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow-skip.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(True)
        # self.pushButton.clicked.connect(self.change_txt)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        c = []
        T = X[3] + X[4]
        T = fcn.sort_time(T)
        self.comboBox.addItem(self.icon, f'Before {T[0]}')
        for time in T:
            if time in c:
                self.comboBox.addItem(self.icon, f'{time} ↰')
            elif time == T[-1]:
                self.comboBox.addItem(self.icon, f'{time} (Finished)')
            else:
                self.comboBox.addItem(self.icon, time)
            c.append(time)


# Partitioned Allocation
class SP_InputWindow:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.job_entries = {}
        self.size_entries = {}
        self.arrival_entries = {}
        self.run_entries = {}
        self.partition_nums = {}
        self.partition_sizes = {}
        self.csv_loaded_successful = False
        self.active_file = ''
        self.max_size = 0
        self.remaining_size = 0
        self.max_partition = 0
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 655)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_job_details = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_job_details.setGeometry(QtCore.QRect(370, 30, 531, 551))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.Group_job_details.setFont(font)
        self.Group_job_details.setObjectName("Group_job_details")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Group_job_details)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 10, 25, 10)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.job_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.job_label.sizePolicy().hasHeightForWidth())
        self.job_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.job_label.setFont(font)
        self.job_label.setAlignment(QtCore.Qt.AlignCenter)
        self.job_label.setObjectName("job_label")
        self.horizontalLayout_3.addWidget(self.job_label)
        self.size_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_label.sizePolicy().hasHeightForWidth())
        self.size_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.size_label.setFont(font)
        self.size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.size_label.setObjectName("size_label")
        self.horizontalLayout_3.addWidget(self.size_label)
        self.arrival_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_label.sizePolicy().hasHeightForWidth())
        self.arrival_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.arrival_label.setFont(font)
        self.arrival_label.setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_label.setObjectName("arrival_label")
        self.horizontalLayout_3.addWidget(self.arrival_label)
        self.runtime_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runtime_label.sizePolicy().hasHeightForWidth())
        self.runtime_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.runtime_label.setFont(font)
        self.runtime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.runtime_label.setObjectName("runtime_label")
        self.horizontalLayout_3.addWidget(self.runtime_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.scrollArea = QtWidgets.QScrollArea(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMouseTracking(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(2)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 488, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setHorizontalSpacing(40)
        self.gridLayout.setVerticalSpacing(55)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, 150, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.import_csv_btn = QtWidgets.QPushButton(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{job number, job size*, arrival time*, run time*}')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.horizontalLayout_4.addWidget(self.import_csv_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(100, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(30)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.rmv_entry_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.rmv_entry_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rmv_entry_btn.setIcon(icon1)
        self.rmv_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.rmv_entry_btn.setCheckable(False)
        self.rmv_entry_btn.setDefault(False)
        self.rmv_entry_btn.setFlat(True)
        self.rmv_entry_btn.setObjectName("rmv_entry_btn")
        self.horizontalLayout_5.addWidget(self.rmv_entry_btn)
        self.add_entry_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.add_entry_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/plus-black-symbol.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_entry_btn.setIcon(icon2)
        self.add_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.add_entry_btn.setCheckable(False)
        self.add_entry_btn.setDefault(False)
        self.add_entry_btn.setFlat(True)
        self.add_entry_btn.setObjectName("add_entry_btn")
        self.horizontalLayout_5.addWidget(self.add_entry_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.Group_memSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memSize.setGeometry(QtCore.QRect(26, 114, 151, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Group_memSize.setFont(font)
        self.Group_memSize.setObjectName("Group_memSize")
        self.memSize_value = QtWidgets.QSpinBox(self.Group_memSize)
        self.memSize_value.setGeometry(QtCore.QRect(14, 40, 121, 29))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.memSize_value.sizePolicy().hasHeightForWidth())
        self.memSize_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.memSize_value.setFont(font)
        self.memSize_value.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.memSize_value.setAlignment(QtCore.Qt.AlignCenter)
        self.memSize_value.setMaximum(999999999)
        self.memSize_value.setSingleStep(5)
        self.memSize_value.setProperty("value", 0)
        self.memSize_value.setObjectName("memSize_value")
        self.Group_osSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_osSize.setGeometry(QtCore.QRect(206, 114, 141, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Group_osSize.setFont(font)
        self.Group_osSize.setObjectName("Group_osSize")
        self.osSize_value = QtWidgets.QSpinBox(self.Group_osSize)
        self.osSize_value.setGeometry(QtCore.QRect(13, 40, 121, 29))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.osSize_value.sizePolicy().hasHeightForWidth())
        self.osSize_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.osSize_value.setFont(font)
        self.osSize_value.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.osSize_value.setAlignment(QtCore.Qt.AlignCenter)
        self.osSize_value.setMaximum(999999999)
        self.osSize_value.setSingleStep(5)
        self.osSize_value.setProperty("value", 0)
        self.osSize_value.setObjectName("osSize_value")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(800, 615, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_btn.setIcon(icon3)
        self.start_btn.setIconSize(QtCore.QSize(20, 20))
        self.start_btn.setCheckable(False)
        self.start_btn.setAutoDefault(False)
        self.start_btn.setDefault(False)
        self.start_btn.setFlat(True)
        self.start_btn.setObjectName("start_btn")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(-10, 615, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.back_btn.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_btn.setIcon(icon4)
        self.back_btn.setIconSize(QtCore.QSize(20, 20))
        self.back_btn.setCheckable(False)
        self.back_btn.setAutoDefault(False)
        self.back_btn.setDefault(False)
        self.back_btn.setFlat(True)
        self.back_btn.setObjectName("back_btn")
        self.pv_line = QtWidgets.QFrame(self.centralwidget)
        self.pv_line.setGeometry(QtCore.QRect(29, 260, 21, 35))
        self.pv_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.pv_line.setLineWidth(2)
        self.pv_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.pv_line.setObjectName("pv_line")

        self.pv_line2 = QtWidgets.QFrame(self.centralwidget)
        self.pv_line2.setGeometry(QtCore.QRect(324, 260, 21, 35))
        self.pv_line2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.pv_line2.setLineWidth(2)
        self.pv_line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.pv_line2.setObjectName("pv_line2")

        self.ph_line = QtWidgets.QFrame(self.centralwidget)
        self.ph_line.setGeometry(QtCore.QRect(38, 250, 297, 20))
        self.ph_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ph_line.setLineWidth(2)
        self.ph_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.ph_line.setObjectName("ph_line")
        self.Group_MemPartition = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_MemPartition.setGeometry(QtCore.QRect(26, 214, 321, 301))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.Group_MemPartition.setFont(font)
        self.Group_MemPartition.setFlat(False)
        self.Group_MemPartition.setCheckable(False)
        self.Group_MemPartition.setObjectName("Group_MemPartition")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Group_MemPartition)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Partition_verticalLayout = QtWidgets.QVBoxLayout()
        self.Partition_verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.Partition_verticalLayout.setSpacing(0)
        self.Partition_verticalLayout.setObjectName("Partition_verticalLayout")
        self.Partition_horizontalLayout = QtWidgets.QHBoxLayout()
        self.Partition_horizontalLayout.setContentsMargins(0, 10, 25, 10)
        self.Partition_horizontalLayout.setSpacing(0)
        self.Partition_horizontalLayout.setObjectName("Partition_horizontalLayout")
        self.partition_label = QtWidgets.QLabel(self.Group_MemPartition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partition_label.sizePolicy().hasHeightForWidth())
        self.partition_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.partition_label.setFont(font)
        self.partition_label.setAlignment(QtCore.Qt.AlignCenter)
        self.partition_label.setObjectName("partition_label")
        self.Partition_horizontalLayout.addWidget(self.partition_label)

        self.partition_size_label = QtWidgets.QLabel(self.Group_MemPartition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partition_size_label.sizePolicy().hasHeightForWidth())
        self.partition_size_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.partition_size_label.setFont(font)
        self.partition_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.partition_size_label.setObjectName("partition_size_label")
        self.Partition_horizontalLayout.addWidget(self.partition_size_label)
        self.Partition_verticalLayout.addLayout(self.Partition_horizontalLayout)
        self.Partition_scrollArea = QtWidgets.QScrollArea(self.Group_MemPartition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Partition_scrollArea.sizePolicy().hasHeightForWidth())
        self.Partition_scrollArea.setSizePolicy(sizePolicy)
        self.Partition_scrollArea.setMouseTracking(True)
        self.Partition_scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.Partition_scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Partition_scrollArea.setLineWidth(2)
        self.Partition_scrollArea.setMidLineWidth(0)
        self.Partition_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Partition_scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Partition_scrollArea.setWidgetResizable(True)
        self.Partition_scrollArea.setObjectName("Partition_scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 278, 69))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_2.setAutoFillBackground(True)
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_4.setHorizontalSpacing(40)
        self.gridLayout_4.setVerticalSpacing(20)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Partition_scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.Partition_verticalLayout.addWidget(self.Partition_scrollArea)
        self.gridLayout_3.addLayout(self.Partition_verticalLayout, 0, 0, 1, 2)
        self.Partition_horizontalLayout_btn = QtWidgets.QHBoxLayout()
        self.Partition_horizontalLayout_btn.setContentsMargins(100, -1, -1, -1)
        self.Partition_horizontalLayout_btn.setSpacing(30)
        self.Partition_horizontalLayout_btn.setObjectName("Partition_horizontalLayout_btn")
        self.rmv_partition_btn = QtWidgets.QPushButton(self.Group_MemPartition)
        self.rmv_partition_btn.setText("")
        self.rmv_partition_btn.setIcon(icon1)
        self.rmv_partition_btn.setIconSize(QtCore.QSize(20, 20))
        self.rmv_partition_btn.setCheckable(False)
        self.rmv_partition_btn.setDefault(False)
        self.rmv_partition_btn.setFlat(True)
        self.rmv_partition_btn.setObjectName("rmv_partition_btn")
        self.Partition_horizontalLayout_btn.addWidget(self.rmv_partition_btn)
        self.add_partition_btn = QtWidgets.QPushButton(self.Group_MemPartition)
        self.add_partition_btn.setText("")
        self.add_partition_btn.setIcon(icon2)
        self.add_partition_btn.setIconSize(QtCore.QSize(20, 20))
        self.add_partition_btn.setCheckable(False)
        self.add_partition_btn.setDefault(False)
        self.add_partition_btn.setFlat(True)
        self.add_partition_btn.setObjectName("add_partition_btn")
        self.Partition_horizontalLayout_btn.addWidget(self.add_partition_btn)
        self.gridLayout_3.addLayout(self.Partition_horizontalLayout_btn, 1, 1, 1, 1)
        
        self.jv_line = QtWidgets.QFrame(self.centralwidget)
        self.jv_line.setGeometry(QtCore.QRect(373, 70, 21, 41))
        self.jv_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.jv_line.setLineWidth(2)
        global dark
        if dark == True:
            self.jv_line.setStyleSheet('color: #FFFFFF')
        else:
            self.jv_line.setStyleSheet('color: #838383')
        self.jv_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.jv_line.setObjectName("jv_line")

        self.jv_line2 = QtWidgets.QFrame(self.centralwidget)
        self.jv_line2.setGeometry(QtCore.QRect(878, 70, 21, 41))
        self.jv_line2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.jv_line2.setLineWidth(2)
        if dark == True:
            self.jv_line2.setStyleSheet('color: #FFFFFF')
        else:
            self.jv_line2.setStyleSheet('color: #838383')
        self.jv_line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.jv_line2.setObjectName("jv_line2")


        self.remaining_label_horizontalLayout = QtWidgets.QHBoxLayout()
        self.remaining_label_horizontalLayout.setContentsMargins(10, 5, 0, 0)
        self.remaining_label_horizontalLayout.setSpacing(30)
        self.remaining_label_horizontalLayout.setObjectName("remaining_label_horizontalLayout")

        self.remaining_label = QtWidgets.QLabel(self.Group_MemPartition)
        self.remaining_label.setFont(font)
        self.remaining_label.setToolTip('This will automatically added to your partition.')
        self.remaining_label.setObjectName('remaining_label')
        self.remaining_label.setGeometry(QtCore.QRect(302, 535, 100, 20))
        self.remaining_label.setAlignment(QtCore.Qt.AlignLeft)
        self.remaining_label.adjustSize()
        self.remaining_label_horizontalLayout.addWidget(self.remaining_label)
        self.gridLayout_3.addLayout(self.remaining_label_horizontalLayout, 1, 0, 1, 1)


        self.jh_line = QtWidgets.QFrame(self.centralwidget)
        self.jh_line.setGeometry(QtCore.QRect(382, 60, 507, 20))
        self.jh_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.jh_line.setLineWidth(2)
        if dark == True:
            self.jh_line.setStyleSheet('color: #FFFFFF')
        else:
            self.jh_line.setStyleSheet('color: #838383')
        self.jh_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.jh_line.setObjectName("jh_line")
        self.Group_job_details.raise_()
        self.Group_memSize.raise_()
        self.Group_osSize.raise_()
        self.start_btn.raise_()
        self.back_btn.raise_()
        self.ph_line.raise_()
        self.Group_MemPartition.raise_()
        self.pv_line.raise_()
        self.jv_line.raise_()
        self.jh_line.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 21))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.make_default_entry(default_entry)
        self.make_default_partition_count(default_partition_count)
        self.button_state()
        self.entry_detail_state()
        self.memSize_value.textChanged.connect(self.entry_detail_state)
        self.osSize_value.textChanged.connect(self.entry_detail_state)
        self.memSize_value.selectAll()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Static Partition"))
        self.Group_job_details.setTitle(_translate("MainWindow", "Job Details"))
        self.job_label.setText(_translate("MainWindow", "Job"))
        self.size_label.setText(_translate("MainWindow", "Size"))
        self.arrival_label.setText(_translate("MainWindow", "Arrival time"))
        self.runtime_label.setText(_translate("MainWindow", "Run time"))
        self.import_csv_btn.setText(_translate("MainWindow", "  Import CSV"))
        self.Group_memSize.setTitle(_translate("MainWindow", "Memory Size"))
        self.Group_osSize.setTitle(_translate("MainWindow", "OS Size"))
        self.start_btn.setText(_translate("MainWindow", "  Start"))
        self.back_btn.setText(_translate("MainWindow", "  Back"))
        self.Group_MemPartition.setTitle(_translate("MainWindow", "Memory Partition"))
        self.partition_label.setText(_translate("MainWindow", "Partition"))
        self.partition_size_label.setText(_translate("MainWindow", "Size"))

        self.start_btn.clicked.connect(self.start)
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.add_entry_btn.clicked.connect(self.add_entry)
        self.rmv_entry_btn.clicked.connect(self.remove_entry)
        self.add_partition_btn.clicked.connect(self.add_partition)
        self.rmv_partition_btn.clicked.connect(self.remove_partition)
        
        self.back_btn.clicked.connect(self.back_to_start_up)

    def back_to_start_up(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def make_default_entry(self, default_entry):
        for _ in range(default_entry):
            self.add_entry()
    
    def make_default_partition_count(self, default_partition_count):
        for _ in range(default_partition_count):
            self.add_partition()
    
    def add_partition(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Parition No.
        self.partition_nums[f'partition{len(self.partition_nums)+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partition_nums[f'partition{len(self.partition_nums)}'].sizePolicy().hasHeightForWidth())
        self.partition_nums[f'partition{len(self.partition_nums)}'].setSizePolicy(sizePolicy)
        self.partition_nums[f'partition{len(self.partition_nums)}'].setText(f'{len(self.partition_nums)}')
        self.partition_nums[f'partition{len(self.partition_nums)}'].setFont(font)
        self.partition_nums[f'partition{len(self.partition_nums)}'].setScaledContents(False)
        self.partition_nums[f'partition{len(self.partition_nums)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.partition_nums[f'partition{len(self.partition_nums)}'].setObjectName(f'partition{len(self.partition_nums)}')
        self.gridLayout_4.addWidget(self.partition_nums[f'partition{len(self.partition_nums)}'], len(self.partition_nums), 0, 1, 1)

    #Partition Size
        self.partition_sizes[f'partition_size{len(self.partition_sizes)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].sizePolicy().hasHeightForWidth())
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setSizePolicy(sizePolicy)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setFont(font)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setMaximum(999999999)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setMinimum(0)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setSingleStep(5)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setProperty("value", 0)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].textChanged.connect(self.partition_entry_state)
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].setObjectName("partition_size1")
        self.gridLayout_4.addWidget(self.partition_sizes[f'partition_size{len(self.partition_sizes)}'], len(self.partition_sizes), 1, 1, 1)
        list(self.partition_sizes.values())[-1].selectAll()
        list(self.partition_sizes.values())[-1].setFocus()
        Pscroll_bar = self.Partition_scrollArea.verticalScrollBar()
        self.Partition_scrollArea.verticalScrollBar().rangeChanged.connect(lambda: Pscroll_bar.setValue(Pscroll_bar.maximum()))
        self.button_state()

    def add_entry(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Job No.
        self.job_entries[f"job{len(self.job_entries)+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.job_entries[f"job{len(self.job_entries)}"].setText(f"{len(self.job_entries)}")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.job_entries[f"job{len(self.job_entries)}"].sizePolicy().hasHeightForWidth())
        self.job_entries[f"job{len(self.job_entries)}"].setSizePolicy(sizePolicy)
        self.job_entries[f"job{len(self.job_entries)}"].setFont(font)
        self.job_entries[f"job{len(self.job_entries)}"].setScaledContents(False)
        self.job_entries[f"job{len(self.job_entries)}"].setAlignment(QtCore.Qt.AlignCenter)
        self.job_entries[f"job{len(self.job_entries)}"].setObjectName(f"job{len(self.job_entries)}")
        self.gridLayout.addWidget(self.job_entries[f"job{len(self.job_entries)}"], len(self.job_entries), 0, 1, 1)
        
    #Size
        self.size_entries[f'size{len(self.size_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_entries[f'size{len(self.size_entries)}'].sizePolicy().hasHeightForWidth())
        self.size_entries[f'size{len(self.size_entries)}'].setSizePolicy(sizePolicy)
        self.size_entries[f'size{len(self.size_entries)}'].setFont(font)
        self.size_entries[f'size{len(self.size_entries)}'].setMinimum(0)
        self.size_entries[f'size{len(self.size_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.size_entries[f'size{len(self.size_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.size_entries[f'size{len(self.size_entries)}'].setMaximum(self.memSize_value.value() - self.osSize_value.value())
        self.size_entries[f'size{len(self.size_entries)}'].setSingleStep(5)
        self.size_entries[f'size{len(self.size_entries)}'].setProperty("value", 0)
        self.size_entries[f'size{len(self.size_entries)}'].setObjectName(f'size{len(self.size_entries)}')
        self.gridLayout.addWidget(self.size_entries[f'size{len(self.size_entries)}'], len(self.size_entries), 1, 1, 1)
        
    #Arrival
        self.arrival_entries[f'arrival{len(self.arrival_entries)+1}'] = QtWidgets.QTimeEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{len(self.arrival_entries)}'].sizePolicy().hasHeightForWidth())
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setSizePolicy(sizePolicy)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setDisplayFormat("h:mm")
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setFont(font)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setObjectName(f'arrival{len(self.arrival_entries)}')
        self.gridLayout.addWidget(self.arrival_entries[f'arrival{len(self.arrival_entries)}'], len(self.arrival_entries), 2, 1, 1)
        
    #Run
        self.run_entries[f'run{len(self.run_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_entries[f'run{len(self.run_entries)}'].sizePolicy().hasHeightForWidth())
        self.run_entries[f'run{len(self.run_entries)}'].setSizePolicy(sizePolicy)
        self.run_entries[f'run{len(self.run_entries)}'].setFont(font)
        self.run_entries[f'run{len(self.run_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.run_entries[f'run{len(self.run_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.run_entries[f'run{len(self.run_entries)}'].setMaximum(999999999)
        self.run_entries[f'run{len(self.run_entries)}'].setSingleStep(5)
        self.run_entries[f'run{len(self.run_entries)}'].setProperty("value", 0)
        self.run_entries[f'run{len(self.run_entries)}'].setObjectName(f'run{len(self.run_entries)}')
        self.gridLayout.addWidget(self.run_entries[f'run{len(self.run_entries)}'], len(self.run_entries), 3, 1, 1)

        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()

    def remove_entry(self):
        self.job_entries[f"job{len(self.job_entries)}"].hide()
        self.size_entries[f'size{len(self.size_entries)}'].hide()
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].hide()
        self.run_entries[f'run{len(self.run_entries)}'].hide()

        del self.job_entries[f"job{len(self.job_entries)}"]
        del self.size_entries[f'size{len(self.size_entries)}']
        del self.arrival_entries[f'arrival{len(self.arrival_entries)}']
        del self.run_entries[f'run{len(self.run_entries)}']
        
        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()
    
    def remove_partition(self):
        self.partition_nums[f"partition{len(self.partition_nums)}"].hide()
        self.partition_sizes[f'partition_size{len(self.partition_sizes)}'].hide()

        del self.partition_nums[f"partition{len(self.partition_nums)}"]
        del self.partition_sizes[f'partition_size{len(self.partition_sizes)}']

        Pscroll_bar = self.Partition_scrollArea.verticalScrollBar()
        self.Partition_scrollArea.verticalScrollBar().rangeChanged.connect(lambda: Pscroll_bar.setValue(Pscroll_bar.maximum()))
        self.button_state()
    
    def scroll(self):
        item = self.ListWidget.findItems('ITEM-0011', QtCore.Qt.MatchRegExp)[0]
        item.setSelected(True)
        self.ListWidget.scrollToItem(item, QtGui.QAbstractItemView.PositionAtTop)

    def button_state(self):
        if len(self.partition_nums) == 1:
            self.rmv_partition_btn.setEnabled(False)
        else:
            self.rmv_partition_btn.setEnabled(True)
        
        if self.csv_loaded_successful:
            self.add_entry_btn.setEnabled(False)
            self.rmv_entry_btn.setEnabled(False)
        else:
            if len(self.job_entries) == 1:
                self.rmv_entry_btn.setEnabled(False)
            else:
                self.rmv_entry_btn.setEnabled(True)
            self.add_entry_btn.setEnabled(True)
    
    def make_import_btn(self):
        self.import_csv_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.import_csv_btn.setGeometry(QtCore.QRect(270, 535, 100, 20))
        self.import_csv_btn.setText("  Import CSV")
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{job number, job size*, arrival time*, run time*}')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.horizontalLayout_4.addWidget(self.import_csv_btn)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon2)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.import_csv_btn.show()
    
    def make_cancel_csv_btn(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)

        self.cancel_csv_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.cancel_csv_btn.setGeometry(QtCore.QRect(270, 528, 32, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_csv_btn.sizePolicy().hasHeightForWidth())
        self.cancel_csv_btn.setSizePolicy(sizePolicy)
        self.cancel_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.horizontalLayout_4.addWidget(self.cancel_csv_btn)
        
        self.cancel_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon_red.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_csv_btn.setIcon(icon2)
        self.cancel_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.cancel_csv_btn.setCheckable(False)
        self.cancel_csv_btn.setDefault(False)
        self.cancel_csv_btn.setFlat(True)
        self.cancel_csv_btn.setObjectName("cancel_csv_btn")
        self.cancel_csv_btn.clicked.connect(self.cancel_csv)

        self.file_name_label = QtWidgets.QLabel(self.Group_job_details)
        self.file_name_label.setFont(font)
        self.file_name_label.setObjectName('file_name_label')
        self.file_name_label.setGeometry(QtCore.QRect(302, 535, 100, 20))
        self.file_name_label.setText(self.active_file)
        self.file_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_name_label.adjustSize()
        self.horizontalLayout_4.addWidget(self.file_name_label)

    def cancel_csv(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to remove this file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            print('Yes  ')
            self.cancel_csv_btn.hide()
            self.file_name_label.hide()
            del self.cancel_csv_btn
            del self.file_name_label

            for _ in range(len(self.job_entries)):
                self.remove_entry()
            for _ in range(len(self.partition_sizes)):
                self.remove_partition()
            self.make_default_partition_count(default_partition_count)
            self.make_default_entry(default_entry)
            self.entry_detail_state()

            self.make_import_btn()
            self.max_size = 0
            self.memSize_value.textChanged.connect(self.entry_detail_state)
            self.osSize_value.textChanged.connect(self.entry_detail_state)
            for i in range(len(self.partition_sizes)):
                list(self.partition_sizes.values())[i].textChanged.connect(self.partition_entry_state)
            self.add_entry_btn.setEnabled(True)
            self.rmv_entry_btn.setEnabled(True)
            
            # QtWidgets.QSpinBox().clear
            self.csv_loaded_successful = False

    def getFileDir(self):
        file_filter = '*.csv'
        response = QtWidgets.QFileDialog.getOpenFileNames(
            parent = QtWidgets.QWidget(),
            caption='Select a csv file',
            directory = os.getcwd(),
            filter=file_filter
        )
        self.active_file = response[0][0].split('/')[-1]
        return response[0][0]

    def import_csv(self):
        try:
            fileDir = self.getFileDir()
            csv = pd.read_csv(fileDir)
            column_name = list(csv.columns)
            jobs = csv[column_name[0]].tolist()
            job_size = csv[column_name[1]].tolist()
            arrival_time = csv[column_name[2]].tolist()
            run_time = csv[column_name[3]].tolist()

            for _ in range(len(self.job_entries)):
                self.remove_entry()
            self.import_csv_btn.hide()
            del self.import_csv_btn
            self.make_cancel_csv_btn()
            self.load_csv_to_window(jobs, job_size, arrival_time, run_time)

        except IndexError:
            print('No file selected')

    def load_csv_to_window(self, j, s, a, r):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Job No.
        for i in range(len(a)):
            self.job_entries[f"job{i+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.job_entries[f"job{i+1}"].setText(f"{i+1}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.job_entries[f"job{i+1}"].sizePolicy().hasHeightForWidth())
            self.job_entries[f"job{i+1}"].setSizePolicy(sizePolicy)
            self.job_entries[f"job{i+1}"].setFont(font)
            self.job_entries[f"job{i+1}"].setScaledContents(False)
            self.job_entries[f"job{i+1}"].setAlignment(QtCore.Qt.AlignCenter)
            self.job_entries[f"job{i+1}"].setObjectName(f"job{i+1}")
            self.gridLayout.addWidget(self.job_entries[f"job{i+1}"], i+1, 0, 1, 1)
    #Size
        for i in range(len(a)):
            self.size_entries[f'size{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.size_entries[f'size{i+1}'].setText(f"{s[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.size_entries[f'size{i+1}'].sizePolicy().hasHeightForWidth())
            self.size_entries[f'size{i+1}'].setSizePolicy(sizePolicy)
            self.size_entries[f'size{i+1}'].setFont(font)
            self.size_entries[f'size{i+1}'].setScaledContents(False)
            self.size_entries[f'size{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.size_entries[f'size{i+1}'].setObjectName(f"size{i+1}")
            self.gridLayout.addWidget(self.size_entries[f'size{i+1}'], i+1, 1, 1, 1)
    #Arrival
        for i in range(len(a)):
            self.arrival_entries[f'arrival{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.arrival_entries[f'arrival{i+1}'].setText(f"{a[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{i+1}'].sizePolicy().hasHeightForWidth())
            self.arrival_entries[f'arrival{i+1}'].setSizePolicy(sizePolicy)
            self.arrival_entries[f'arrival{i+1}'].setFont(font)
            self.arrival_entries[f'arrival{i+1}'].setScaledContents(False)
            self.arrival_entries[f'arrival{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.arrival_entries[f'arrival{i+1}'].setObjectName(f"arrival{i+1}")
            self.gridLayout.addWidget(self.arrival_entries[f'arrival{i+1}'], i+1, 2, 1, 1)
    #Run
        for i in range(len(a)):
            self.run_entries[f'run{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.run_entries[f'run{i+1}'].setText(f"{r[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.run_entries[f'run{i+1}'].sizePolicy().hasHeightForWidth())
            self.run_entries[f'run{i+1}'].setSizePolicy(sizePolicy)
            self.run_entries[f'run{i+1}'].setFont(font)
            self.run_entries[f'run{i+1}'].setScaledContents(False)
            self.run_entries[f'run{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.run_entries[f'run{i+1}'].setObjectName(f"run{i+1}")
            self.gridLayout.addWidget(self.run_entries[f'run{i+1}'], i+1, 3, 1, 1)

        self.max_size = max(s)
        for i in range(len(self.partition_sizes)):
            list(self.partition_sizes.values())[i].textChanged.connect(self.partition_entry_state_QLabel)
        self.memSize_value.textChanged.connect(self.entry_detail_state_QLabel)
        self.osSize_value.textChanged.connect(self.entry_detail_state_QLabel)

        self.csv_loaded_successful = True
        self.Group_job_details.setEnabled(True)
        self.add_entry_btn.setEnabled(False)
        self.rmv_entry_btn.setEnabled(False)
        
        self.entry_detail_state_QLabel()
        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.minimum()))
        # self.partition_entry_state_QLabel()
        
    def entry_detail_state(self):
        global dark
        if dark == True:
            self.jh_line.setStyleSheet('color: #FFFFFF')
        else:
            self.jh_line.setStyleSheet('color: #838383')
        if dark == False:
            if self.memSize_value.value() != 0:
                self.Group_job_details.setEnabled(True)
                self.jv_line.setStyleSheet('color: black')
                self.jv_line2.setStyleSheet('color: black')
                self.jh_line.setStyleSheet('color: black')
                self.Group_MemPartition.setEnabled(True)
                self.pv_line.setStyleSheet('color: black')
                self.pv_line2.setStyleSheet('color: black')
                self.ph_line.setStyleSheet('color: black')
            else:
                self.Group_job_details.setEnabled(False)
                self.jv_line.setStyleSheet('color: #838383')
                self.jv_line2.setStyleSheet('color: #838383')
                self.jh_line.setStyleSheet('color: #838383')
                self.Group_MemPartition.setEnabled(False)
                self.pv_line.setStyleSheet('color: #838383')
                self.pv_line2.setStyleSheet('color: #838383')
                self.ph_line.setStyleSheet('color: #838383')
        else:
            if self.memSize_value.value() != 0:
                self.Group_job_details.setEnabled(True)
                self.jv_line.setStyleSheet('color: #FFFFFF')
                self.jv_line2.setStyleSheet('color: #FFFFFF')
                self.jh_line.setStyleSheet('color: #FFFFFF')
                self.Group_MemPartition.setEnabled(True)
                self.pv_line.setStyleSheet('color: #FFFFFF')
                self.pv_line2.setStyleSheet('color: #FFFFFF')
                self.ph_line.setStyleSheet('color: #FFFFFF')
            else:
                self.Group_job_details.setEnabled(False)
                self.jv_line.setStyleSheet('color: #FFFFFF')
                self.jv_line2.setStyleSheet('color: #FFFFFF')
                self.jh_line.setStyleSheet('color: #FFFFFF')
                self.Group_MemPartition.setEnabled(False)
                self.pv_line.setStyleSheet('color: #FFFFFF')
                self.pv_line2.setStyleSheet('color: #FFFFFF')
                self.ph_line.setStyleSheet('color: #FFFFFF')

        if type(self.size_entries['size1']).__name__ != 'QLabel':
            self.osSize_value.setMaximum(self.memSize_value.value())
            self.partition_entry_state()
            for i in range(len(self.size_entries)):
                if type(self.size_entries['size1']).__name__ != 'QLabel':
                    if self.remaining_size > self.max_partition:
                        list(self.size_entries.values())[i].setMaximum(self.remaining_size)
                    else:
                        list(self.size_entries.values())[i].setMaximum(self.max_partition)
                    if list(self.size_entries.values())[i].value() < 0:
                        list(self.size_entries.values())[i].setMinimum(0)            

    def partition_entry_state(self):
        if type(self.size_entries['size1']).__name__ != 'QLabel':
            partition = []
            self.osSize_value.setMaximum(self.memSize_value.value())
            self.remaining_size = self.memSize_value.value() - self.osSize_value.value()
            for i in range(len(self.partition_sizes)):
                list(self.partition_sizes.values())[i].setMaximum(self.remaining_size)
                list(self.partition_sizes.values())[i].setMinimum(0)
                self.remaining_size -= list(self.partition_sizes.values())[i].value()
                partition.append(list(self.partition_sizes.values())[i].value())
            self.max_partition = max(partition) ################# Job Size Validation (based on max partition) #####################
            if self.remaining_size < 0:
                self.remaining_label.setText(f'Remaining: 0')
            else:
                self.remaining_label.setText(f'Remaining: {self.remaining_size}')
            
            for i in range(len(self.size_entries)):
                    if self.remaining_size > self.max_partition:
                        list(self.size_entries.values())[i].setMaximum(self.remaining_size)
                    else:
                        list(self.size_entries.values())[i].setMaximum(self.max_partition)
                    if list(self.size_entries.values())[i].value() < 0:
                        list(self.size_entries.values())[i].setMinimum(0)
    
    def entry_detail_state_QLabel(self):
        if type(self.size_entries['size1']).__name__ == 'QLabel':
            self.memSize_value.setMinimum(self.max_size)
            self.osSize_value.setMaximum(self.memSize_value.value())
            
            self.remaining_size = self.memSize_value.value() - self.osSize_value.value()

            self.partition_entry_state_QLabel()
            if self.remaining_size < 0:
                self.remaining_label.setText(f'Remaining: 0')
            else:
                self.remaining_label.setText(f'Remaining: {self.remaining_size}')

    def partition_entry_state_QLabel(self):
        if type(self.size_entries['size1']).__name__ == 'QLabel':
            partition = []
            self.remaining_size = self.memSize_value.value() - self.osSize_value.value()
            for i in range(len(self.partition_sizes)):
                if self.remaining_size >= 0:
                # list(self.partition_sizes.values())[i].setMinimum(self.max_size)
                    list(self.partition_sizes.values())[i].setMaximum(self.remaining_size)
                    
                    self.remaining_size -= list(self.partition_sizes.values())[i].value()
                partition.append(list(self.partition_sizes.values())[i].value())
            self.max_partition = max(partition)
            if self.remaining_size < 0:
                self.remaining_label.setText(f'Remaining: 0')
            else:
                self.remaining_label.setText(f'Remaining: {self.remaining_size}')

    def start(self):
        print(type(self.size_entries['size1']).__name__, '<----------------------')
        # Validate Inputs
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setIcon(QtWidgets.QMessageBox.Information)
        notify_user.setFont(font)

        err_msg = QtWidgets.QMessageBox()
        err_msg.setIcon(QtWidgets.QMessageBox.Information)
        err_msg.setFont(font)
        
        self.validated = True
        for _ in range(1):
            if self.memSize_value.value() <= self.osSize_value.value():
                self.validated = False
                err_msg.setText('Sizes must be:\nMemory size > OS size > 0      ')
                err_msg.setWindowTitle("Memory Error")
                err_msg.exec_()
                self.memSize_value.setFocus()
                self.memSize_value.selectAll()
                self.Group_job_details.setEnabled(False)
                break
                
            elif self.osSize_value.value() <= 0:
                self.validated = False
                err_msg.setText('Sizes must be:\nMemory size > OS size > 0      ')
                err_msg.setWindowTitle("Memory Error")
                err_msg.exec_()
                self.osSize_value.setFocus()
                self.osSize_value.selectAll()
                self.Group_job_details.setEnabled(False)
                break

            elif self.max_size > (self.memSize_value.value() - self.osSize_value.value()):
                self.validated = False
                err_msg.setText(f'Job sizes must fit !\n ~max={self.max_size}                  ')
                err_msg.setWindowTitle("Size Error")
                err_msg.exec_()
                break

            for i in range(len(self.job_entries)):
                if type(self.size_entries['size1']).__name__ == 'QLabel':
                    if list(self.size_entries.values())[i].text() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.size_entries.values())[i].setFocus()
                        list(self.size_entries.values())[i].selectAll()
                        break
                    if list(self.arrival_entries.values())[i].text().split(':')[0] == '0':
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.arrival_entries.values())[i].setFocus()
                        list(self.arrival_entries.values())[i].selectAll()
                        break
                    if list(self.run_entries.values())[i].text() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.run_entries.values())[i].setFocus()
                        list(self.run_entries.values())[i].selectAll()
                        break
                else:
                    if list(self.size_entries.values())[i].value() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.size_entries.values())[i].setFocus()
                        list(self.size_entries.values())[i].selectAll()
                        yloc = list(self.size_entries.values())[i].y() - list(self.size_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
                    if list(self.arrival_entries.values())[i].text().split(':')[0] == '0':
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.arrival_entries.values())[i].setFocus()
                        list(self.arrival_entries.values())[i].selectAll()
                        yloc = list(self.arrival_entries.values())[i].y() - list(self.arrival_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
                    if list(self.run_entries.values())[i].value() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.run_entries.values())[i].setFocus()
                        list(self.run_entries.values())[i].selectAll()
                        yloc = list(self.run_entries.values())[i].y() - list(self.run_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
        
        if self.validated == False and self.csv_loaded_successful == True:
            self.Group_job_details.setEnabled(True)

    # Export JSON
        if self.validated:
            if type(self.size_entries['size1']).__name__ == 'QLabel':
                dictionary ={
                'Memory size' : self.memSize_value.value(),
                'OS size' : self.osSize_value.value(),
                'Partition size' : [partition_size.value() for partition_size in self.partition_sizes.values()],
                'Job' : [job.text() for job in self.job_entries.values()],
                'Size' : [int(size.text()) for size in self.size_entries.values()],
                'Arrival time' : [arrival.text() for arrival in self.arrival_entries.values()],
                'Run time' : [int(run.text()) for run in self.run_entries.values()]
                }
            else:
                dictionary ={
                'Memory size' : self.memSize_value.value(),
                'OS size' : self.osSize_value.value(),
                'Partition size' : [partition_size.value() for partition_size in self.partition_sizes.values()],
                'Job' : [job.text() for job in self.job_entries.values()],
                'Size' : [int(size.value()) for size in self.size_entries.values()],
                'Arrival time' : [arrival.text() for arrival in self.arrival_entries.values()],
                'Run time' : [int(run.value()) for run in self.run_entries.values()]
                }

            if dictionary["Arrival time"] != sorted(dictionary["Arrival time"]):
                notify_user.setText('Unsorted arrival detected\n~Inputs are now sorted by arrival !      ')
                notify_user.setWindowTitle("Sort by Arrival")
                notify_user.button
                notify_user.setStandardButtons
                notify_user.exec_()

        # Sort by Arrival
            for i in range(len(dictionary['Arrival time'])-1):
                for j in range(0, len(dictionary['Arrival time'])-i-1):
                    if fcn.to_minutes(dictionary['Arrival time'][j]) > fcn.to_minutes(dictionary['Arrival time'][j+1]):
                        dictionary['Arrival time'][j], dictionary['Arrival time'][j+1] = dictionary['Arrival time'][j+1], dictionary['Arrival time'][j]
                        dictionary['Size'][j], dictionary['Size'][j+1] = dictionary['Size'][j+1], dictionary['Size'][j]
                        dictionary['Run time'][j], dictionary['Run time'][j+1] = dictionary['Run time'][j+1], dictionary['Run time'][j]

            with open(f"{usrfile_name}.json", "w") as outfile:
                json.dump(dictionary, outfile, indent=4)

            global D
            global X
            
            D = dictionary
            X = sp.static_partition_EXEC(usrfile_name)
            self.next_window(D, X)
            print('VALIDATAED')

        else:
            print('NOT VALIDATED')

    def next_window(self, inputs, Data):
        self.newWindow = MyWindow()
        self.second_ui = SP_ProcessWindow(self.newWindow, inputs, Data)
        self.newWindow.show()
        self.MainWindow.hide()

class SP_ProcessWindow:
    V_END = 470
    def __init__(self, MainWindow, inputs, D):
        self.mem_map, self.label, self.message, self.status_table, self.partition_size,  = D[0], D[1], D[2], D[3], D[4]
        self.start_time, self.finish, self.cpu_wait = D[5], D[6], D[7]
        self.inputs = inputs
        self.MainWindow = MainWindow
        self.idx = 0
        self.fixed = False
        self.d = {}
        self.labels = {}
        self.mem_labels ={}
        self.end_show = False
        self.error_msg_value = 0
        global dark
        self.dark_theme_enabled = dark
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 655)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_memoryMap = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memoryMap.setGeometry(QtCore.QRect(510, 10, 321, 540))

        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Group_memoryMap.setFont(font)
        self.Group_memoryMap.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Group_memoryMap.setObjectName("Group_memoryMap")
        self.Group_job_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_job_table.setGeometry(QtCore.QRect(20, 119, 451, 215))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_job_table.setFont(font)
        self.Group_job_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_job_table.setCheckable(False)
        self.Group_job_table.setChecked(False)
        self.Group_job_table.setObjectName("Group_job_table")
        self.Job_Table = QtWidgets.QTableWidget(self.Group_job_table)
        self.Job_Table.setGeometry(QtCore.QRect(10, 27, 432, 181))
        self.Job_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Job_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Job_Table.setFont(font)
        self.Job_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Job_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Job_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.Job_Table.verticalHeader().setVisible(False) # Row Index
        self.Job_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.Job_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        
        self.Job_Table.setAutoScroll(True)
        self.Job_Table.setAlternatingRowColors(True)
        self.Job_Table.setObjectName("Job_Table")
        self.Job_Table.setColumnCount(4)
        self.Job_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(0, item)
        self.Job_Table.setItemDelegateForColumn(0, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(1, item)
        self.Job_Table.setItemDelegateForColumn(1, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(2, item)
        self.Job_Table.setItemDelegateForColumn(2, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(3, item)
        self.Job_Table.setItemDelegateForColumn(3, AlignDelegate(self.Job_Table))
        self.Job_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.Job_Table.horizontalHeaderItem(0).setFont(font)
        self.Job_Table.horizontalHeaderItem(1).setFont(font)
        self.Job_Table.horizontalHeaderItem(2).setFont(font)
        self.Job_Table.horizontalHeaderItem(3).setFont(font)
             
        self.Job_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # self.Job_Table.verticalHeader().setDefaultSectionSize(44)

        self.Group_pat_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_pat_table.setGeometry(QtCore.QRect(20, 350, 451, 215))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_pat_table.setFont(font)
        self.Group_pat_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_pat_table.setCheckable(False)
        self.Group_pat_table.setChecked(False)
        self.Group_pat_table.setObjectName("Group_pat_table")

        self.PAT_Table = QtWidgets.QTableWidget(self.Group_pat_table)
        self.PAT_Table.setGeometry(QtCore.QRect(10, 27, 432, 181))
        self.PAT_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PAT_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PAT_Table.setFont(font)
        self.PAT_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.PAT_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PAT_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.PAT_Table.verticalHeader().setVisible(False) # Row Index
        self.PAT_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.PAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #2A74BB;}')
        
        self.PAT_Table.setAutoScroll(True)
        self.PAT_Table.setAlternatingRowColors(True)
        self.PAT_Table.setObjectName("PAT_Table")
        self.PAT_Table.setColumnCount(4)
        self.PAT_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(0, item)
        self.PAT_Table.setItemDelegateForColumn(0, AlignDelegate(self.PAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(1, item)
        self.PAT_Table.setItemDelegateForColumn(1, AlignDelegate(self.PAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(2, item)
        self.PAT_Table.setItemDelegateForColumn(2, AlignDelegate(self.PAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(3, item)
        self.PAT_Table.setItemDelegateForColumn(3, AlignDelegate(self.PAT_Table))
        self.PAT_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.PAT_Table.horizontalHeaderItem(0).setFont(font)
        self.PAT_Table.horizontalHeaderItem(1).setFont(font)
        self.PAT_Table.horizontalHeaderItem(2).setFont(font)
        self.PAT_Table.horizontalHeaderItem(3).setFont(font)
             
        self.PAT_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.PAT_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.PAT_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.PAT_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # self.Job_Table.verticalHeader().setDefaultSectionSize(44)

        self.Group_osSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_osSize.setGeometry(QtCore.QRect(350, 70, 120, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_osSize.setFont(font)
        self.Group_osSize.setObjectName("Group_osSize")
        self.OS_size_label = QtWidgets.QLabel(self.Group_osSize)
        self.OS_size_label.setEnabled(True)
        self.OS_size_label.setGeometry(QtCore.QRect(10, 18, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.OS_size_label.setFont(font)
        self.OS_size_label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.OS_size_label.setMouseTracking(False)
        self.OS_size_label.setTabletTracking(False)
        self.OS_size_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.OS_size_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.OS_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.OS_size_label.setObjectName("OS_size_label")
        self.Group_memSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memSize.setGeometry(QtCore.QRect(30, 70, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_memSize.setFont(font)
        self.Group_memSize.setFlat(False)
        self.Group_memSize.setCheckable(False)
        self.Group_memSize.setObjectName("Group_memSize")
        self.mem_size_label = QtWidgets.QLabel(self.Group_memSize)
        self.mem_size_label.setGeometry(QtCore.QRect(20, 18, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mem_size_label.setFont(font)
        self.mem_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mem_size_label.setObjectName("mem_size_label")
        self.partition_title = QtWidgets.QLabel(self.centralwidget)
        self.partition_title.setGeometry(QtCore.QRect(20, 5, 451, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.partition_title.setFont(font)
        self.partition_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.partition_title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.partition_title.setLineWidth(1)
        self.partition_title.setAlignment(QtCore.Qt.AlignCenter)
        self.partition_title.setObjectName("partition_title")
        self.prev_button = QtWidgets.QPushButton(self.centralwidget)
        self.prev_button.setGeometry(QtCore.QRect(550, 565, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.prev_button.setFont(font)
        self.prev_button.setObjectName("prev_button")
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(700, 565, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.next_button.setFont(font)
        self.next_button.setObjectName("next_button")
        self.simplify_cbx = QtWidgets.QCheckBox(self.centralwidget)
        self.simplify_cbx.setGeometry(QtCore.QRect(775, 605, 65, 19))
        self.simplify_cbx.setFont(font)
        self.simplify_cbx.setObjectName("simplify_cbx")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(18, 560, 451, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.message_label.setFont(font)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setObjectName("message_label")
        self.horizontalLayout.addWidget(self.message_label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 28))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuHelp.setFont(font)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAbout = QtWidgets.QMenu(self.menuHelp)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAbout.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/message.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAbout.setIcon(icon)
        self.menuAbout.setObjectName("menuAbout")
        self.menuDevelopers = QtWidgets.QMenu(self.menuAbout)
        icon0 = QtGui.QIcon()
        icon0.addPixmap(QtGui.QPixmap(resource_path("Icons/group.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuDevelopers.setIcon(icon0)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuDevelopers.setFont(font)
        self.menuDevelopers.setObjectName("menuDevelopers")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuAppearance = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance.setFont(font)
        self.menuAppearance.setObjectName("menuAppearance")
        self.menuAppearance_2 = QtWidgets.QMenu(self.menuAppearance)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance_2.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/favorite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAppearance_2.setIcon(icon)
        self.menuAppearance_2.setObjectName("menuAppearance_2")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.toolBar.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setAcceptDrops(False)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setMovable(True)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setIconSize(QtCore.QSize(30, 25))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionHome = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/house_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon)
        self.actionHome.setObjectName("actionHome")
        self.actionLyra = QtWidgets.QAction(MainWindow)
        self.actionLyra.setObjectName("actionLyra")
        self.actionRyan = QtWidgets.QAction(MainWindow)
        self.actionRyan.setObjectName("actionRyan")
        self.actionJoshua = QtWidgets.QAction(MainWindow)
        self.actionJoshua.setObjectName("actionJoshua")
        self.actionLyra_2 = QtWidgets.QAction(MainWindow)
        self.actionLyra_2.setObjectName("actionLyra_2")
        self.actionRyan_2 = QtWidgets.QAction(MainWindow)
        self.actionRyan_2.setObjectName("actionRyan_2")
        self.actionJoshua_2 = QtWidgets.QAction(MainWindow)
        self.actionJoshua_2.setObjectName("actionJoshua_2")
        self.actionKent = QtWidgets.QAction(MainWindow)
        self.actionKent.setObjectName("actionKent")
        self.actionGrant = QtWidgets.QAction(MainWindow)
        self.actionGrant.setObjectName("actionGrant")
        self.actionThis_partition = QtWidgets.QAction(MainWindow)
        self.actionThis_partition.setObjectName("actionThis_partition")
        self.actionHow_to_use = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/idea.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHow_to_use.setIcon(icon)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.actionCSV = QtWidgets.QAction(MainWindow)
        self.actionCSV.setObjectName("actionCSV")
        self.actionPNG = QtWidgets.QAction(MainWindow)
        self.actionPNG.setObjectName("actionPNG")
        self.actionJPEG = QtWidgets.QAction(MainWindow)
        self.actionJPEG.setObjectName("actionJPEG")
        self.actionCSV_2 = QtWidgets.QAction(MainWindow)
        self.actionCSV_2.setObjectName("actionCSV_2")
        self.actionPNG_2 = QtWidgets.QAction(MainWindow)
        self.actionPNG_2.setObjectName("actionPNG_2")
        self.actionJPEG_2 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_2.setObjectName("actionJPEG_2")
        self.actionJPEG_3 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_3.setObjectName("actionJPEG_3")
        self.actionSave_image = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/picture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_image.setIcon(icon1)
        self.actionSave_image.setObjectName("actionSave_image")
        self.actionclose = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionclose.setIcon(icon2)
        self.actionclose.setObjectName("actionclose")
        self.actionExport_csv = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/calendar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport_csv.setIcon(icon3)
        self.actionExport_csv.setObjectName("actionExport_csv")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen_Recent = QtWidgets.QAction(MainWindow)
        self.actionOpen_Recent.setObjectName("actionOpen_Recent")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(resource_path("Icons/write.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon5)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.actionNew.setFont(font)
        self.actionNew.setObjectName("actionNew")
        self.actionDark_Mode = QtWidgets.QAction(MainWindow)
        self.actionDark_Mode.setObjectName("actionDark_Mode")
        self.actionLight_Mode = QtWidgets.QAction(MainWindow)
        self.actionLight_Mode.setObjectName("actionLight_Mode")
        self.actionJump_to = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(resource_path("Icons/clock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJump_to.setIcon(icon6)
        self.actionJump_to.setObjectName("actionJump_to")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(resource_path("Icons/turn_off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon7)
        self.actionExit.setObjectName("actionExit")
        self.actionShow_Summary_Table = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(resource_path("Icons/presentation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Summary_Table.setIcon(icon8)
        self.actionShow_Summary_Table.setObjectName("actionShow_Summary_Table")
        self.menuDevelopers.addAction(self.actionLyra_2)
        self.menuDevelopers.addAction(self.actionRyan_2)
        self.menuDevelopers.addAction(self.actionKent)
        self.menuDevelopers.addAction(self.actionJoshua_2)
        self.menuDevelopers.addAction(self.actionGrant)
        self.menuAbout.addAction(self.actionThis_partition)
        self.menuAbout.addAction(self.menuDevelopers.menuAction())
        self.menuHelp.addAction(self.actionHow_to_use)
        self.menuHelp.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_image)
        self.menuFile.addAction(self.actionExport_csv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionclose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAppearance_2.addAction(self.actionLight_Mode)
        self.menuAppearance_2.addAction(self.actionDark_Mode)
        self.menuAppearance.addAction(self.menuAppearance_2.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAppearance.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionJump_to)
        self.toolBar.addAction(self.actionShow_Summary_Table)

        self.label_zero = QtWidgets.QLabel(self.Group_memoryMap)
        self.label_zero.setText('0')
        self.label_zero.adjustSize()
        self.label_zero.setAlignment(QtCore.Qt.AlignRight)
        self.label_zero.setGeometry(QtCore.QRect(0, 30, 43, 13))
        self.label_zero.setObjectName("label_zero")

        self.label_memory_size = QtWidgets.QLabel(self.Group_memoryMap)
        self.label_memory_size.setText(f'{self.mem_map[0][-1]}')
        self.label_memory_size.adjustSize()
        self.label_memory_size.setAlignment(QtCore.Qt.AlignRight)
        self.label_memory_size.setGeometry(QtCore.QRect(0, self.V_END+30, 43, 13))
        self.label_memory_size.setObjectName("label_memory_size")

        self.v_line = QtWidgets.QFrame(self.Group_memoryMap)
        self.v_line.setGeometry(QtCore.QRect(40, 40, 20, self.V_END))
        self.v_line.setLineWidth(2)
        self.v_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.v_line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.v_line.setObjectName("v_line")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.make_lines(len(self.mem_map[self.idx]))
        self.make_labels(len(self.mem_map[self.idx]))
        self.make_memory_labels(self.mem_map[self.idx], self.fixed)
        self.button_state()
        self.load_job_table()
        self.load_pat_table()
        self.show_status_column()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Static Partition"))
        self.Group_memoryMap.setTitle(_translate("MainWindow", "Memory Map"))
        self.Group_job_table.setTitle(_translate("MainWindow", "Job Table"))
        item = self.Job_Table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Job"))
        item = self.Job_Table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Size"))
        item = self.Job_Table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Arrival time"))
        item = self.Job_Table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Run time"))
        self.Group_pat_table.setTitle(_translate("MainWindow", "Partition Allocation Table"))
        item = self.PAT_Table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Partition"))
        item = self.PAT_Table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Size"))
        item = self.PAT_Table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Location"))
        item = self.PAT_Table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        
        self.Group_osSize.setTitle(_translate("MainWindow", "OS Size"))
        self.OS_size_label.setText(_translate("MainWindow", f"{self.inputs['OS size']}"))
        self.Group_memSize.setTitle(_translate("MainWindow", "Memory Size"))
        self.mem_size_label.setText(_translate("MainWindow", f"{self.inputs['Memory size']}"))
        self.partition_title.setText(_translate("MainWindow", "Static Partition Memory Management"))
        self.prev_button.setText(_translate("MainWindow", "Prev"))
        self.next_button.setText(_translate("MainWindow", "Next"))
        self.simplify_cbx.setText(_translate("MainWindow", "Simplify"))
        self.message_label.setText(_translate("MainWindow", f"{self.message[0]}"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuDevelopers.setTitle(_translate("MainWindow", "Developers"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAppearance.setTitle(_translate("MainWindow", "View"))
        self.menuAppearance_2.setTitle(_translate("MainWindow", "Theme"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Tool Bar"))
        self.actionHome.setText(_translate("MainWindow", "Home"))
        self.actionLyra.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua.setText(_translate("MainWindow", "Joshua"))
        self.actionLyra_2.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan_2.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua_2.setText(_translate("MainWindow", "Joshua"))
        self.actionKent.setText(_translate("MainWindow", "Kent"))
        self.actionGrant.setText(_translate("MainWindow", "Grant"))
        self.actionThis_partition.setText(_translate("MainWindow", "This partition"))
        self.actionHow_to_use.setText(_translate("MainWindow", "How to use"))
        self.actionCSV.setText(_translate("MainWindow", "CSV"))
        self.actionPNG.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG.setText(_translate("MainWindow", "JPEG"))
        self.actionCSV_2.setText(_translate("MainWindow", "CSV"))
        self.actionPNG_2.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG_2.setText(_translate("MainWindow", "JPEG"))
        self.actionJPEG_3.setText(_translate("MainWindow", "JPEG"))
        self.actionSave_image.setText(_translate("MainWindow", "Save Image"))
        self.actionclose.setText(_translate("MainWindow", "Close"))
        self.actionExport_csv.setText(_translate("MainWindow", "Export (.csv)"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen_Recent.setText(_translate("MainWindow", "Open Recent"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionDark_Mode.setText(_translate("MainWindow", "Dark"))
        self.actionLight_Mode.setText(_translate("MainWindow", "Light"))
        self.actionJump_to.setText(_translate("MainWindow", "Jump to"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionShow_Summary_Table.setText(_translate("MainWindow", "Summary"))
        self.next_button.clicked.connect(self.next_clicked)
        self.prev_button.clicked.connect(self.prev_clicked)
        self.actionJump_to.triggered.connect(self.jump_to)
        self.actionShow_Summary_Table.triggered.connect(self.show_summary_table)
        self.actionLight_Mode.triggered.connect(self.light_theme)
        self.actionDark_Mode.triggered.connect(self.dark_theme)
        self.simplify_cbx.stateChanged.connect(self.simplify_mem_map)
        self.actionNew.triggered.connect(self.new_input)
        self.actionExit.triggered.connect(self.quitting)

        self.actionSave_image.triggered.connect(self.message_to_user)
        self.actionExport_csv.triggered.connect(self.message_to_user)
        self.actionOpen.triggered.connect(self.message_to_user)
        self.actionHow_to_use.triggered.connect(self.message_to_user)
        self.actionThis_partition.triggered.connect(self.message_to_user)

        self.actionclose.triggered.connect(self.closing)
        self.actionHome.triggered.connect(self.goto_home)
        
    def goto_home(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def message_to_user(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setText("Sorry not available right now, we're still working on this.      ")
        info.setWindowTitle("Info")
        info.exec_()

    def closing(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('This will bring you to the home window, continue?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.goto_home()

    def quitting(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to quit?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            sys.exit()
    def dark_theme(self):
        # Palette to switch to dark colors:
        # app.setStyle("Fusion")
        global dark
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette().Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette().AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette().ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette().Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)
        self.PAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #2A74BB;}')
        self.Job_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        self.dark_theme_enabled = True
        dark = True
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
    
    def light_theme(self):
        global dark
        palette = QtGui.QPalette()
        app.setPalette(palette)
        self.PAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #2A74BB;}')
        self.Job_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        self.dark_theme_enabled = False
        dark = False
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
        
        
    def load_job_table(self):
        size = self.inputs['Size']
        arrival = self.inputs['Arrival time']
        run = self.inputs['Run time']
        self.Job_Table.setRowCount(len(size))
        for row in range(len(size)):
            self.Job_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
            self.Job_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(size[row])))
            self.Job_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(arrival[row])))
            self.Job_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(run[row])))
    
    def load_pat_table(self):
        self.PAT_Table.setRowCount(len(self.partition_size))
        for row in range(len(self.partition_size)):
            self.PAT_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
            self.PAT_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.partition_size[row])))
            self.PAT_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(self.mem_map[0][row])))
            # self.PAT_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(psize[row])))
    
    def show_status_column(self):
        for row in range(len(self.status_table[self.idx])):
            self.PAT_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.status_table[self.idx][row])))

    def simplify_mem_map(self):
        if self.simplify_cbx.isChecked():
            if self.fixed == False:
                self.fixed = True
        else:
            if self.fixed == True:
                self.fixed = False
        self.show_line_LOC(self.mem_map[self.idx], self.fixed)
        self.show_label_LOC(self.mem_map[self.idx], self.fixed)
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

    def button_state(self):
        if self.idx == len(self.mem_map)-1:
            self.next_button.setEnabled(False)
            self.end_show = True
            # self.summaryButton.setStyleSheet("color: blue")
        else:
            self.next_button.setEnabled(True)
        
        if self.idx == 0:
            self.prev_button.setEnabled(False)
        else:
            self.prev_button.setEnabled(True)
        
        # self.summaryButton.setEnabled(self.end_show)

    def new_input(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.Yes)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('New file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.new_window = MyWindow()
            self.activate_window = SP_InputWindow(self.new_window)
            self.new_window.show()
            self.MainWindow.hide()

    def next_clicked(self):
        try:
            self.idx += 1
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_status_column()
            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1
        self.button_state()

    def prev_clicked(self):
        try:
            self.idx -= 1
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_status_column()
            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1
        self.button_state()
    
    def show_error_message(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setTextFormat(QtCore.Qt.RichText)
        info.setText("Sorry, an error has occured when I begin to process your data. We're still working on this, please try another input. \
                    <a href='https://www.facebook.com/xtnctx'><br><br>Tell me about the error</br></br></a>    ")
        info.setWindowTitle("Developer message")
        info.exec_()

    # Make unique objects returning in different memory location (of Python)
    def make_lines(self, length):
        self.new_mem_map = fcn.margin_memory_loc(self.mem_map[self.idx], self.V_END, y=30, fixed=self.fixed)
        for i in range(length-1):
            self.d[f"self.horizontal_line{i}"] = QtWidgets.QFrame(self.Group_memoryMap)
            self.d[f"self.horizontal_line{i}"].setLineWidth(2)
            self.d[f"self.horizontal_line{i}"].setGeometry(QtCore.QRect(50, self.new_mem_map[i]+20, 251, 16))
            self.d[f"self.horizontal_line{i}"].setFrameShape(QtWidgets.QFrame.HLine)
            self.d[f"self.horizontal_line{i}"].setFrameShadow(QtWidgets.QFrame.Raised)
            self.d[f"self.horizontal_line{i}"].setObjectName("horizontal_line")
        return self.d

    def make_labels(self, length):
        self.new_mem_map = fcn.margin_memory_loc(self.mem_map[self.idx], self.V_END, y=30, fixed=self.fixed)
        for i in range(length-1):
            self.labels[f"self.pointer_label{i}"] = QtWidgets.QLabel(self.Group_memoryMap)
            self.labels[f"self.pointer_label{i}"].setText(f"{self.mem_map[self.idx][i]}")
            self.labels[f"self.pointer_label{i}"].adjustSize()
            self.labels[f"self.pointer_label{i}"].setAlignment(QtCore.Qt.AlignRight)
            self.labels[f"self.pointer_label{i}"].setGeometry(QtCore.QRect(0, self.new_mem_map[i]+20, 43, 13))
            self.labels[f"self.pointer_label{i}"].setObjectName("pointer_label")
        return self.labels
    
    def make_memory_labels(self, mem_map, fixed):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        font.setKerning(True)

        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)
        
        length = len(mem_map)
        for i in range(length):
            self.mem_labels[f"self.memory_label{i}"] = QtWidgets.QLabel(self.Group_memoryMap)
            if 'J' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #44B432")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #6FBE28")
            elif 'wasted' in self.label[self.idx][i]:
                font.setPointSize(8)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #C64943")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #D84B4B")
            elif 'P' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #436DC6")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #3C5277")
            else:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #DBDBDB")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #4F4F4F")
            self.mem_labels[f"self.memory_label{i}"].setText(f"{self.label[self.idx][i]}")
            self.mem_labels[f"self.memory_label{i}"].adjustSize()
            self.mem_labels[f"self.memory_label{i}"].setAlignment(QtCore.Qt.AlignCenter)
            self.mem_labels[f"self.memory_label{i}"].setGeometry(QtCore.QRect(50, self.memory_label_yloc[0][i]+20, 270, 13))
            self.mem_labels[f"self.memory_label{i}"].setObjectName("memory_label")
    
    # Configure assigned variables from dictionary
    def show_line_LOC(self, mem_map, fixed):
        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        # Add missing widget
        if len(self.new_mem_map) > len(self.d)+1:
            for missing in range(len(self.d), len(self.new_mem_map)-1):
                self.d[f"self.horizontal_line{missing}"] = QtWidgets.QFrame(self.Group_memoryMap)
                self.d[f"self.horizontal_line{missing}"].setLineWidth(2)
                self.d[f"self.horizontal_line{missing}"].setGeometry(QtCore.QRect(50, self.new_mem_map[missing]+20, 251, 16))
                self.d[f"self.horizontal_line{missing}"].setFrameShape(QtWidgets.QFrame.HLine)
                self.d[f"self.horizontal_line{missing}"].setFrameShadow(QtWidgets.QFrame.Raised)
                self.d[f"self.horizontal_line{missing}"].setObjectName("horizontal_line")
        
        # Show widget
        d = dict(itertools.islice(self.d.items(), len(self.new_mem_map)-1))
        for i in range(len(d)):
            d[f"self.horizontal_line{i}"].setLineWidth(2)
            d[f"self.horizontal_line{i}"].setGeometry(QtCore.QRect(50, self.new_mem_map[i]+20, 251, 16))
            d[f"self.horizontal_line{i}"].setFrameShape(QtWidgets.QFrame.HLine)
            d[f"self.horizontal_line{i}"].setFrameShadow(QtWidgets.QFrame.Raised)
            d[f"self.horizontal_line{i}"].setObjectName("horizontal_line")
            d[f"self.horizontal_line{i}"].show()

        # Hide the excess widget
        for k in range(len(d), len(self.d)):
            self.d[f"self.horizontal_line{k}"].hide()
            # del self.d[f"self.horizontal_line{k}"]
    
    def show_label_LOC(self, mem_map, fixed):
        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        if len(self.new_mem_map) > len(self.labels)+1:
            for missing in range(len(self.labels), len(self.new_mem_map)-1):
                self.labels[f"self.pointer_label{missing}"] = QtWidgets.QLabel(self.Group_memoryMap)
                self.labels[f"self.pointer_label{missing}"].setText(f"{mem_map[missing]}")
                self.labels[f"self.pointer_label{missing}"].adjustSize()
                self.labels[f"self.pointer_label{missing}"].setAlignment(QtCore.Qt.AlignRight)
                self.labels[f"self.pointer_label{missing}"].setGeometry(QtCore.QRect(0, self.new_mem_map[missing]+20, 43, 13))
                self.labels[f"self.pointer_label{missing}"].setObjectName("pointer_label")

        p = dict(itertools.islice(self.labels.items(), len(self.new_mem_map)-1))
        for i in range(len(p)):
            p[f"self.pointer_label{i}"].setText(f"{mem_map[i]}")
            p[f"self.pointer_label{i}"].adjustSize()
            p[f"self.pointer_label{i}"].setAlignment(QtCore.Qt.AlignRight)
            p[f"self.pointer_label{i}"].setGeometry(QtCore.QRect(0, self.new_mem_map[i]+20, 43, 13))
            p[f"self.pointer_label{i}"].setObjectName("pointer_label")
            p[f"self.pointer_label{i}"].show()
            
        for k in range(len(p), len(self.labels)):
            self.labels[f"self.pointer_label{k}"].hide()
            # del self.labels[f"self.pointer_label{k}"]
    
    def show_MMlabel_LOC(self, mem_map, fixed):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        font.setKerning(True)

        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)

        if len(self.memory_label_yloc[0]) > len(self.mem_labels):
            for missing in range(len(self.mem_labels), len(self.memory_label_yloc[0])):
                self.mem_labels[f"self.memory_label{missing}"] = QtWidgets.QLabel(self.Group_memoryMap)
                self.mem_labels[f"self.memory_label{missing}"].setText(f"{self.label[self.idx][missing]}")
                self.mem_labels[f"self.memory_label{missing}"].adjustSize()
                self.mem_labels[f"self.memory_label{missing}"].setAlignment(QtCore.Qt.AlignCenter)
                self.mem_labels[f"self.memory_label{missing}"].setGeometry(QtCore.QRect(50, 
                                self.memory_label_yloc[0][missing]+20, 270, 13))
                self.mem_labels[f"self.memory_label{missing}"].setObjectName("memory_label")
        
        elif len(self.memory_label_yloc[0]) < len(self.mem_labels):
            for k in range(len(self.memory_label_yloc[0]), len(self.mem_labels)):
                self.mem_labels[f"self.memory_label{k}"].hide()
                del self.mem_labels[f"self.memory_label{k}"]

        for i in range(len(self.mem_labels)):
            if 'J' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #44B432")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #3C773D")
            elif 'wasted' in self.label[self.idx][i]:
                font.setPointSize(8)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #C64943")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #823D3D")
            elif 'P' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #436DC6")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #3C5277")
            else:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #DBDBDB")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #4F4F4F")
            self.mem_labels[f"self.memory_label{i}"].setText(f"{self.label[self.idx][i]}")
            self.mem_labels[f"self.memory_label{i}"].adjustSize()
            self.mem_labels[f"self.memory_label{i}"].setGeometry(QtCore.QRect(50, self.memory_label_yloc[0][i]+20, 270, 13))
            self.mem_labels[f"self.memory_label{i}"].setAlignment(QtCore.Qt.AlignCenter)
            self.mem_labels[f"self.memory_label{i}"].setObjectName("memory_label")
            self.mem_labels[f"self.memory_label{i}"].show()
    
    def show_summary_table(self):
        self.second_ui = SummaryTableWindow([self.start_time, self.finish, self.cpu_wait])
    
    def jump_to(self):
        self.new_window = QtWidgets.QMainWindow()
        self.second_ui = Partition_TimeList(self.new_window)
        self.second_ui.pushButton.clicked.connect(self.go_)
        self.new_window.show()
    
    def go_(self):
        if not self.idx == self.second_ui.comboBox.currentIndex():
            self.idx = self.second_ui.comboBox.currentIndex()
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_status_column()
            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

            self.button_state()

class DP_InputWindow:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.job_entries = {}
        self.size_entries = {}
        self.arrival_entries = {}
        self.run_entries = {}
        self.csv_loaded_successful = False
        self.active_file = ''
        self.max_size = 0
        self.remaining_size = 0
        self.max_partition = 0
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 655)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_job_details = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_job_details.setGeometry(QtCore.QRect(370, 30, 531, 551))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.Group_job_details.setFont(font)
        self.Group_job_details.setObjectName("Group_job_details")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Group_job_details)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 10, 25, 10)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.job_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.job_label.sizePolicy().hasHeightForWidth())
        self.job_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.job_label.setFont(font)
        self.job_label.setAlignment(QtCore.Qt.AlignCenter)
        self.job_label.setObjectName("job_label")
        self.horizontalLayout_3.addWidget(self.job_label)
        self.size_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_label.sizePolicy().hasHeightForWidth())
        self.size_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.size_label.setFont(font)
        self.size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.size_label.setObjectName("size_label")
        self.horizontalLayout_3.addWidget(self.size_label)
        self.arrival_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_label.sizePolicy().hasHeightForWidth())
        self.arrival_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.arrival_label.setFont(font)
        self.arrival_label.setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_label.setObjectName("arrival_label")
        self.horizontalLayout_3.addWidget(self.arrival_label)
        self.runtime_label = QtWidgets.QLabel(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runtime_label.sizePolicy().hasHeightForWidth())
        self.runtime_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.runtime_label.setFont(font)
        self.runtime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.runtime_label.setObjectName("runtime_label")
        self.horizontalLayout_3.addWidget(self.runtime_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.scrollArea = QtWidgets.QScrollArea(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMouseTracking(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(2)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 488, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setHorizontalSpacing(40)
        self.gridLayout.setVerticalSpacing(55)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, 150, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.import_csv_btn = QtWidgets.QPushButton(self.Group_job_details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{job number, job size*, arrival time*, run time*}')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.horizontalLayout_4.addWidget(self.import_csv_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(100, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(30)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.rmv_entry_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.rmv_entry_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rmv_entry_btn.setIcon(icon1)
        self.rmv_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.rmv_entry_btn.setCheckable(False)
        self.rmv_entry_btn.setDefault(False)
        self.rmv_entry_btn.setFlat(True)
        self.rmv_entry_btn.setObjectName("rmv_entry_btn")
        self.horizontalLayout_5.addWidget(self.rmv_entry_btn)
        self.add_entry_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.add_entry_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/plus-black-symbol.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_entry_btn.setIcon(icon2)
        self.add_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.add_entry_btn.setCheckable(False)
        self.add_entry_btn.setDefault(False)
        self.add_entry_btn.setFlat(True)
        self.add_entry_btn.setObjectName("add_entry_btn")
        self.horizontalLayout_5.addWidget(self.add_entry_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.Group_memSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memSize.setGeometry(QtCore.QRect(26, 325, 151, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Group_memSize.setFont(font)
        self.Group_memSize.setObjectName("Group_memSize")
        self.memSize_value = QtWidgets.QSpinBox(self.Group_memSize)
        self.memSize_value.setGeometry(QtCore.QRect(14, 40, 121, 29))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.memSize_value.sizePolicy().hasHeightForWidth())
        self.memSize_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.memSize_value.setFont(font)
        self.memSize_value.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.memSize_value.setAlignment(QtCore.Qt.AlignCenter)
        self.memSize_value.setMaximum(999999999)
        self.memSize_value.setSingleStep(5)
        self.memSize_value.setProperty("value", 0)
        self.memSize_value.setObjectName("memSize_value")
        self.Group_osSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_osSize.setGeometry(QtCore.QRect(206, 325, 141, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Group_osSize.setFont(font)
        self.Group_osSize.setObjectName("Group_osSize")
        self.osSize_value = QtWidgets.QSpinBox(self.Group_osSize)
        self.osSize_value.setGeometry(QtCore.QRect(13, 40, 121, 29))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.osSize_value.sizePolicy().hasHeightForWidth())
        self.osSize_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.osSize_value.setFont(font)
        self.osSize_value.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.osSize_value.setAlignment(QtCore.Qt.AlignCenter)
        self.osSize_value.setMaximum(999999999)
        self.osSize_value.setSingleStep(5)
        self.osSize_value.setProperty("value", 0)
        self.osSize_value.setObjectName("osSize_value")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(800, 615, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_btn.setIcon(icon3)
        self.start_btn.setIconSize(QtCore.QSize(20, 20))
        self.start_btn.setCheckable(False)
        self.start_btn.setAutoDefault(False)
        self.start_btn.setDefault(False)
        self.start_btn.setFlat(True)
        self.start_btn.setObjectName("start_btn")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(-10, 615, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.back_btn.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_btn.setIcon(icon4)
        self.back_btn.setIconSize(QtCore.QSize(20, 20))
        self.back_btn.setCheckable(False)
        self.back_btn.setAutoDefault(False)
        self.back_btn.setDefault(False)
        self.back_btn.setFlat(True)
        self.back_btn.setObjectName("back_btn")

        self.Group_Dynamic = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_Dynamic.setGeometry(QtCore.QRect(26, 150, 321, 150))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.Group_Dynamic.setFont(font)
        self.Group_Dynamic.setFlat(False)
        self.Group_Dynamic.setCheckable(False)
        self.Group_Dynamic.setObjectName("Group_Dynamic")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Group_Dynamic)
        self.gridLayout_3.setObjectName("gridLayout_3")

        

        self.comboBox = QtWidgets.QComboBox(self.Group_Dynamic)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)

        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.icon = QtGui.QIcon()
        self.gridLayout_3.addWidget(self.comboBox, 0, 0, 1, 1)
        self.comboBox.addItem(f'Best Fit')
        self.comboBox.addItem(f'First Fit')
        
        self.compaction_cbx_horizontal_layout = QtWidgets.QVBoxLayout()
        self.compaction_cbx_horizontal_layout.setContentsMargins(0, 0, -1, 0)
        self.compaction_cbx_horizontal_layout.setObjectName("gridLayout_3")
        
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(60)
        font.setKerning(True)

        self.compaction_cbx = QtWidgets.QCheckBox(self.Group_Dynamic)
        self.compaction_cbx.setGeometry(QtCore.QRect(0, 0, 0, 19))
        self.compaction_cbx.setFont(font)
        self.compaction_cbx.setStyleSheet("QCheckBox::indicator" "{" "width :15;" "height : 15;""}")
        self.compaction_cbx.setObjectName("compaction_cbx")
        self.compaction_cbx_horizontal_layout.addWidget(self.compaction_cbx)
        self.gridLayout_3.addLayout(self.compaction_cbx_horizontal_layout, 1, 0, 1, 1)

        self.jv_line = QtWidgets.QFrame(self.centralwidget)
        self.jv_line.setGeometry(QtCore.QRect(373, 70, 21, 41))
        self.jv_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.jv_line.setLineWidth(2)
        global dark
        if dark == True:
            self.jv_line.setStyleSheet('color: #FFFFFF')
        else:
            self.jv_line.setStyleSheet('color: #838383')
        self.jv_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.jv_line.setObjectName("jv_line")

        self.jv_line2 = QtWidgets.QFrame(self.centralwidget)
        self.jv_line2.setGeometry(QtCore.QRect(878, 70, 21, 41))
        self.jv_line2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.jv_line2.setLineWidth(2)
        if dark == True:
            self.jv_line2.setStyleSheet('color: #FFFFFF')
        else:
            self.jv_line2.setStyleSheet('color: #838383')
        self.jv_line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.jv_line2.setObjectName("jv_line2")


        self.jh_line = QtWidgets.QFrame(self.centralwidget)
        self.jh_line.setGeometry(QtCore.QRect(382, 60, 507, 20))
        self.jh_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.jh_line.setLineWidth(2)
        if dark == True:
            self.jh_line.setStyleSheet('color: #FFFFFF')
        else:
            self.jh_line.setStyleSheet('color: #838383')
        self.jh_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.jh_line.setObjectName("jh_line")
        self.Group_job_details.raise_()
        self.Group_memSize.raise_()
        self.Group_osSize.raise_()
        self.start_btn.raise_()
        self.back_btn.raise_()
        self.Group_Dynamic.raise_()
        self.jv_line.raise_()
        self.jh_line.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 21))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.make_default_entry(default_entry)
        # self.make_default_partition_count(default_partition_count)
        
        self.entry_detail_state()
        self.memSize_value.textChanged.connect(self.entry_detail_state)
        self.osSize_value.textChanged.connect(self.entry_detail_state)
        self.memSize_value.selectAll()
        self.button_state()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dynamic Partition"))
        self.Group_job_details.setTitle(_translate("MainWindow", "Job Details"))
        self.job_label.setText(_translate("MainWindow", "Job"))
        self.size_label.setText(_translate("MainWindow", "Size"))
        self.arrival_label.setText(_translate("MainWindow", "Arrival time"))
        self.runtime_label.setText(_translate("MainWindow", "Run time"))
        self.import_csv_btn.setText(_translate("MainWindow", "  Import CSV"))
        self.Group_memSize.setTitle(_translate("MainWindow", "Memory Size"))
        self.Group_osSize.setTitle(_translate("MainWindow", "OS Size"))
        self.start_btn.setText(_translate("MainWindow", "  Start"))
        self.back_btn.setText(_translate("MainWindow", "  Back"))
        self.Group_Dynamic.setTitle(_translate("MainWindow", "Dynamic Partitioned Allocation"))

        self.compaction_cbx.setText(_translate("MainWindow", "With compaction"))
        self.start_btn.clicked.connect(self.start)
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.add_entry_btn.clicked.connect(self.add_entry)
        self.rmv_entry_btn.clicked.connect(self.remove_entry)

        self.back_btn.clicked.connect(self.back_to_start_up)

    def back_to_start_up(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def message_to_user(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setText("Sorry not available right now, we're still working on this.      ")
        info.setWindowTitle("Info")
        info.exec_()

    def make_default_entry(self, default_entry):
        for _ in range(default_entry):
            self.add_entry()

    def add_entry(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Job No.
        self.job_entries[f"job{len(self.job_entries)+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.job_entries[f"job{len(self.job_entries)}"].setText(f"{len(self.job_entries)}")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.job_entries[f"job{len(self.job_entries)}"].sizePolicy().hasHeightForWidth())
        self.job_entries[f"job{len(self.job_entries)}"].setSizePolicy(sizePolicy)
        self.job_entries[f"job{len(self.job_entries)}"].setFont(font)
        self.job_entries[f"job{len(self.job_entries)}"].setScaledContents(False)
        self.job_entries[f"job{len(self.job_entries)}"].setAlignment(QtCore.Qt.AlignCenter)
        self.job_entries[f"job{len(self.job_entries)}"].setObjectName(f"job{len(self.job_entries)}")
        self.gridLayout.addWidget(self.job_entries[f"job{len(self.job_entries)}"], len(self.job_entries), 0, 1, 1)
        
    #Size
        self.size_entries[f'size{len(self.size_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_entries[f'size{len(self.size_entries)}'].sizePolicy().hasHeightForWidth())
        self.size_entries[f'size{len(self.size_entries)}'].setSizePolicy(sizePolicy)
        self.size_entries[f'size{len(self.size_entries)}'].setFont(font)
        self.size_entries[f'size{len(self.size_entries)}'].setMinimum(0)
        self.size_entries[f'size{len(self.size_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.size_entries[f'size{len(self.size_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.size_entries[f'size{len(self.size_entries)}'].setMaximum(self.memSize_value.value() - self.osSize_value.value())
        self.size_entries[f'size{len(self.size_entries)}'].setSingleStep(5)
        self.size_entries[f'size{len(self.size_entries)}'].setProperty("value", 0)
        self.size_entries[f'size{len(self.size_entries)}'].setObjectName(f'size{len(self.size_entries)}')
        self.gridLayout.addWidget(self.size_entries[f'size{len(self.size_entries)}'], len(self.size_entries), 1, 1, 1)
        
    #Arrival
        self.arrival_entries[f'arrival{len(self.arrival_entries)+1}'] = QtWidgets.QTimeEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{len(self.arrival_entries)}'].sizePolicy().hasHeightForWidth())
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setSizePolicy(sizePolicy)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setDisplayFormat("h:mm")
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setFont(font)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setObjectName(f'arrival{len(self.arrival_entries)}')
        self.gridLayout.addWidget(self.arrival_entries[f'arrival{len(self.arrival_entries)}'], len(self.arrival_entries), 2, 1, 1)
        
    #Run
        self.run_entries[f'run{len(self.run_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_entries[f'run{len(self.run_entries)}'].sizePolicy().hasHeightForWidth())
        self.run_entries[f'run{len(self.run_entries)}'].setSizePolicy(sizePolicy)
        self.run_entries[f'run{len(self.run_entries)}'].setFont(font)
        self.run_entries[f'run{len(self.run_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.run_entries[f'run{len(self.run_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.run_entries[f'run{len(self.run_entries)}'].setMaximum(999999999)
        self.run_entries[f'run{len(self.run_entries)}'].setSingleStep(5)
        self.run_entries[f'run{len(self.run_entries)}'].setProperty("value", 0)
        self.run_entries[f'run{len(self.run_entries)}'].setObjectName(f'run{len(self.run_entries)}')
        self.gridLayout.addWidget(self.run_entries[f'run{len(self.run_entries)}'], len(self.run_entries), 3, 1, 1)

        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()

    def remove_entry(self):
        self.job_entries[f"job{len(self.job_entries)}"].hide()
        self.size_entries[f'size{len(self.size_entries)}'].hide()
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].hide()
        self.run_entries[f'run{len(self.run_entries)}'].hide()

        del self.job_entries[f"job{len(self.job_entries)}"]
        del self.size_entries[f'size{len(self.size_entries)}']
        del self.arrival_entries[f'arrival{len(self.arrival_entries)}']
        del self.run_entries[f'run{len(self.run_entries)}']
        
        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()

    def button_state(self):
        if self.csv_loaded_successful:
            self.add_entry_btn.setEnabled(False)
            self.rmv_entry_btn.setEnabled(False)
        else:
            if len(self.job_entries) == 1:
                self.rmv_entry_btn.setEnabled(False)
            else:
                self.rmv_entry_btn.setEnabled(True)
            self.add_entry_btn.setEnabled(True)
    
    def make_import_btn(self):
        self.import_csv_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.import_csv_btn.setGeometry(QtCore.QRect(270, 535, 100, 20))
        self.import_csv_btn.setText("  Import CSV")
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{job number, job size*, arrival time*, run time*}')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.horizontalLayout_4.addWidget(self.import_csv_btn)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon2)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.import_csv_btn.show()
    
    def make_cancel_csv_btn(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)

        self.cancel_csv_btn = QtWidgets.QPushButton(self.Group_job_details)
        self.cancel_csv_btn.setGeometry(QtCore.QRect(270, 528, 32, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_csv_btn.sizePolicy().hasHeightForWidth())
        self.cancel_csv_btn.setSizePolicy(sizePolicy)
        self.cancel_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.horizontalLayout_4.addWidget(self.cancel_csv_btn)
        
        self.cancel_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon_red.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_csv_btn.setIcon(icon2)
        self.cancel_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.cancel_csv_btn.setCheckable(False)
        self.cancel_csv_btn.setDefault(False)
        self.cancel_csv_btn.setFlat(True)
        self.cancel_csv_btn.setObjectName("cancel_csv_btn")
        self.cancel_csv_btn.clicked.connect(self.cancel_csv)

        self.file_name_label = QtWidgets.QLabel(self.Group_job_details)
        self.file_name_label.setFont(font)
        self.file_name_label.setObjectName('file_name_label')
        self.file_name_label.setGeometry(QtCore.QRect(302, 535, 100, 20))
        self.file_name_label.setText(self.active_file)
        self.file_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_name_label.adjustSize()
        self.horizontalLayout_4.addWidget(self.file_name_label)

    def cancel_csv(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to remove this file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            print('Yes  ')
            self.cancel_csv_btn.hide()
            self.file_name_label.hide()
            del self.cancel_csv_btn
            del self.file_name_label

            for _ in range(len(self.job_entries)):
                self.remove_entry()
            self.make_default_entry(default_entry)
            self.entry_detail_state()

            self.make_import_btn()
            self.max_size = 0
            self.memSize_value.setMaximum(999999999)
            self.memSize_value.textChanged.connect(self.entry_detail_state)
            self.osSize_value.textChanged.connect(self.entry_detail_state)

            self.add_entry_btn.setEnabled(True)
            self.rmv_entry_btn.setEnabled(True)
            
            # QtWidgets.QSpinBox().clear
            self.csv_loaded_successful = False

    def getFileDir(self):
        file_filter = '*.csv'
        response = QtWidgets.QFileDialog.getOpenFileNames(
            parent = QtWidgets.QWidget(),
            caption='Select a csv file',
            directory = os.getcwd(),
            filter=file_filter
        )
        self.active_file = response[0][0].split('/')[-1]
        return response[0][0]

    def import_csv(self):
        try:
            fileDir = self.getFileDir()
            csv = pd.read_csv(fileDir)
            column_name = list(csv.columns)
            jobs = csv[column_name[0]].tolist()
            job_size = csv[column_name[1]].tolist()
            arrival_time = csv[column_name[2]].tolist()
            run_time = csv[column_name[3]].tolist()

            for _ in range(len(self.job_entries)):
                self.remove_entry()
            self.import_csv_btn.hide()
            del self.import_csv_btn
            self.make_cancel_csv_btn()
            self.load_csv_to_window(jobs, job_size, arrival_time, run_time)

        except IndexError:
            print('No file selected')

    def load_csv_to_window(self, j, s, a, r):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Job No.
        for i in range(len(a)):
            self.job_entries[f"job{i+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.job_entries[f"job{i+1}"].setText(f"{i+1}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.job_entries[f"job{i+1}"].sizePolicy().hasHeightForWidth())
            self.job_entries[f"job{i+1}"].setSizePolicy(sizePolicy)
            self.job_entries[f"job{i+1}"].setFont(font)
            self.job_entries[f"job{i+1}"].setScaledContents(False)
            self.job_entries[f"job{i+1}"].setAlignment(QtCore.Qt.AlignCenter)
            self.job_entries[f"job{i+1}"].setObjectName(f"job{i+1}")
            self.gridLayout.addWidget(self.job_entries[f"job{i+1}"], i+1, 0, 1, 1)
    #Size
        for i in range(len(a)):
            self.size_entries[f'size{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.size_entries[f'size{i+1}'].setText(f"{s[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.size_entries[f'size{i+1}'].sizePolicy().hasHeightForWidth())
            self.size_entries[f'size{i+1}'].setSizePolicy(sizePolicy)
            self.size_entries[f'size{i+1}'].setFont(font)
            self.size_entries[f'size{i+1}'].setScaledContents(False)
            self.size_entries[f'size{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.size_entries[f'size{i+1}'].setObjectName(f"size{i+1}")
            self.gridLayout.addWidget(self.size_entries[f'size{i+1}'], i+1, 1, 1, 1)
    #Arrival
        for i in range(len(a)):
            self.arrival_entries[f'arrival{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.arrival_entries[f'arrival{i+1}'].setText(f"{a[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{i+1}'].sizePolicy().hasHeightForWidth())
            self.arrival_entries[f'arrival{i+1}'].setSizePolicy(sizePolicy)
            self.arrival_entries[f'arrival{i+1}'].setFont(font)
            self.arrival_entries[f'arrival{i+1}'].setScaledContents(False)
            self.arrival_entries[f'arrival{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.arrival_entries[f'arrival{i+1}'].setObjectName(f"arrival{i+1}")
            self.gridLayout.addWidget(self.arrival_entries[f'arrival{i+1}'], i+1, 2, 1, 1)
    #Run
        for i in range(len(a)):
            self.run_entries[f'run{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.run_entries[f'run{i+1}'].setText(f"{r[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.run_entries[f'run{i+1}'].sizePolicy().hasHeightForWidth())
            self.run_entries[f'run{i+1}'].setSizePolicy(sizePolicy)
            self.run_entries[f'run{i+1}'].setFont(font)
            self.run_entries[f'run{i+1}'].setScaledContents(False)
            self.run_entries[f'run{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.run_entries[f'run{i+1}'].setObjectName(f"run{i+1}")
            self.gridLayout.addWidget(self.run_entries[f'run{i+1}'], i+1, 3, 1, 1)

        self.max_size = max(s)
        self.memSize_value.textChanged.connect(self.entry_detail_state_QLabel)
        self.osSize_value.textChanged.connect(self.entry_detail_state_QLabel)

        self.csv_loaded_successful = True
        self.Group_job_details.setEnabled(True)
        self.add_entry_btn.setEnabled(False)
        self.rmv_entry_btn.setEnabled(False)
        
        self.entry_detail_state_QLabel()
        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.minimum()))

    def entry_detail_state(self):
        global dark
        if dark == True:
            self.jh_line.setStyleSheet('color: #FFFFFF')
        else:
            self.jh_line.setStyleSheet('color: #838383')
        if dark == False:
            if self.memSize_value.value() != 0:
                self.Group_job_details.setEnabled(True)
                self.jv_line.setStyleSheet('color: black')
                self.jv_line2.setStyleSheet('color: black')
                self.jh_line.setStyleSheet('color: black')
            else:
                self.Group_job_details.setEnabled(False)
                self.jv_line.setStyleSheet('color: #838383')
                self.jv_line2.setStyleSheet('color: #838383')
                self.jh_line.setStyleSheet('color: #838383')
        else:
            if self.memSize_value.value() != 0:
                self.Group_job_details.setEnabled(True)
                self.jv_line.setStyleSheet('color: #FFFFFF')
                self.jv_line2.setStyleSheet('color: #FFFFFF')
                self.jh_line.setStyleSheet('color: #FFFFFF')
            else:
                self.Group_job_details.setEnabled(False)
                self.jv_line.setStyleSheet('color: #FFFFFF')
                self.jv_line2.setStyleSheet('color: #FFFFFF')
                self.jh_line.setStyleSheet('color: #FFFFFF')

        if type(self.size_entries['size1']).__name__ != 'QLabel':
            if self.memSize_value.value() != 0:
                for i in range(len(self.job_entries)):
                    list(self.size_entries.values())[i].setMaximum(self.memSize_value.value() - self.osSize_value.value())
                    if list(self.size_entries.values())[i].value() < 0:
                        list(self.size_entries.values())[i].setProperty("value", 0)
                self.Group_job_details.setEnabled(True)
            else:
                self.Group_job_details.setEnabled(False)           
            self.osSize_value.setMaximum(self.memSize_value.value())

    def entry_detail_state_QLabel(self):
        if type(self.size_entries['size1']).__name__ == 'QLabel':
            self.memSize_value.setMinimum(self.max_size)
            self.osSize_value.setMaximum(self.memSize_value.value())

    def start(self):
        print(type(self.size_entries['size1']).__name__, '<----------------------')
        # Validate Inputs
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setIcon(QtWidgets.QMessageBox.Information)
        notify_user.setFont(font)

        err_msg = QtWidgets.QMessageBox()
        err_msg.setIcon(QtWidgets.QMessageBox.Information)
        err_msg.setFont(font)
        
        self.validated = True
        for _ in range(1):
            if self.memSize_value.value() <= self.osSize_value.value():
                self.validated = False
                err_msg.setText('Sizes must be:\nMemory size > OS size > 0      ')
                err_msg.setWindowTitle("Memory Error")
                err_msg.exec_()
                self.memSize_value.setFocus()
                self.memSize_value.selectAll()
                self.Group_job_details.setEnabled(False)
                break
                
            elif self.osSize_value.value() <= 0:
                self.validated = False
                err_msg.setText('Sizes must be:\nMemory size > OS size > 0      ')
                err_msg.setWindowTitle("Memory Error")
                err_msg.exec_()
                self.osSize_value.setFocus()
                self.osSize_value.selectAll()
                self.Group_job_details.setEnabled(False)
                break

            elif self.max_size > (self.memSize_value.value() - self.osSize_value.value()):
                self.validated = False
                err_msg.setText(f'Job sizes must fit !\n ~max={self.max_size}                  ')
                err_msg.setWindowTitle("Size Error")
                err_msg.exec_()
                break

            for i in range(len(self.job_entries)):
                if type(self.size_entries['size1']).__name__ == 'QLabel':
                    if list(self.size_entries.values())[i].text() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.size_entries.values())[i].setFocus()
                        list(self.size_entries.values())[i].selectAll()
                        break
                    if list(self.arrival_entries.values())[i].text().split(':')[0] == '0':
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.arrival_entries.values())[i].setFocus()
                        list(self.arrival_entries.values())[i].selectAll()
                        break
                    if list(self.run_entries.values())[i].text() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.run_entries.values())[i].setFocus()
                        list(self.run_entries.values())[i].selectAll()
                        break
                else:
                    if list(self.size_entries.values())[i].value() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.size_entries.values())[i].setFocus()
                        list(self.size_entries.values())[i].selectAll()
                        yloc = list(self.size_entries.values())[i].y() - list(self.size_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
                    if list(self.arrival_entries.values())[i].text().split(':')[0] == '0':
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.arrival_entries.values())[i].setFocus()
                        list(self.arrival_entries.values())[i].selectAll()
                        yloc = list(self.arrival_entries.values())[i].y() - list(self.arrival_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
                    if list(self.run_entries.values())[i].value() == 0:
                        self.validated = False
                        err_msg.setText('Time and sizes must be greater than 0      ')
                        err_msg.setWindowTitle("Job Error")
                        err_msg.exec_()
                        list(self.run_entries.values())[i].setFocus()
                        list(self.run_entries.values())[i].selectAll()
                        yloc = list(self.run_entries.values())[i].y() - list(self.run_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
        
        if self.validated == False and self.csv_loaded_successful == True:
            self.Group_job_details.setEnabled(True)

    # Export JSON
        if self.validated:
            if type(self.size_entries['size1']).__name__ == 'QLabel':
                dictionary ={
                'Memory size' : self.memSize_value.value(),
                'OS size' : self.osSize_value.value(),
                'Job' : [job.text() for job in self.job_entries.values()],
                'Size' : [int(size.text()) for size in self.size_entries.values()],
                'Arrival time' : [arrival.text() for arrival in self.arrival_entries.values()],
                'Run time' : [int(run.text()) for run in self.run_entries.values()]
                }
            else:
                dictionary ={
                'Memory size' : self.memSize_value.value(),
                'OS size' : self.osSize_value.value(),
                'Job' : [job.text() for job in self.job_entries.values()],
                'Size' : [int(size.value()) for size in self.size_entries.values()],
                'Arrival time' : [arrival.text() for arrival in self.arrival_entries.values()],
                'Run time' : [int(run.value()) for run in self.run_entries.values()]
                }

            if dictionary["Arrival time"] != fcn.sort_time(dictionary["Arrival time"]):
                notify_user.setText('Unsorted arrival detected\n~Inputs are now sorted by arrival !      ')
                notify_user.setWindowTitle("Sort by Arrival")
                notify_user.button
                notify_user.setStandardButtons
                notify_user.exec_()

        # Sort by Arrival
            for i in range(len(dictionary['Arrival time'])-1):
                for j in range(0, len(dictionary['Arrival time'])-i-1):
                    if fcn.to_minutes(dictionary['Arrival time'][j]) > fcn.to_minutes(dictionary['Arrival time'][j+1]):
                        dictionary['Arrival time'][j], dictionary['Arrival time'][j+1] = dictionary['Arrival time'][j+1], dictionary['Arrival time'][j]
                        dictionary['Size'][j], dictionary['Size'][j+1] = dictionary['Size'][j+1], dictionary['Size'][j]
                        dictionary['Run time'][j], dictionary['Run time'][j+1] = dictionary['Run time'][j+1], dictionary['Run time'][j]

            with open(f"{usrfile_name}.json", "w") as outfile:
                json.dump(dictionary, outfile, indent=4)

            global D
            global X
            
            D = dictionary
            if self.comboBox.currentText() == 'Best Fit':
                X = db.dynamic_bestfit_EXEC(usrfile_name, self.compaction_cbx.isChecked())
            else:
                X = df.dynamic_firstfit_EXEC(usrfile_name, self.compaction_cbx.isChecked())

            self.next_window(D, X)
            print('VALIDATAED')

        else:
            print('NOT VALIDATED')

    def next_window(self, inputs, Data):
        self.newWindow = MyWindow()
        self.second_ui = DP_ProcessWindow(self.newWindow, inputs, Data)
        self.second_ui.partition_title.setText(f'Dynamic {self.comboBox.currentText()} Partition Allocation')
        if self.compaction_cbx.isChecked():
            self.second_ui.Group_memoryMap.setTitle(f'Memory Map - with compaction')
        else:
            self.second_ui.Group_memoryMap.setTitle(f'Memory Map - without compaction')
        self.newWindow.show()
        self.MainWindow.hide()

class DP_ProcessWindow:
    V_END = 470
    def __init__(self, MainWindow, inputs, D):
        self.mem_map, self.label, self.message, self.f_list, self.p_list,  = D[0], D[1], D[2], D[3], D[4]
        self.start_time, self.finish, self.cpu_wait = D[5], D[6], D[7]
        self.inputs = inputs
        self.MainWindow = MainWindow
        self.idx = 0
        self.fixed = False
        self.d = {}
        self.labels = {}
        self.mem_labels ={}
        self.end_show = False
        self.error_msg_value = 0
        global dark
        self.dark_theme_enabled = dark
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 655)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_memoryMap = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memoryMap.setGeometry(QtCore.QRect(510, 10, 321, 540))

        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Group_memoryMap.setFont(font)
        self.Group_memoryMap.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Group_memoryMap.setObjectName("Group_memoryMap")
        self.Group_FAT_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_FAT_table.setGeometry(QtCore.QRect(20, 119, 451, 215))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_FAT_table.setFont(font)
        self.Group_FAT_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_FAT_table.setCheckable(False)
        self.Group_FAT_table.setChecked(False)
        self.Group_FAT_table.setObjectName("Group_FAT_table")
        self.FAT_Table = QtWidgets.QTableWidget(self.Group_FAT_table)
        self.FAT_Table.setGeometry(QtCore.QRect(10, 27, 432, 181))
        self.FAT_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.FAT_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.FAT_Table.setFont(font)
        self.FAT_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.FAT_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.FAT_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.FAT_Table.verticalHeader().setVisible(False) # Row Index
        self.FAT_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.FAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        
        self.FAT_Table.setAutoScroll(True)
        self.FAT_Table.setAlternatingRowColors(True)
        self.FAT_Table.setObjectName("FAT_Table")
        self.FAT_Table.setColumnCount(4)
        self.FAT_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.FAT_Table.setHorizontalHeaderItem(0, item)
        self.FAT_Table.setItemDelegateForColumn(0, AlignDelegate(self.FAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.FAT_Table.setHorizontalHeaderItem(1, item)
        self.FAT_Table.setItemDelegateForColumn(1, AlignDelegate(self.FAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.FAT_Table.setHorizontalHeaderItem(2, item)
        self.FAT_Table.setItemDelegateForColumn(2, AlignDelegate(self.FAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.FAT_Table.setHorizontalHeaderItem(3, item)
        self.FAT_Table.setItemDelegateForColumn(3, AlignDelegate(self.FAT_Table))
        self.FAT_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.FAT_Table.horizontalHeaderItem(0).setFont(font)
        self.FAT_Table.horizontalHeaderItem(1).setFont(font)
        self.FAT_Table.horizontalHeaderItem(2).setFont(font)
        self.FAT_Table.horizontalHeaderItem(3).setFont(font)
             
        self.FAT_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.FAT_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.FAT_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.FAT_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # self.Job_Table.verticalHeader().setDefaultSectionSize(44)

        self.Group_pat_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_pat_table.setGeometry(QtCore.QRect(20, 350, 451, 215))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_pat_table.setFont(font)
        self.Group_pat_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_pat_table.setCheckable(False)
        self.Group_pat_table.setChecked(False)
        self.Group_pat_table.setObjectName("Group_pat_table")

        self.PAT_Table = QtWidgets.QTableWidget(self.Group_pat_table)
        self.PAT_Table.setGeometry(QtCore.QRect(10, 27, 432, 181))
        self.PAT_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PAT_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PAT_Table.setFont(font)
        self.PAT_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.PAT_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PAT_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.PAT_Table.verticalHeader().setVisible(False) # Row Index
        self.PAT_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.PAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #2A74BB;}')
        
        self.PAT_Table.setAutoScroll(True)
        self.PAT_Table.setAlternatingRowColors(True)
        self.PAT_Table.setObjectName("PAT_Table")
        self.PAT_Table.setColumnCount(4)
        self.PAT_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(0, item)
        self.PAT_Table.setItemDelegateForColumn(0, AlignDelegate(self.PAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(1, item)
        self.PAT_Table.setItemDelegateForColumn(1, AlignDelegate(self.PAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(2, item)
        self.PAT_Table.setItemDelegateForColumn(2, AlignDelegate(self.PAT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.PAT_Table.setHorizontalHeaderItem(3, item)
        self.PAT_Table.setItemDelegateForColumn(3, AlignDelegate(self.PAT_Table))
        self.PAT_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.PAT_Table.horizontalHeaderItem(0).setFont(font)
        self.PAT_Table.horizontalHeaderItem(1).setFont(font)
        self.PAT_Table.horizontalHeaderItem(2).setFont(font)
        self.PAT_Table.horizontalHeaderItem(3).setFont(font)
             
        self.PAT_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.PAT_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.PAT_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.PAT_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # self.Job_Table.verticalHeader().setDefaultSectionSize(44)

        self.Group_osSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_osSize.setGeometry(QtCore.QRect(350, 70, 120, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_osSize.setFont(font)
        self.Group_osSize.setObjectName("Group_osSize")
        self.OS_size_label = QtWidgets.QLabel(self.Group_osSize)
        self.OS_size_label.setEnabled(True)
        self.OS_size_label.setGeometry(QtCore.QRect(10, 18, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.OS_size_label.setFont(font)
        self.OS_size_label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.OS_size_label.setMouseTracking(False)
        self.OS_size_label.setTabletTracking(False)
        self.OS_size_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.OS_size_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.OS_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.OS_size_label.setObjectName("OS_size_label")
        self.Group_memSize = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memSize.setGeometry(QtCore.QRect(30, 70, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_memSize.setFont(font)
        self.Group_memSize.setFlat(False)
        self.Group_memSize.setCheckable(False)
        self.Group_memSize.setObjectName("Group_memSize")
        self.mem_size_label = QtWidgets.QLabel(self.Group_memSize)
        self.mem_size_label.setGeometry(QtCore.QRect(20, 18, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mem_size_label.setFont(font)
        self.mem_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mem_size_label.setObjectName("mem_size_label")
        self.partition_title = QtWidgets.QLabel(self.centralwidget)
        self.partition_title.setGeometry(QtCore.QRect(20, 5, 451, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.partition_title.setFont(font)
        self.partition_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.partition_title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.partition_title.setLineWidth(1)
        self.partition_title.setAlignment(QtCore.Qt.AlignCenter)
        self.partition_title.setObjectName("partition_title")
        self.prev_button = QtWidgets.QPushButton(self.centralwidget)
        self.prev_button.setGeometry(QtCore.QRect(550, 565, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.prev_button.setFont(font)
        self.prev_button.setObjectName("prev_button")
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(700, 565, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.next_button.setFont(font)
        self.next_button.setObjectName("next_button")
        self.simplify_cbx = QtWidgets.QCheckBox(self.centralwidget)
        self.simplify_cbx.setGeometry(QtCore.QRect(775, 605, 65, 19))
        self.simplify_cbx.setFont(font)
        self.simplify_cbx.setObjectName("simplify_cbx")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(18, 560, 451, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.message_label.setFont(font)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setObjectName("message_label")
        self.horizontalLayout.addWidget(self.message_label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 28))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuHelp.setFont(font)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAbout = QtWidgets.QMenu(self.menuHelp)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAbout.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/message.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAbout.setIcon(icon)
        self.menuAbout.setObjectName("menuAbout")
        self.menuDevelopers = QtWidgets.QMenu(self.menuAbout)
        icon0 = QtGui.QIcon()
        icon0.addPixmap(QtGui.QPixmap(resource_path("Icons/group.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuDevelopers.setIcon(icon0)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuDevelopers.setFont(font)
        self.menuDevelopers.setObjectName("menuDevelopers")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuAppearance = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance.setFont(font)
        self.menuAppearance.setObjectName("menuAppearance")
        self.menuAppearance_2 = QtWidgets.QMenu(self.menuAppearance)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance_2.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/favorite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAppearance_2.setIcon(icon)
        self.menuAppearance_2.setObjectName("menuAppearance_2")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.toolBar.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setAcceptDrops(False)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setMovable(True)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setIconSize(QtCore.QSize(30, 25))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionHome = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/house_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon)
        self.actionHome.setObjectName("actionHome")
        self.actionLyra = QtWidgets.QAction(MainWindow)
        self.actionLyra.setObjectName("actionLyra")
        self.actionRyan = QtWidgets.QAction(MainWindow)
        self.actionRyan.setObjectName("actionRyan")
        self.actionJoshua = QtWidgets.QAction(MainWindow)
        self.actionJoshua.setObjectName("actionJoshua")
        self.actionLyra_2 = QtWidgets.QAction(MainWindow)
        self.actionLyra_2.setObjectName("actionLyra_2")
        self.actionRyan_2 = QtWidgets.QAction(MainWindow)
        self.actionRyan_2.setObjectName("actionRyan_2")
        self.actionJoshua_2 = QtWidgets.QAction(MainWindow)
        self.actionJoshua_2.setObjectName("actionJoshua_2")
        self.actionKent = QtWidgets.QAction(MainWindow)
        self.actionKent.setObjectName("actionKent")
        self.actionGrant = QtWidgets.QAction(MainWindow)
        self.actionGrant.setObjectName("actionGrant")
        self.actionThis_partition = QtWidgets.QAction(MainWindow)
        iconx = QtGui.QIcon()
        iconx.addPixmap(QtGui.QPixmap(resource_path("Icons/page.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionThis_partition.setIcon(iconx)
        self.actionThis_partition.setObjectName("actionThis_partition")
        self.actionHow_to_use = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/idea.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHow_to_use.setIcon(icon)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.actionCSV = QtWidgets.QAction(MainWindow)
        self.actionCSV.setObjectName("actionCSV")
        self.actionPNG = QtWidgets.QAction(MainWindow)
        self.actionPNG.setObjectName("actionPNG")
        self.actionJPEG = QtWidgets.QAction(MainWindow)
        self.actionJPEG.setObjectName("actionJPEG")
        self.actionCSV_2 = QtWidgets.QAction(MainWindow)
        self.actionCSV_2.setObjectName("actionCSV_2")
        self.actionPNG_2 = QtWidgets.QAction(MainWindow)
        self.actionPNG_2.setObjectName("actionPNG_2")
        self.actionJPEG_2 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_2.setObjectName("actionJPEG_2")
        self.actionJPEG_3 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_3.setObjectName("actionJPEG_3")
        self.actionSave_image = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/picture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_image.setIcon(icon1)
        self.actionSave_image.setObjectName("actionSave_image")
        self.actionclose = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionclose.setIcon(icon2)
        self.actionclose.setObjectName("actionclose")
        self.actionExport_csv = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/calendar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport_csv.setIcon(icon3)
        self.actionExport_csv.setObjectName("actionExport_csv")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen_Recent = QtWidgets.QAction(MainWindow)
        self.actionOpen_Recent.setObjectName("actionOpen_Recent")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(resource_path("Icons/write.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon5)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.actionNew.setFont(font)
        self.actionNew.setObjectName("actionNew")
        self.actionDark_Mode = QtWidgets.QAction(MainWindow)
        self.actionDark_Mode.setObjectName("actionDark_Mode")
        self.actionLight_Mode = QtWidgets.QAction(MainWindow)
        self.actionLight_Mode.setObjectName("actionLight_Mode")
        self.actionJump_to = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(resource_path("Icons/clock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJump_to.setIcon(icon6)
        self.actionJump_to.setObjectName("actionJump_to")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(resource_path("Icons/turn_off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon7)
        self.actionExit.setObjectName("actionExit")
        self.actionShow_Summary_Table = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(resource_path("Icons/presentation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Summary_Table.setIcon(icon8)
        self.actionShow_Summary_Table.setObjectName("actionShow_Summary_Table")

        self.actionShow_Job_Table = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/checklist.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Job_Table.setIcon(icon)
        self.actionShow_Job_Table.setObjectName("actionShow_Job_Table")

        self.menuDevelopers.addAction(self.actionLyra_2)
        self.menuDevelopers.addAction(self.actionRyan_2)
        self.menuDevelopers.addAction(self.actionKent)
        self.menuDevelopers.addAction(self.actionJoshua_2)
        self.menuDevelopers.addAction(self.actionGrant)
        self.menuAbout.addAction(self.actionThis_partition)
        self.menuAbout.addAction(self.menuDevelopers.menuAction())
        self.menuHelp.addAction(self.actionHow_to_use)
        self.menuHelp.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_image)
        self.menuFile.addAction(self.actionExport_csv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionclose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAppearance_2.addAction(self.actionLight_Mode)
        self.menuAppearance_2.addAction(self.actionDark_Mode)
        self.menuAppearance.addAction(self.menuAppearance_2.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAppearance.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionJump_to)
        self.toolBar.addAction(self.actionShow_Job_Table)
        self.toolBar.addAction(self.actionShow_Summary_Table)
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")
        
        self.label_zero = QtWidgets.QLabel(self.Group_memoryMap)
        self.label_zero.setText('0')
        self.label_zero.adjustSize()
        self.label_zero.setAlignment(QtCore.Qt.AlignRight)
        self.label_zero.setGeometry(QtCore.QRect(0, 30, 43, 13))
        self.label_zero.setObjectName("label_zero")

        self.label_memory_size = QtWidgets.QLabel(self.Group_memoryMap)
        Memory_size = self.inputs['Memory size']
        self.label_memory_size.setText(f'{Memory_size}')
        self.label_memory_size.adjustSize()
        self.label_memory_size.setAlignment(QtCore.Qt.AlignRight)
        self.label_memory_size.setGeometry(QtCore.QRect(0, self.V_END+30, 43, 13))
        self.label_memory_size.setObjectName("label_memory_size")

        self.v_line = QtWidgets.QFrame(self.Group_memoryMap)
        self.v_line.setGeometry(QtCore.QRect(40, 40, 20, self.V_END))
        self.v_line.setLineWidth(2)
        self.v_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.v_line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.v_line.setObjectName("v_line")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.make_lines(len(self.mem_map[self.idx]))
        self.make_labels(len(self.mem_map[self.idx]))
        self.make_memory_labels(self.mem_map[self.idx], self.fixed)
        self.button_state()
        self.show_FAT(self.idx)
        self.show_PAT(self.idx)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dynamic Partition"))
        self.Group_memoryMap.setTitle(_translate("MainWindow", "Memory Map"))
        self.Group_FAT_table.setTitle(_translate("MainWindow", "Free Allocation Table"))
        item = self.FAT_Table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "FA#"))
        item = self.FAT_Table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Size"))
        item = self.FAT_Table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Location"))
        item = self.FAT_Table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        self.Group_pat_table.setTitle(_translate("MainWindow", "Partition Allocation Table"))
        item = self.PAT_Table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Partition"))
        item = self.PAT_Table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Size"))
        item = self.PAT_Table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Location"))
        item = self.PAT_Table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        
        self.Group_osSize.setTitle(_translate("MainWindow", "OS Size"))
        self.OS_size_label.setText(_translate("MainWindow", f"{self.inputs['OS size']}"))
        self.Group_memSize.setTitle(_translate("MainWindow", "Memory Size"))
        self.mem_size_label.setText(_translate("MainWindow", f"{self.inputs['Memory size']}"))
        self.partition_title.setText(_translate("MainWindow", "Dynamic Partition Memory Management"))
        self.prev_button.setText(_translate("MainWindow", "Prev"))
        self.next_button.setText(_translate("MainWindow", "Next"))
        self.simplify_cbx.setText(_translate("MainWindow", "Simplify"))
        self.message_label.setText(_translate("MainWindow", f"{self.message[0]}"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuDevelopers.setTitle(_translate("MainWindow", "Developers"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAppearance.setTitle(_translate("MainWindow", "View"))
        self.menuAppearance_2.setTitle(_translate("MainWindow", "Theme"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Tool Bar"))
        self.actionHome.setText(_translate("MainWindow", "Home"))
        self.actionShow_Job_Table.setText(_translate("MainWindow", "Entries"))
        self.actionLyra.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua.setText(_translate("MainWindow", "Joshua"))
        self.actionLyra_2.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan_2.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua_2.setText(_translate("MainWindow", "Joshua"))
        self.actionKent.setText(_translate("MainWindow", "Kent"))
        self.actionGrant.setText(_translate("MainWindow", "Grant"))
        self.actionThis_partition.setText(_translate("MainWindow", "This partition"))
        self.actionHow_to_use.setText(_translate("MainWindow", "How to use"))
        self.actionCSV.setText(_translate("MainWindow", "CSV"))
        self.actionPNG.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG.setText(_translate("MainWindow", "JPEG"))
        self.actionCSV_2.setText(_translate("MainWindow", "CSV"))
        self.actionPNG_2.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG_2.setText(_translate("MainWindow", "JPEG"))
        self.actionJPEG_3.setText(_translate("MainWindow", "JPEG"))
        self.actionSave_image.setText(_translate("MainWindow", "Save Image"))
        self.actionclose.setText(_translate("MainWindow", "Close"))
        self.actionExport_csv.setText(_translate("MainWindow", "Export (.csv)"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen_Recent.setText(_translate("MainWindow", "Open Recent"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionDark_Mode.setText(_translate("MainWindow", "Dark"))
        self.actionLight_Mode.setText(_translate("MainWindow", "Light"))
        self.actionJump_to.setText(_translate("MainWindow", "Jump to"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionShow_Summary_Table.setText(_translate("MainWindow", "Summary"))
        self.next_button.clicked.connect(self.next_clicked)
        self.prev_button.clicked.connect(self.prev_clicked)
        self.actionJump_to.triggered.connect(self.jump_to)
        self.actionShow_Summary_Table.triggered.connect(self.show_summary_table)
        self.actionShow_Job_Table.triggered.connect(self.show_job_entries)
        self.actionLight_Mode.triggered.connect(self.light_theme)
        self.actionDark_Mode.triggered.connect(self.dark_theme)
        self.simplify_cbx.stateChanged.connect(self.simplify_mem_map)
        self.actionNew.triggered.connect(self.new_input)
        self.actionExit.triggered.connect(self.quitting)

        self.actionSave_image.triggered.connect(self.message_to_user)
        self.actionExport_csv.triggered.connect(self.message_to_user)
        self.actionOpen.triggered.connect(self.message_to_user)
        self.actionHow_to_use.triggered.connect(self.message_to_user)
        self.actionThis_partition.triggered.connect(self.message_to_user)

        self.actionclose.triggered.connect(self.closing)
        self.actionHome.triggered.connect(self.goto_home)

    def goto_home(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def message_to_user(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setText("Sorry not available right now, we're still working on this.      ")
        info.setWindowTitle("Info")
        info.exec_()

    def closing(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('This will bring you to the home window, continue?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.goto_home()
            
    def quitting(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to quit?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            sys.exit()
    def dark_theme(self):
        # Palette to switch to dark colors:
        # app.setStyle("Fusion")
        global dark
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette().Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette().AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette().ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette().Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)
        self.PAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #2A74BB;}')
        self.FAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")
        self.dark_theme_enabled = True
        dark = True
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
    
    def light_theme(self):
        global dark
        palette = QtGui.QPalette()
        app.setPalette(palette)
        self.PAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #2A74BB;}')
        self.FAT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")
        self.dark_theme_enabled = False
        dark = False
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
        
    def show_FAT(self, idx):
        Fnum = self.f_list[idx]['FA#']
        Fs = self.f_list[idx]['S']
        Floc = self.f_list[idx]['Loc']
        Fstatus = self.f_list[idx]['Status']
        
        self.FAT_Table.clearContents()
        try:
            if max(Fnum) > 5:
                self.FAT_Table.setRowCount(max(Fnum))
            else:
                self.FAT_Table.setRowCount(5)
        except TypeError:
            self.FAT_Table.setRowCount(1)

        for row in range(len(Fnum)):
            self.FAT_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(Fnum[row])))
            self.FAT_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(Fs[row])))
            self.FAT_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(Floc[row])))
            self.FAT_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(Fstatus[row])))

    def show_PAT(self, idx):
        Pnum = self.p_list[idx]['Partition']
        Ps = self.p_list[idx]['S']
        Ploc = self.p_list[idx]['Loc']
        Pstatus = self.p_list[idx]['Status']
        
        self.PAT_Table.clearContents()
        if max(Pnum) > 5:
            self.PAT_Table.setRowCount(max(Pnum))
        else:
            self.PAT_Table.setRowCount(5)
        for row in range(len(Pnum)):
            self.PAT_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(Pnum[row])))
            self.PAT_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(Ps[row])))
            self.PAT_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(Ploc[row])))
            self.PAT_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(Pstatus[row])))
    
    def show_status_column(self):
        for row in range(len(self.status_table[self.idx])):
            self.PAT_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.status_table[self.idx][row])))

    def simplify_mem_map(self):
        if self.simplify_cbx.isChecked():
            if self.fixed == False:
                self.fixed = True
        else:
            if self.fixed == True:
                self.fixed = False
        self.show_line_LOC(self.mem_map[self.idx], self.fixed)
        self.show_label_LOC(self.mem_map[self.idx], self.fixed)
        self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)

    def button_state(self):
        if self.idx == len(self.mem_map)-1:
            self.next_button.setEnabled(False)
            self.end_show = True
        else:
            self.next_button.setEnabled(True)
        
        if self.idx == 0:
            self.prev_button.setEnabled(False)
        else:
            self.prev_button.setEnabled(True)


    def new_input(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.Yes)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('New file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.new_window = MyWindow()
            self.activate_window = DP_InputWindow(self.new_window)
            self.new_window.show()
            self.MainWindow.hide()

    def next_clicked(self):
        try:
            self.idx += 1
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
            self.show_PAT(self.idx)
            self.show_FAT(self.idx)

        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1
        self.button_state()

    def prev_clicked(self):
        try:
            self.idx -= 1
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
            self.show_PAT(self.idx)
            self.show_FAT(self.idx)

        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1
        self.button_state()
    
    def show_error_message(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setTextFormat(QtCore.Qt.RichText)
        info.setText("Sorry, an error has occured when I begin to process your data. We're still working on this, please try another input. \
                    <a href='https://www.facebook.com/xtnctx'><br><br>Tell me about the error</br></br></a>    ")
        info.setWindowTitle("Developer message")
        info.exec_()

    # Make unique objects returning in different memory location (of Python)
    def make_lines(self, length):
        self.new_mem_map = fcn.margin_memory_loc(self.mem_map[self.idx], self.V_END, y=30, fixed=self.fixed)
        for i in range(length-1):
            self.d[f"self.horizontal_line{i}"] = QtWidgets.QFrame(self.Group_memoryMap)
            self.d[f"self.horizontal_line{i}"].setLineWidth(2)
            self.d[f"self.horizontal_line{i}"].setGeometry(QtCore.QRect(50, self.new_mem_map[i]+20, 251, 16))
            self.d[f"self.horizontal_line{i}"].setFrameShape(QtWidgets.QFrame.HLine)
            self.d[f"self.horizontal_line{i}"].setFrameShadow(QtWidgets.QFrame.Raised)
            self.d[f"self.horizontal_line{i}"].setObjectName("horizontal_line")
        return self.d

    def make_labels(self, length):
        self.new_mem_map = fcn.margin_memory_loc(self.mem_map[self.idx], self.V_END, y=30, fixed=self.fixed)
        for i in range(length-1):
            self.labels[f"self.pointer_label{i}"] = QtWidgets.QLabel(self.Group_memoryMap)
            self.labels[f"self.pointer_label{i}"].setText(f"{self.mem_map[self.idx][i]}")
            self.labels[f"self.pointer_label{i}"].adjustSize()
            self.labels[f"self.pointer_label{i}"].setAlignment(QtCore.Qt.AlignRight)
            self.labels[f"self.pointer_label{i}"].setGeometry(QtCore.QRect(0, self.new_mem_map[i]+20, 43, 13))
            self.labels[f"self.pointer_label{i}"].setObjectName("pointer_label")
        return self.labels
    
    def make_memory_labels(self, mem_map, fixed):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        font.setKerning(True)

        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)
        
        length = len(mem_map)
        for i in range(length):
            self.mem_labels[f"self.memory_label{i}"] = QtWidgets.QLabel(self.Group_memoryMap)
            if 'F' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #8E44AD")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #6C3483")
            elif 'wasted' in self.label[self.idx][i]:
                font.setPointSize(8)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #C64943")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #D84B4B")
            elif 'P' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #436DC6")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #3C5277")
            else:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #DBDBDB")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #4F4F4F")
            self.mem_labels[f"self.memory_label{i}"].setText(f"{self.label[self.idx][i]}")
            self.mem_labels[f"self.memory_label{i}"].adjustSize()
            self.mem_labels[f"self.memory_label{i}"].setAlignment(QtCore.Qt.AlignCenter)
            self.mem_labels[f"self.memory_label{i}"].setGeometry(QtCore.QRect(50, self.memory_label_yloc[0][i]+20, 270, 13))
            self.mem_labels[f"self.memory_label{i}"].setObjectName("memory_label")
    
    # Configure assigned variables from dictionary
    def show_line_LOC(self, mem_map, fixed):
        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        # Add missing widget
        if len(self.new_mem_map) > len(self.d)+1:
            for missing in range(len(self.d), len(self.new_mem_map)-1):
                self.d[f"self.horizontal_line{missing}"] = QtWidgets.QFrame(self.Group_memoryMap)
                self.d[f"self.horizontal_line{missing}"].setLineWidth(2)
                self.d[f"self.horizontal_line{missing}"].setGeometry(QtCore.QRect(50, self.new_mem_map[missing]+20, 251, 16))
                self.d[f"self.horizontal_line{missing}"].setFrameShape(QtWidgets.QFrame.HLine)
                self.d[f"self.horizontal_line{missing}"].setFrameShadow(QtWidgets.QFrame.Raised)
                self.d[f"self.horizontal_line{missing}"].setObjectName("horizontal_line")
        
        # Show widget
        d = dict(itertools.islice(self.d.items(), len(self.new_mem_map)-1))
        for i in range(len(d)):
            d[f"self.horizontal_line{i}"].setLineWidth(2)
            d[f"self.horizontal_line{i}"].setGeometry(QtCore.QRect(50, self.new_mem_map[i]+20, 251, 16))
            d[f"self.horizontal_line{i}"].setFrameShape(QtWidgets.QFrame.HLine)
            d[f"self.horizontal_line{i}"].setFrameShadow(QtWidgets.QFrame.Raised)
            d[f"self.horizontal_line{i}"].setObjectName("horizontal_line")
            d[f"self.horizontal_line{i}"].show()

        # Hide the excess widget
        for k in range(len(d), len(self.d)):
            self.d[f"self.horizontal_line{k}"].hide()
            # del self.d[f"self.horizontal_line{k}"]
    
    def show_label_LOC(self, mem_map, fixed):
        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        if len(self.new_mem_map) > len(self.labels)+1:
            for missing in range(len(self.labels), len(self.new_mem_map)-1):
                self.labels[f"self.pointer_label{missing}"] = QtWidgets.QLabel(self.Group_memoryMap)
                self.labels[f"self.pointer_label{missing}"].setText(f"{mem_map[missing]}")
                self.labels[f"self.pointer_label{missing}"].adjustSize()
                self.labels[f"self.pointer_label{missing}"].setAlignment(QtCore.Qt.AlignRight)
                self.labels[f"self.pointer_label{missing}"].setGeometry(QtCore.QRect(0, self.new_mem_map[missing]+20, 43, 13))
                self.labels[f"self.pointer_label{missing}"].setObjectName("pointer_label")

        p = dict(itertools.islice(self.labels.items(), len(self.new_mem_map)-1))
        for i in range(len(p)):
            p[f"self.pointer_label{i}"].setText(f"{mem_map[i]}")
            p[f"self.pointer_label{i}"].adjustSize()
            p[f"self.pointer_label{i}"].setAlignment(QtCore.Qt.AlignRight)
            p[f"self.pointer_label{i}"].setGeometry(QtCore.QRect(0, self.new_mem_map[i]+20, 43, 13))
            p[f"self.pointer_label{i}"].setObjectName("pointer_label")
            p[f"self.pointer_label{i}"].show()
            
        for k in range(len(p), len(self.labels)):
            self.labels[f"self.pointer_label{k}"].hide()
            # del self.labels[f"self.pointer_label{k}"]
    
    def show_MMlabel_LOC(self, mem_map, fixed):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        font.setKerning(True)

        self.new_mem_map = fcn.margin_memory_loc(mem_map, self.V_END, y=30, fixed=fixed)
        self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)

        if len(self.memory_label_yloc[0]) > len(self.mem_labels):
            for missing in range(len(self.mem_labels), len(self.memory_label_yloc[0])):
                self.mem_labels[f"self.memory_label{missing}"] = QtWidgets.QLabel(self.Group_memoryMap)
                self.mem_labels[f"self.memory_label{missing}"].setText(f"{self.label[self.idx][missing]}")
                self.mem_labels[f"self.memory_label{missing}"].adjustSize()
                self.mem_labels[f"self.memory_label{missing}"].setAlignment(QtCore.Qt.AlignCenter)
                self.mem_labels[f"self.memory_label{missing}"].setGeometry(QtCore.QRect(50, 
                                self.memory_label_yloc[0][missing]+20, 270, 13))
                self.mem_labels[f"self.memory_label{missing}"].setObjectName("memory_label")
        
        elif len(self.memory_label_yloc[0]) < len(self.mem_labels):
            for k in range(len(self.memory_label_yloc[0]), len(self.mem_labels)):
                self.mem_labels[f"self.memory_label{k}"].hide()
                del self.mem_labels[f"self.memory_label{k}"]

        for i in range(len(self.mem_labels)):
            if 'F' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #8E44AD")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #6C3483")
            elif 'wasted' in self.label[self.idx][i]:
                font.setPointSize(8)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #C64943")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #823D3D")
            elif 'P' in self.label[self.idx][i]:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #436DC6")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #3C5277")
            else:
                font.setPointSize(10)
                if self.dark_theme_enabled:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #DBDBDB")
                else:
                    self.mem_labels[f"self.memory_label{i}"].setFont(font)
                    self.mem_labels[f"self.memory_label{i}"].setStyleSheet("color: #4F4F4F")
            self.mem_labels[f"self.memory_label{i}"].setText(f"{self.label[self.idx][i]}")
            self.mem_labels[f"self.memory_label{i}"].adjustSize()
            self.mem_labels[f"self.memory_label{i}"].setGeometry(QtCore.QRect(50, self.memory_label_yloc[0][i]+20, 270, 13))
            self.mem_labels[f"self.memory_label{i}"].setAlignment(QtCore.Qt.AlignCenter)
            self.mem_labels[f"self.memory_label{i}"].setObjectName("memory_label")
            self.mem_labels[f"self.memory_label{i}"].show()
    
    def show_job_entries(self):
        self.job_window = QtWidgets.QMainWindow()
        self.job_ui = JobTableWindow(self.job_window)
        self.job_window.show()

    
    def show_summary_table(self):
        self.second_ui = SummaryTableWindow([self.start_time, self.finish, self.cpu_wait])
    
    def jump_to(self):
        self.timelist_window = QtWidgets.QMainWindow()
        self.timelist_ui = Partition_TimeList(self.timelist_window)
        self.timelist_ui.pushButton.clicked.connect(self.go_)
        self.timelist_window.show()
    
    def go_(self):
        if not self.idx == self.timelist_ui.comboBox.currentIndex():
            self.idx = self.timelist_ui.comboBox.currentIndex()
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

            self.show_line_LOC(self.mem_map[self.idx], self.fixed)
            self.show_label_LOC(self.mem_map[self.idx], self.fixed)
            self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
            self.show_PAT(self.idx)
            self.show_FAT(self.idx)
            self.button_state()

class Partition_TimeList:
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Time List")
        MainWindow.setFixedSize(251, 170)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("Icons/clock.png")))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(resource_path("Icons/clock-history.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(91, 111, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow-skip.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(True)
        # self.pushButton.clicked.connect(self.change_txt)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        c = []
        T = X[5] + X[6]
        T = fcn.sort_time(T)
        self.comboBox.addItem(self.icon, f'Before {T[0]}')
        for time in T:
            if time in c:
                self.comboBox.addItem(self.icon, f'{time} ↰')
            elif time == T[-1]:
                self.comboBox.addItem(self.icon, f'{time} (Finished)')
            else:
                self.comboBox.addItem(self.icon, time)
            c.append(time)


# Process Management
class PM_InputWindow:
    def __init__(self, MainWindow):
        self.process_entries = {}
        self.burst_entries = {}
        self.arrival_entries = {}
        self.priority_entries = {}
        self.csv_loaded_successful = False
        self.priority_isActive = False
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 655)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_entries = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_entries.setGeometry(QtCore.QRect(330, 124, 571, 437))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.Group_entries.setFont(font)
        self.Group_entries.setObjectName("Group_entries")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Group_entries)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.colum_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.colum_name_horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.colum_name_horizontalLayout.setSpacing(0)
        self.colum_name_horizontalLayout.setObjectName("colum_name_horizontalLayout")
        self.process_label = QtWidgets.QLabel(self.Group_entries)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.process_label.sizePolicy().hasHeightForWidth())
        self.process_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.process_label.setFont(font)
        self.process_label.setAlignment(QtCore.Qt.AlignCenter)
        self.process_label.setObjectName("process_label")
        self.colum_name_horizontalLayout.addWidget(self.process_label)
        self.burst_label = QtWidgets.QLabel(self.Group_entries)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.burst_label.sizePolicy().hasHeightForWidth())
        self.burst_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.burst_label.setFont(font)
        self.burst_label.setAlignment(QtCore.Qt.AlignCenter)
        self.burst_label.setObjectName("burst_label")
        self.colum_name_horizontalLayout.addWidget(self.burst_label)
        self.arrival_label = QtWidgets.QLabel(self.Group_entries)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_label.sizePolicy().hasHeightForWidth())
        self.arrival_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.arrival_label.setFont(font)
        self.arrival_label.setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_label.setObjectName("arrival_label")
        self.colum_name_horizontalLayout.addWidget(self.arrival_label)
        self.verticalLayout.addLayout(self.colum_name_horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.Group_entries)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMouseTracking(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(2)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 528, 69))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(30, 20, 10, 20)
        self.gridLayout.setHorizontalSpacing(40)
        self.gridLayout.setVerticalSpacing(27)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.import_horizontalLayout = QtWidgets.QHBoxLayout()
        self.import_horizontalLayout.setContentsMargins(-1, -1, 150, -1)
        self.import_horizontalLayout.setObjectName("import_horizontalLayout")
        self.import_csv_btn = QtWidgets.QPushButton(self.Group_entries)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{process number, burst time*, arrival time*}')
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.import_horizontalLayout.addWidget(self.import_csv_btn)
        self.gridLayout_2.addLayout(self.import_horizontalLayout, 1, 0, 1, 1)
        self.add_rmv_horizontalLayout = QtWidgets.QHBoxLayout()
        self.add_rmv_horizontalLayout.setContentsMargins(100, -1, -1, -1)
        self.add_rmv_horizontalLayout.setSpacing(30)
        self.add_rmv_horizontalLayout.setObjectName("add_rmv_horizontalLayout")
        self.rmv_entry_btn = QtWidgets.QPushButton(self.Group_entries)
        self.rmv_entry_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rmv_entry_btn.setIcon(icon1)
        self.rmv_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.rmv_entry_btn.setCheckable(False)
        self.rmv_entry_btn.setDefault(False)
        self.rmv_entry_btn.setFlat(True)
        self.rmv_entry_btn.setObjectName("rmv_entry_btn")
        self.add_rmv_horizontalLayout.addWidget(self.rmv_entry_btn)
        self.add_entry_btn = QtWidgets.QPushButton(self.Group_entries)
        self.add_entry_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/plus-black-symbol.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_entry_btn.setIcon(icon2)
        self.add_entry_btn.setIconSize(QtCore.QSize(20, 20))
        self.add_entry_btn.setCheckable(False)
        self.add_entry_btn.setDefault(False)
        self.add_entry_btn.setFlat(True)
        self.add_entry_btn.setObjectName("add_entry_btn")
        self.add_rmv_horizontalLayout.addWidget(self.add_entry_btn)
        self.gridLayout_2.addLayout(self.add_rmv_horizontalLayout, 1, 1, 1, 1)
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(800, 620, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_btn.setIcon(icon3)
        self.start_btn.setIconSize(QtCore.QSize(20, 20))
        self.start_btn.setCheckable(False)
        self.start_btn.setAutoDefault(False)
        self.start_btn.setDefault(False)
        self.start_btn.setFlat(True)
        self.start_btn.setObjectName("start_btn")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(-10, 620, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.back_btn.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow_left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_btn.setIcon(icon4)
        self.back_btn.setIconSize(QtCore.QSize(20, 20))
        self.back_btn.setCheckable(False)
        self.back_btn.setAutoDefault(False)
        self.back_btn.setDefault(False)
        self.back_btn.setFlat(True)
        self.back_btn.setObjectName("back_btn")

        self.ev_line = QtWidgets.QFrame(self.centralwidget)
        self.ev_line.setGeometry(QtCore.QRect(333, 164, 21, 41))
        self.ev_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ev_line.setLineWidth(2)
        self.ev_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.ev_line.setObjectName("ev_line")

        self.ev_line2 = QtWidgets.QFrame(self.centralwidget)
        self.ev_line2.setGeometry(QtCore.QRect(878, 164, 21, 41))
        self.ev_line2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ev_line2.setLineWidth(2)
        self.ev_line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.ev_line2.setObjectName("ev_line2")

        self.eh_line = QtWidgets.QFrame(self.centralwidget)
        self.eh_line.setGeometry(QtCore.QRect(343, 155, 545, 20))
        self.eh_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.eh_line.setLineWidth(2)
        self.eh_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.eh_line.setObjectName("eh_line")
        self.Group_processManagement = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_processManagement.setGeometry(QtCore.QRect(20, 50, 291, 511))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Group_processManagement.setFont(font)
        self.Group_processManagement.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_processManagement.setFlat(False)
        self.Group_processManagement.setCheckable(False)
        self.Group_processManagement.setObjectName("Group_processManagement")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Group_processManagement)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.processScrollArea = QtWidgets.QScrollArea(self.Group_processManagement)
        self.processScrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.processScrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.processScrollArea.setLineWidth(2)
        self.processScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.processScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.processScrollArea.setWidgetResizable(True)
        self.processScrollArea.setObjectName("processScrollArea")
        self.process_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.process_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 267, 445))
        self.process_scrollAreaWidgetContents.setObjectName("process_scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.process_scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.priority_radioBtn = QtWidgets.QRadioButton(self.process_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.priority_radioBtn.setFont(font)
        self.priority_radioBtn.setObjectName("priority_radioBtn")
        self.gridLayout_3.addWidget(self.priority_radioBtn, 2, 0, 1, 1)
        self.srt_radioBtn = QtWidgets.QRadioButton(self.process_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.srt_radioBtn.setFont(font)
        self.srt_radioBtn.setObjectName("srt_radioBtn")
        self.gridLayout_3.addWidget(self.srt_radioBtn, 3, 0, 1, 1)
        self.fcfs_radioBtn = QtWidgets.QRadioButton(self.process_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.fcfs_radioBtn.setFont(font)
        self.fcfs_radioBtn.setChecked(True)
        self.fcfs_radioBtn.setObjectName("fcfs_radioBtn")
        self.gridLayout_3.addWidget(self.fcfs_radioBtn, 0, 0, 1, 1)
        self.sjf_radioBtn = QtWidgets.QRadioButton(self.process_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.sjf_radioBtn.setFont(font)
        self.sjf_radioBtn.setChecked(False)
        self.sjf_radioBtn.setObjectName("sjf_radioBtn")
        self.gridLayout_3.addWidget(self.sjf_radioBtn, 1, 0, 1, 1)
        self.rr_radioBtn = QtWidgets.QRadioButton(self.process_scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.rr_radioBtn.setFont(font)
        self.rr_radioBtn.setObjectName("rr_radioBtn")
        self.gridLayout_3.addWidget(self.rr_radioBtn, 4, 0, 1, 1)
        self.processScrollArea.setWidget(self.process_scrollAreaWidgetContents)
        self.gridLayout_4.addWidget(self.processScrollArea, 0, 0, 1, 1)
        
        self.Group_entries.raise_()
        self.start_btn.raise_()
        self.back_btn.raise_()
        self.eh_line.raise_()
        self.ev_line.raise_()
        self.Group_processManagement.raise_()
        MainWindow.setCentralWidget(self.centralwidget)


        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(60)
        font.setKerning(True)

        self.preemptive_cbx = QtWidgets.QCheckBox(self.centralwidget)
        self.preemptive_cbx.setGeometry(QtCore.QRect(185, 315, 100, 19))
        self.preemptive_cbx.setFont(font)
        self.preemptive_cbx.setText('Preemptive')
        self.preemptive_cbx.setStyleSheet("QCheckBox::indicator" "{" "width :15;" "height : 15;""}")
        self.preemptive_cbx.setObjectName("preemptive_cbx")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.make_default_entry(default_entry)
        self.fcfs_radioBtn_isChecked()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Process Management"))
        self.Group_entries.setTitle(_translate("MainWindow", "Entries"))
        self.process_label.setText(_translate("MainWindow", "Process"))
        self.burst_label.setText(_translate("MainWindow", "Burst Time"))
        self.arrival_label.setText(_translate("MainWindow", "Arrival Time"))
        self.import_csv_btn.setText(_translate("MainWindow", "  Import CSV"))
        self.start_btn.setText(_translate("MainWindow", "  Start"))
        self.back_btn.setText(_translate("MainWindow", "  Back"))
        self.Group_processManagement.setTitle(_translate("MainWindow", "Process Management"))
        self.priority_radioBtn.setText(_translate("MainWindow", "Priority    <-->"))
        self.srt_radioBtn.setText(_translate("MainWindow", "Shortest Remaining Time"))
        self.fcfs_radioBtn.setText(_translate("MainWindow", "First Come First Serve"))
        self.sjf_radioBtn.setText(_translate("MainWindow", "Shortest Job First"))
        self.rr_radioBtn.setText(_translate("MainWindow", "Round Robin"))
        self.start_btn.clicked.connect(self.start)
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.add_entry_btn.clicked.connect(self.add_entry)
        self.rmv_entry_btn.clicked.connect(self.remove_entry)
        self.fcfs_radioBtn.clicked.connect(self.fcfs_radioBtn_isChecked)
        self.sjf_radioBtn.clicked.connect(self.sjf_radioBtn_isChecked)
        self.priority_radioBtn.clicked.connect(self.priority_radioBtn_isChecked)
        self.srt_radioBtn.clicked.connect(self.srt_radioBtn_isChecked)
        self.rr_radioBtn.clicked.connect(self.rr_radioBtn_isChecked)
    
        self.back_btn.clicked.connect(self.back_to_start_up)

    def back_to_start_up(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def message_to_user(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setText("Sorry not available right now, we're still working on this.      ")
        info.setWindowTitle("Info")
        info.exec_()

    def make_default_entry(self, default_entry):
        for _ in range(default_entry):
            self.add_entry()

    def add_entry(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Process No.
        self.process_entries[f"process{len(self.process_entries)+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.process_entries[f"process{len(self.process_entries)}"].setText(f"P{len(self.process_entries)}")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.process_entries[f"process{len(self.process_entries)}"].sizePolicy().hasHeightForWidth())
        self.process_entries[f"process{len(self.process_entries)}"].setSizePolicy(sizePolicy)
        self.process_entries[f"process{len(self.process_entries)}"].setFont(font)
        self.process_entries[f"process{len(self.process_entries)}"].setScaledContents(False)
        self.process_entries[f"process{len(self.process_entries)}"].setAlignment(QtCore.Qt.AlignCenter)
        self.process_entries[f"process{len(self.process_entries)}"].setObjectName(f"process{len(self.process_entries)}")
        self.gridLayout.addWidget(self.process_entries[f"process{len(self.process_entries)}"], len(self.process_entries), 0, 1, 1)
        
    #Burst
        self.burst_entries[f'burst{len(self.burst_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.burst_entries[f'burst{len(self.burst_entries)}'].sizePolicy().hasHeightForWidth())
        self.burst_entries[f'burst{len(self.burst_entries)}'].setSizePolicy(sizePolicy)
        self.burst_entries[f'burst{len(self.burst_entries)}'].setFont(font)
        self.burst_entries[f'burst{len(self.burst_entries)}'].setMinimum(0)
        self.burst_entries[f'burst{len(self.burst_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.burst_entries[f'burst{len(self.burst_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.burst_entries[f'burst{len(self.burst_entries)}'].setMaximum(999999999)
        self.burst_entries[f'burst{len(self.burst_entries)}'].setSingleStep(5)
        self.burst_entries[f'burst{len(self.burst_entries)}'].setProperty("value", 0)
        self.burst_entries[f'burst{len(self.burst_entries)}'].setObjectName(f'burst{len(self.burst_entries)}')
        self.gridLayout.addWidget(self.burst_entries[f'burst{len(self.burst_entries)}'], len(self.burst_entries), 1, 1, 1)

    #Arrival
        self.arrival_entries[f'arrival{len(self.arrival_entries)+1}'] = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{len(self.arrival_entries)}'].sizePolicy().hasHeightForWidth())
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setSizePolicy(sizePolicy)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setFont(font)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setMinimum(0)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setAlignment(QtCore.Qt.AlignCenter)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setMaximum(999999999)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setSingleStep(5)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setProperty("value", 0)
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].setObjectName(f'arrival{len(self.arrival_entries)}')
        self.gridLayout.addWidget(self.arrival_entries[f'arrival{len(self.arrival_entries)}'], len(self.arrival_entries), 2, 1, 1)

    #Priority
        
        if self.priority_isActive:
            self.priority_entries[f'priority_num{len(self.priority_entries)+1}'] = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.priority_entries[f'priority_num{len(self.priority_entries)}'].sizePolicy().hasHeightForWidth())
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].setSizePolicy(sizePolicy)
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].setFont(font)
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].setEditable(True)
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].setDuplicatesEnabled(False)
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].setObjectName("priority_comboBox")
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].addItem("--")
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].lineEdit().setAlignment(QtCore.Qt.AlignCenter)
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].lineEdit().setReadOnly(True)
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].currentTextChanged.connect(self.on_combobox_changed)
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].addItems([str(i+1) for i in list(range(len(self.priority_entries)))])
            self.gridLayout.addWidget(self.priority_entries[f'priority_num{len(self.priority_entries)}'], len(self.priority_entries), 3, 1, 1)
            All_Items = [self.priority_entries[f'priority_num{len(self.priority_entries)}'].itemText(i) for i in range(self.priority_entries[f'priority_num{len(self.priority_entries)}'].count())]
            print(All_Items, 'sddsdsds')
        
        items = [str(i+1) for i in list(range(len(self.priority_entries)))]
        for i in range(len(self.priority_entries)-1):
            self.priority_entries[f'priority_num{i+1}'].addItem(items[-1])
            
        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()
    
    def remove_entry(self):
        self.process_entries[f"process{len(self.process_entries)}"].hide()
        self.burst_entries[f'burst{len(self.burst_entries)}'].hide()
        self.arrival_entries[f'arrival{len(self.arrival_entries)}'].hide()

        del self.process_entries[f"process{len(self.process_entries)}"]
        del self.burst_entries[f'burst{len(self.burst_entries)}']
        del self.arrival_entries[f'arrival{len(self.arrival_entries)}']

        if self.priority_isActive:
            self.priority_entries[f'priority_num{len(self.priority_entries)}'].hide()
            del self.priority_entries[f'priority_num{len(self.priority_entries)}']
            items = [str(i+1) for i in list(range(len(self.priority_entries)))]
            if not self.csv_loaded_successful:
                for i in range(len(self.priority_entries)):
                    self.priority_entries[f'priority_num{i+1}'].removeItem(int(items[-1])+1)

        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()

    def button_state(self):
        if self.csv_loaded_successful:
            self.add_entry_btn.setEnabled(False)
            self.rmv_entry_btn.setEnabled(False)
        else:
            if len(self.process_entries) == 1:
                self.rmv_entry_btn.setEnabled(False)
            else:
                self.rmv_entry_btn.setEnabled(True)
            self.add_entry_btn.setEnabled(True)

    def fcfs_radioBtn_isChecked(self):
        if self.priority_isActive:
            self.priority_num_label.hide()
            del self.priority_num_label

        for i in range(len(self.priority_entries)):
            self.priority_entries[f'priority_num{i+1}'].hide()
            del self.priority_entries[f'priority_num{i+1}']

        self.rr_radioBtn.setText('Round Robin')
        self.priority_radioBtn.setText('Priority')
        self.preemptive_cbx.hide()
        self.priority_isActive = False
        print('Priority is not checked.')

    def sjf_radioBtn_isChecked(self):
        if self.priority_isActive:
            self.priority_num_label.hide()
            del self.priority_num_label

        for i in range(len(self.priority_entries)):
            self.priority_entries[f'priority_num{i+1}'].hide()
            del self.priority_entries[f'priority_num{i+1}']
        
        self.rr_radioBtn.setText('Round Robin')
        self.priority_radioBtn.setText('Priority')
        self.preemptive_cbx.hide()

        self.priority_isActive = False
        print('Priority is not checked.')

    def srt_radioBtn_isChecked(self):
        if self.priority_isActive:
            self.priority_num_label.hide()
            del self.priority_num_label

        for i in range(len(self.priority_entries)):
            self.priority_entries[f'priority_num{i+1}'].hide()
            del self.priority_entries[f'priority_num{i+1}']

        self.rr_radioBtn.setText('Round Robin')
        self.priority_radioBtn.setText('Priority')
        self.preemptive_cbx.hide()
        self.priority_isActive = False
        print('Priority is not checked.')

    def rr_radioBtn_isChecked(self):
        if self.priority_isActive:
            self.priority_num_label.hide()
            del self.priority_num_label

        for i in range(len(self.priority_entries)):
            self.priority_entries[f'priority_num{i+1}'].hide()
            del self.priority_entries[f'priority_num{i+1}']

        self.rr_radioBtn.setText('Round Robin (q = 5)')
        self.priority_radioBtn.setText('Priority')
        self.preemptive_cbx.hide()
        self.priority_isActive = False
        print('Priority is not checked.')

    def priority_radioBtn_isChecked(self):
        print('Priority is checked.')
        if self.priority_isActive == False:
            self.rr_radioBtn.setText('Round Robin')
            self.priority_radioBtn.setText('Priority    <-->')
            self.preemptive_cbx.show()
            
            self.priority_num_label = QtWidgets.QLabel(self.centralwidget)
            self.priority_num_label.setGeometry(QtCore.QRect(700, 50, 132, 19))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.priority_num_label.sizePolicy().hasHeightForWidth())
            self.priority_num_label.setSizePolicy(sizePolicy)
            font = QtGui.QFont()
            font.setFamily("Poppins")
            font.setPointSize(8)
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(75)
            font.setKerning(True)
            self.priority_num_label.setFont(font)
            self.priority_num_label.setText('Priority No.')
            self.priority_num_label.setAlignment(QtCore.Qt.AlignCenter)
            self.priority_num_label.setObjectName("priority_num_label")
            self.colum_name_horizontalLayout.addWidget(self.priority_num_label)
            self.priority_isActive = True

            for _ in range(len(self.priority_entries), len(self.process_entries)):
                font = QtGui.QFont()
                font.setFamily("Poppins")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                font.setKerning(True)
                self.priority_entries[f'priority_num{len(self.priority_entries)+1}'] = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.priority_entries[f'priority_num{len(self.priority_entries)}'].sizePolicy().hasHeightForWidth())
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].setSizePolicy(sizePolicy)
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].setFont(font)
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].setEditable(True)
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].setDuplicatesEnabled(False)
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].setObjectName("priority_comboBox")
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].addItem("--")
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].lineEdit().setAlignment(QtCore.Qt.AlignCenter)
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].lineEdit().setReadOnly(True)
                self.priority_entries[f'priority_num{len(self.priority_entries)}'].currentTextChanged.connect(self.on_combobox_changed)
                self.gridLayout.addWidget(self.priority_entries[f'priority_num{len(self.priority_entries)}'], len(self.priority_entries), 3, 1, 1)
            
            items = [str(i+1) for i in list(range(len(self.priority_entries)))]
            for i in range(len(self.priority_entries)):
                self.priority_entries[f'priority_num{i+1}'].addItems(items)
                        
        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.button_state()

    def make_import_btn(self):
        self.import_csv_btn = QtWidgets.QPushButton(self.Group_entries)
        self.import_csv_btn.setGeometry(QtCore.QRect(270, 535, 100, 20))
        self.import_csv_btn.setText("  Import CSV")
        self.import_csv_btn.setToolTip('Must have this order in your file:\n{process number, burst time*, arrival time*}')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_csv_btn.sizePolicy().hasHeightForWidth())
        self.import_csv_btn.setSizePolicy(sizePolicy)
        self.import_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.import_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.import_horizontalLayout.addWidget(self.import_csv_btn)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)
        self.import_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/table_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_csv_btn.setIcon(icon2)
        self.import_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.import_csv_btn.setCheckable(False)
        self.import_csv_btn.setDefault(False)
        self.import_csv_btn.setFlat(True)
        self.import_csv_btn.setObjectName("import_csv_btn")
        self.import_csv_btn.clicked.connect(self.import_csv)
        self.import_csv_btn.show()
    
    def make_cancel_csv_btn(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(65)
        font.setKerning(True)

        self.cancel_csv_btn = QtWidgets.QPushButton(self.Group_entries)
        self.cancel_csv_btn.setGeometry(QtCore.QRect(270, 528, 32, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_csv_btn.sizePolicy().hasHeightForWidth())
        self.cancel_csv_btn.setSizePolicy(sizePolicy)
        self.cancel_csv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel_csv_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.import_horizontalLayout.addWidget(self.cancel_csv_btn)
        
        self.cancel_csv_btn.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon_red.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_csv_btn.setIcon(icon2)
        self.cancel_csv_btn.setIconSize(QtCore.QSize(15, 15))
        self.cancel_csv_btn.setCheckable(False)
        self.cancel_csv_btn.setDefault(False)
        self.cancel_csv_btn.setFlat(True)
        self.cancel_csv_btn.setObjectName("cancel_csv_btn")
        self.cancel_csv_btn.clicked.connect(self.cancel_csv)

        self.file_name_label = QtWidgets.QLabel(self.Group_entries)
        self.file_name_label.setFont(font)
        self.file_name_label.setObjectName('file_name_label')
        self.file_name_label.setGeometry(QtCore.QRect(302, 535, 100, 20))
        self.file_name_label.setText(self.active_file)
        self.file_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_name_label.adjustSize()
        self.import_horizontalLayout.addWidget(self.file_name_label)
    
    def cancel_csv(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to remove this file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            print('Yes  ')
            self.cancel_csv_btn.hide()
            self.file_name_label.hide()
            del self.cancel_csv_btn
            del self.file_name_label

            for _ in range(len(self.process_entries)):
                self.remove_entry()
            self.make_default_entry(default_entry)

            self.make_import_btn()

            self.add_entry_btn.setEnabled(True)
            self.rmv_entry_btn.setEnabled(True)
            
            # QtWidgets.QSpinBox().clear
            self.csv_loaded_successful = False
    
    def getFileDir(self):
        file_filter = '*.csv'
        response = QtWidgets.QFileDialog.getOpenFileNames(
            parent = QtWidgets.QWidget(),
            caption='Select a csv file',
            directory = os.getcwd(),
            filter=file_filter
        )
        self.active_file = response[0][0].split('/')[-1]
        return response[0][0]

    def import_csv(self):
        try:
            fileDir = self.getFileDir()
            csv = pd.read_csv(fileDir)
            column_name = list(csv.columns)
            process = csv[column_name[0]].tolist()
            burst_time = csv[column_name[1]].tolist()
            arrival_time = csv[column_name[2]].tolist()
            if self.priority_isActive:
                priority = csv[column_name[3]].tolist()
            

            for _ in range(len(self.process_entries)):
                self.remove_entry()
            self.import_csv_btn.hide()
            del self.import_csv_btn
            self.make_cancel_csv_btn()

            if self.priority_isActive:
                
                self.load_csv_to_window(process, burst_time, arrival_time, priority)
                print('this loaded')
            else:
                self.load_csv_to_window(process, burst_time, arrival_time, None)
                print('this loadedxxx')

        except IndexError:
            if self.priority_isActive:
                print('You need assign priority number to your file')
            else:
                print('No file selected')

    def load_csv_to_window(self, p, b, a, priority):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
    #Process No.
        for i in range(len(a)):
            self.process_entries[f"process{i+1}"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.process_entries[f"process{i+1}"].setText(f"P{i+1}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.process_entries[f"process{i+1}"].sizePolicy().hasHeightForWidth())
            self.process_entries[f"process{i+1}"].setSizePolicy(sizePolicy)
            self.process_entries[f"process{i+1}"].setFont(font)
            self.process_entries[f"process{i+1}"].setScaledContents(False)
            self.process_entries[f"process{i+1}"].setAlignment(QtCore.Qt.AlignCenter)
            self.process_entries[f"process{i+1}"].setObjectName(f"process{i+1}")
            self.gridLayout.addWidget(self.process_entries[f"process{i+1}"], i+1, 0, 1, 1)
    #Burst time
        for i in range(len(a)):
            self.burst_entries[f'burst{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.burst_entries[f'burst{i+1}'].setText(f"{b[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.burst_entries[f'burst{i+1}'].sizePolicy().hasHeightForWidth())
            self.burst_entries[f'burst{i+1}'].setSizePolicy(sizePolicy)
            self.burst_entries[f'burst{i+1}'].setFont(font)
            self.burst_entries[f'burst{i+1}'].setScaledContents(False)
            self.burst_entries[f'burst{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.burst_entries[f'burst{i+1}'].setObjectName(f"burst{i+1}")
            self.gridLayout.addWidget(self.burst_entries[f'burst{i+1}'], i+1, 1, 1, 1)
    #Arrival
        for i in range(len(a)):
            self.arrival_entries[f'arrival{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.arrival_entries[f'arrival{i+1}'].setText(f"{a[i]}")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.arrival_entries[f'arrival{i+1}'].sizePolicy().hasHeightForWidth())
            self.arrival_entries[f'arrival{i+1}'].setSizePolicy(sizePolicy)
            self.arrival_entries[f'arrival{i+1}'].setFont(font)
            self.arrival_entries[f'arrival{i+1}'].setScaledContents(False)
            self.arrival_entries[f'arrival{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
            self.arrival_entries[f'arrival{i+1}'].setObjectName(f"arrival{i+1}")
            self.gridLayout.addWidget(self.arrival_entries[f'arrival{i+1}'], i+1, 2, 1, 1)
    
    #Priority No.
        if self.priority_isActive:
            for i in range(len(a)):
                self.priority_entries[f'priority_num{i+1}'] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                self.priority_entries[f'priority_num{i+1}'].setText(f"{priority[i]}")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.priority_entries[f'priority_num{i+1}'].sizePolicy().hasHeightForWidth())
                self.priority_entries[f'priority_num{i+1}'].setSizePolicy(sizePolicy)
                self.priority_entries[f'priority_num{i+1}'].setFont(font)
                self.priority_entries[f'priority_num{i+1}'].setScaledContents(False)
                self.priority_entries[f'priority_num{i+1}'].setAlignment(QtCore.Qt.AlignCenter)
                self.priority_entries[f'priority_num{i+1}'].setObjectName(f"priority_num{i+1}")
                self.gridLayout.addWidget(self.priority_entries[f'priority_num{i+1}'], i+1, 3, 1, 1)

        self.csv_loaded_successful = True
        self.Group_entries.setEnabled(True)
        self.add_entry_btn.setEnabled(False)
        self.rmv_entry_btn.setEnabled(False)

        scroll_bar = self.scrollArea.verticalScrollBar()
        self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.minimum()))

    def on_combobox_changed(self, event):
        current_items = [i.currentText() for i in self.priority_entries.values()]
        if current_items.count(event) > 1 and event != '--':
            duplicates = [i for i, x in enumerate(current_items) if x == event]
            for i in duplicates:
                self.priority_entries[f'priority_num{i+1}'].setCurrentText('--')
                break
    
    def start(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setIcon(QtWidgets.QMessageBox.Information)
        notify_user.setFont(font)

        err_msg = QtWidgets.QMessageBox()
        err_msg.setIcon(QtWidgets.QMessageBox.Information)
        err_msg.setFont(font)

        self.validated = True
        for i in range(len(self.process_entries)):
            if type(self.burst_entries['burst1']).__name__ == 'QLabel':
                if list(self.burst_entries.values())[i].text() == 0:
                    self.validated = False
                    err_msg.setText('Burst time must be greater than 0      ')
                    err_msg.setWindowTitle("Entry Error")
                    err_msg.exec_()
                    list(self.burst_entries.values())[i].setFocus()
                    list(self.burst_entries.values())[i].selectAll()
                    yloc = list(self.burst_entries.values())[i].y() - list(self.burst_entries.values())[i].height()
                    self.scrollArea.verticalScrollBar().setValue(yloc)
                    break
            else:
                if list(self.burst_entries.values())[i].value() == 0:
                    self.validated = False
                    err_msg.setText('Burst time must be greater than 0      ')
                    err_msg.setWindowTitle("Entry Error")
                    err_msg.exec_()
                    list(self.burst_entries.values())[i].setFocus()
                    list(self.burst_entries.values())[i].selectAll()
                    yloc = list(self.burst_entries.values())[i].y() - list(self.burst_entries.values())[i].height()
                    self.scrollArea.verticalScrollBar().setValue(yloc)
                    break

            if self.priority_isActive:
                if type(self.priority_entries['priority_num1']).__name__ == 'QLabel': 
                    if list(self.priority_entries.values())[i].text() == '--' or list(self.priority_entries.values())[i].text() == '':
                        self.validated = False
                        err_msg.setText('Please select a priority number to this process      ')
                        err_msg.setWindowTitle("Entry Error")
                        err_msg.exec_()
                        list(self.priority_entries.values())[i].setFocus()
                        list(self.priority_entries.values())[i].lineEdit().selectAll()
                        yloc = list(self.priority_entries.values())[i].y() - list(self.priority_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
                else:
                    if list(self.priority_entries.values())[i].currentText() == '--':
                        self.validated = False
                        err_msg.setText('Please select a priority number to this process      ')
                        err_msg.setWindowTitle("Entry Error")
                        err_msg.exec_()
                        list(self.priority_entries.values())[i].setFocus()
                        list(self.priority_entries.values())[i].lineEdit().selectAll()
                        yloc = list(self.priority_entries.values())[i].y() - list(self.priority_entries.values())[i].height()
                        self.scrollArea.verticalScrollBar().setValue(yloc)
                        break
    # Export JSON
        if self.validated:
            if type(self.burst_entries['burst1']).__name__ == 'QLabel':
                burst = [int(burst.text()) for burst in self.burst_entries.values()]
            else:
                burst = [burst.value() for burst in self.burst_entries.values()]
            
            if type(self.arrival_entries['arrival1']).__name__ == 'QLabel':
                arrival = [int(arrival.text()) for arrival in self.arrival_entries.values()]
            else:
                arrival = [arrival.value() for arrival in self.arrival_entries.values()]
            
            if self.priority_isActive:
                if type(self.priority_entries['priority_num1']).__name__ == 'QLabel':
                    priority = [int(priority.text()) for priority in self.priority_entries.values()]
                else:
                    priority = [int(priority.currentText()) for priority in self.priority_entries.values()]
            if self.priority_isActive:
                dictionary ={
                    'Process' : [process.text() for process in self.process_entries.values()],
                    'Burst Time' : burst,
                    'Arrival Time' : arrival,
                    'Priority No.' : priority
                    }
            else:
                dictionary ={
                    'Process' : [process.text() for process in self.process_entries.values()],
                    'Burst Time' : burst,
                    'Arrival Time' : arrival
                    }
            
            with open(f"{usrfile_name}.json", "w") as outfile:
                json.dump(dictionary, outfile, indent=4)

            global D
            global X
            global pick
            
            D = dictionary

            if self.fcfs_radioBtn.isChecked():
                pick = 'fcfs'
                X = pm.process_management_EXEC(usrfile_name, key='fcfs')
                self.next_window(D, X)

            elif self.sjf_radioBtn.isChecked():
                pick = 'sjf'
                X = pm.process_management_EXEC(usrfile_name, key='sjf')
                self.next_window(D, X)

            elif self.priority_radioBtn.isChecked():
                if self.preemptive_cbx.isChecked():
                    pick = 'priority_p'
                    X = pm.priority(usrfile_name, key='p')
                    self.next_window(D, X)
                else:
                    pick = 'priority_np'
                    X = pm.priority(usrfile_name, key='np')
                    self.next_window(D, X)

            elif self.srt_radioBtn.isChecked():
                    pick = 'srtf'
                    X = pm.srtf(usrfile_name)
                    self.next_window(D, X)
            
            elif self.rr_radioBtn.isChecked():
                pick = 'rr'
                X = pm.round_robin(usrfile_name)
                self.next_window(D, X)

            print('VALIDATED')
        else:
            print('NOT VALIDATED')
    
    def next_window(self, inputs, Data):
        self.newWindow = MyWindow()
        self.second_ui = PM_ProcessWindow(self.newWindow, inputs, Data)
        
        if self.fcfs_radioBtn.isChecked():
            self.second_ui.partition_title.setText('Process Management - FCFS')

        elif self.sjf_radioBtn.isChecked():
            self.second_ui.partition_title.setText('Process Management - SJF')
        
        elif self.priority_radioBtn.isChecked():
            if self.preemptive_cbx.isChecked():
                self.second_ui.partition_title.setText('Process Management - Priority (Preemptive)')
            else:
                self.second_ui.partition_title.setText('Process Management - Priority (Non-Preemptive)')
        
        elif self.srt_radioBtn.isChecked():
            self.second_ui.partition_title.setText('Process Management - SRTF')

        elif self.rr_radioBtn.isChecked():
            self.second_ui.partition_title.setText('Process Management - RR (q = 5)')
        self.newWindow.show()
        self.MainWindow.hide()

class PM_ProcessWindow:
    H_END = 557
    def __init__(self, MainWindow, inputs, D):
        self.gantt_list, self.gantt_label, self.message  = D[0], D[1], D[2]
        self.CPU_Utilization, self.Start, self.Finish = D[3], D[4], D[5]
        self.PROCESS, self.BURST, self.ARRIVAL = D[6], D[7], D[8]
        self.idle_sum = D[9]

        global pick
        if (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.remaining_T = D[10]

        self.inputs = inputs
        self.MainWindow = MainWindow
        self.idx = 0
        self.fixed = False
        self.d = {}
        self.labels = {}
        self.mem_labels ={}
        self.error_msg_value = 0
        global dark
        self.dark_theme_enabled = dark
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path('Images\MainWindow.png')))
        MainWindow.setFixedSize(917, 655)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_memoryMap = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_memoryMap.setGeometry(QtCore.QRect((917//2)-(600//2)-50, 435, 600, 150))

        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Group_memoryMap.setFont(font)
        self.Group_memoryMap.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Group_memoryMap.setObjectName("Group_memoryMap")
        self.Group_Entry_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_Entry_table.setGeometry(QtCore.QRect((917//2)-(451//2)-50, 80, 451, 291))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Group_Entry_table.setFont(font)
        self.Group_Entry_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_Entry_table.setCheckable(False)
        self.Group_Entry_table.setChecked(False)
        self.Group_Entry_table.setObjectName("Group_Entry_table")
        self.Entry_Table = QtWidgets.QTableWidget(self.Group_Entry_table)
        self.Entry_Table.setGeometry(QtCore.QRect(10, 27, 432, 251))
        self.Entry_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Entry_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Entry_Table.setFont(font)
        self.Entry_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Entry_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Entry_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.Entry_Table.verticalHeader().setVisible(False) # Row Index
        self.Entry_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.Entry_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        
        self.Entry_Table.setAutoScroll(True)
        self.Entry_Table.setAlternatingRowColors(True)
        self.Entry_Table.setObjectName("Entry_Table")
        self.Entry_Table.setColumnCount(3)
        
        if (pick == 'priority_p' or pick == 'priority_np'):
            self.Entry_Table.setColumnCount(4)
        self.Entry_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Entry_Table.setHorizontalHeaderItem(0, item)
        self.Entry_Table.setItemDelegateForColumn(0, AlignDelegate(self.Entry_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Entry_Table.setHorizontalHeaderItem(1, item)
        self.Entry_Table.setItemDelegateForColumn(1, AlignDelegate(self.Entry_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Entry_Table.setHorizontalHeaderItem(2, item)
        self.Entry_Table.setItemDelegateForColumn(2, AlignDelegate(self.Entry_Table))
        if (pick == 'priority_p' or pick == 'priority_np'):
            item = QtWidgets.QTableWidgetItem()
            self.Entry_Table.setHorizontalHeaderItem(3, item)
            self.Entry_Table.setItemDelegateForColumn(3, AlignDelegate(self.Entry_Table))
        self.Entry_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.Entry_Table.horizontalHeaderItem(0).setFont(font)
        self.Entry_Table.horizontalHeaderItem(1).setFont(font)
        self.Entry_Table.horizontalHeaderItem(2).setFont(font)
        if (pick == 'priority_p' or pick == 'priority_np'):
            self.Entry_Table.horizontalHeaderItem(3).setFont(font)
             
        self.Entry_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.Entry_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.Entry_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        if (pick == 'priority_p' or pick == 'priority_np'):
            self.Entry_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.Entry_Table.verticalHeader().setDefaultSectionSize(44)

        self.partition_title = QtWidgets.QLabel(self.centralwidget)
        self.partition_title.setGeometry(QtCore.QRect((917//2)-(840//2)-33, 5, 840, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.partition_title.setFont(font)
        self.partition_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.partition_title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.partition_title.setLineWidth(1)
        self.partition_title.setAlignment(QtCore.Qt.AlignCenter)
        self.partition_title.setObjectName("partition_title")
        self.prev_button = QtWidgets.QPushButton(self.centralwidget)
        self.prev_button.setGeometry(QtCore.QRect(445, 600, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.prev_button.setFont(font)
        self.prev_button.setObjectName("prev_button")
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(595, 600, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.next_button.setFont(font)
        self.next_button.setObjectName("next_button")
        self.simplify_cbx = QtWidgets.QCheckBox(self.centralwidget)
        self.simplify_cbx.setGeometry(QtCore.QRect(775, 605, 65, 19))
        self.simplify_cbx.setFont(font)
        self.simplify_cbx.setObjectName("simplify_cbx")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect((917//2)-(500//2)+50, 400, 500, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.message_label.setFont(font)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setObjectName("message_label")
        self.horizontalLayout.addWidget(self.message_label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 917, 28))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuHelp.setFont(font)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAbout = QtWidgets.QMenu(self.menuHelp)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAbout.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/message.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAbout.setIcon(icon)
        self.menuAbout.setObjectName("menuAbout")
        self.menuDevelopers = QtWidgets.QMenu(self.menuAbout)
        icon0 = QtGui.QIcon()
        icon0.addPixmap(QtGui.QPixmap(resource_path("Icons/group.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuDevelopers.setIcon(icon0)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuDevelopers.setFont(font)
        self.menuDevelopers.setObjectName("menuDevelopers")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuAppearance = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance.setFont(font)
        self.menuAppearance.setObjectName("menuAppearance")
        self.menuAppearance_2 = QtWidgets.QMenu(self.menuAppearance)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setWeight(50)
        self.menuAppearance_2.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/favorite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuAppearance_2.setIcon(icon)
        self.menuAppearance_2.setObjectName("menuAppearance_2")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.toolBar.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setAcceptDrops(False)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setMovable(True)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setIconSize(QtCore.QSize(30, 25))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionHome = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/house_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon)
        self.actionHome.setObjectName("actionHome")
        self.actionLyra = QtWidgets.QAction(MainWindow)
        self.actionLyra.setObjectName("actionLyra")
        self.actionRyan = QtWidgets.QAction(MainWindow)
        self.actionRyan.setObjectName("actionRyan")
        self.actionJoshua = QtWidgets.QAction(MainWindow)
        self.actionJoshua.setObjectName("actionJoshua")
        self.actionLyra_2 = QtWidgets.QAction(MainWindow)
        self.actionLyra_2.setObjectName("actionLyra_2")
        self.actionRyan_2 = QtWidgets.QAction(MainWindow)
        self.actionRyan_2.setObjectName("actionRyan_2")
        self.actionJoshua_2 = QtWidgets.QAction(MainWindow)
        self.actionJoshua_2.setObjectName("actionJoshua_2")
        self.actionKent = QtWidgets.QAction(MainWindow)
        self.actionKent.setObjectName("actionKent")
        self.actionGrant = QtWidgets.QAction(MainWindow)
        self.actionGrant.setObjectName("actionGrant")
        self.actionThis_partition = QtWidgets.QAction(MainWindow)
        iconx = QtGui.QIcon()
        iconx.addPixmap(QtGui.QPixmap(resource_path("Icons/page.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionThis_partition.setIcon(iconx)
        self.actionThis_partition.setObjectName("actionThis_partition")
        self.actionHow_to_use = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("Icons/idea.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHow_to_use.setIcon(icon)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.actionCSV = QtWidgets.QAction(MainWindow)
        self.actionCSV.setObjectName("actionCSV")
        self.actionPNG = QtWidgets.QAction(MainWindow)
        self.actionPNG.setObjectName("actionPNG")
        self.actionJPEG = QtWidgets.QAction(MainWindow)
        self.actionJPEG.setObjectName("actionJPEG")
        self.actionCSV_2 = QtWidgets.QAction(MainWindow)
        self.actionCSV_2.setObjectName("actionCSV_2")
        self.actionPNG_2 = QtWidgets.QAction(MainWindow)
        self.actionPNG_2.setObjectName("actionPNG_2")
        self.actionJPEG_2 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_2.setObjectName("actionJPEG_2")
        self.actionJPEG_3 = QtWidgets.QAction(MainWindow)
        self.actionJPEG_3.setObjectName("actionJPEG_3")
        self.actionSave_image = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/picture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_image.setIcon(icon1)
        self.actionSave_image.setObjectName("actionSave_image")
        self.actionclose = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("Icons/Close_Icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionclose.setIcon(icon2)
        self.actionclose.setObjectName("actionclose")
        self.actionExport_csv = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("Icons/calendar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport_csv.setIcon(icon3)
        self.actionExport_csv.setObjectName("actionExport_csv")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(resource_path("Icons/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen_Recent = QtWidgets.QAction(MainWindow)
        self.actionOpen_Recent.setObjectName("actionOpen_Recent")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(resource_path("Icons/write.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon5)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.actionNew.setFont(font)
        self.actionNew.setObjectName("actionNew")
        self.actionDark_Mode = QtWidgets.QAction(MainWindow)
        self.actionDark_Mode.setObjectName("actionDark_Mode")
        self.actionLight_Mode = QtWidgets.QAction(MainWindow)
        self.actionLight_Mode.setObjectName("actionLight_Mode")
        self.actionJump_to = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(resource_path("Icons/clock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJump_to.setIcon(icon6)
        self.actionJump_to.setObjectName("actionJump_to")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(resource_path("Icons/turn_off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon7)
        self.actionExit.setObjectName("actionExit")
        self.actionShow_ATA_Table = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(resource_path("Icons/presentation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_ATA_Table.setIcon(icon8)
        self.actionShow_ATA_Table.setObjectName("actionShow_ATA_Table")

        self.menuDevelopers.addAction(self.actionLyra_2)
        self.menuDevelopers.addAction(self.actionRyan_2)
        self.menuDevelopers.addAction(self.actionKent)
        self.menuDevelopers.addAction(self.actionJoshua_2)
        self.menuDevelopers.addAction(self.actionGrant)
        self.menuAbout.addAction(self.actionThis_partition)
        self.menuAbout.addAction(self.menuDevelopers.menuAction())
        self.menuHelp.addAction(self.actionHow_to_use)
        self.menuHelp.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_image)
        self.menuFile.addAction(self.actionExport_csv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionclose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAppearance_2.addAction(self.actionLight_Mode)
        self.menuAppearance_2.addAction(self.actionDark_Mode)
        self.menuAppearance.addAction(self.menuAppearance_2.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAppearance.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionJump_to)
        self.toolBar.addAction(self.actionShow_ATA_Table)
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")
        
        # self.label_zero = QtWidgets.QLabel(self.Group_memoryMap)
        # self.label_zero.setText('0')
        # self.label_zero.adjustSize()
        # self.label_zero.setAlignment(QtCore.Qt.AlignRight)
        # self.label_zero.setGeometry(QtCore.QRect(0, 30, 43, 13))
        # self.label_zero.setObjectName("label_zero")

        # self.label_memory_size = QtWidgets.QLabel(self.Group_memoryMap)
        # self.label_memory_size.setText(f'{0}')
        # self.label_memory_size.adjustSize()
        # self.label_memory_size.setAlignment(QtCore.Qt.AlignRight)
        # self.label_memory_size.setGeometry(QtCore.QRect(0, V_END+30, 43, 13))
        # self.label_memory_size.setObjectName("label_memory_size")

        self.h_line = QtWidgets.QFrame(self.Group_memoryMap)
        self.h_line.setGeometry(QtCore.QRect(25, 25, self.H_END, 20))
        self.h_line.setLineWidth(2)
        self.h_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.h_line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.h_line.setObjectName("h_line")

        self.h_line2 = QtWidgets.QFrame(self.Group_memoryMap)
        self.h_line2.setGeometry(QtCore.QRect(25, 110, self.H_END, 20))
        self.h_line2.setLineWidth(2)
        self.h_line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.h_line2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.h_line2.setObjectName("h_line2")

        self.v_line = QtWidgets.QFrame(self.Group_memoryMap)
        self.v_line.setGeometry(QtCore.QRect(20, 35, 10, 85))
        self.v_line.setLineWidth(2)
        self.v_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.v_line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.v_line.setObjectName("v_line")

        self.v_line2 = QtWidgets.QFrame(self.Group_memoryMap)
        self.v_line2.setGeometry(QtCore.QRect(self.H_END+18, 35, 10, 85))
        self.v_line2.setLineWidth(2)
        self.v_line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.v_line2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.v_line2.setObjectName("v_line2")

        self.label_zero = QtWidgets.QLabel(self.Group_memoryMap)
        self.label_zero.setText('0')
        self.label_zero.setGeometry(QtCore.QRect(19, 127, 10, 85))
        self.label_zero.setAlignment(QtCore.Qt.AlignRight)
        self.label_zero.setObjectName('label_zero')

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.show_entry_table()
        self.button_state()
        self.create_remaining_table()
        self.show_remaining(self.idx)

        # self.show_line_LOC(self.idx)
        # self.show_pointer_labels(self.idx)
        # self.show_memory_labels(self.idx)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Process Management"))
        self.Group_memoryMap.setTitle(_translate("MainWindow", "Gantt Chart"))
        self.Group_Entry_table.setTitle(_translate("MainWindow", "Entries"))
        item = self.Entry_Table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Process"))
        item = self.Entry_Table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Burst time"))
        item = self.Entry_Table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Arrival time"))
        if (pick == 'priority_p' or pick == 'priority_np'):
            item = self.Entry_Table.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Priority No."))
        
        # self.Group_osSize.setTitle(_translate("MainWindow", "OS Size"))
        # self.OS_size_label.setText(_translate("MainWindow", f"{self.inputs['OS size']}"))
        # self.Group_memSize.setTitle(_translate("MainWindow", "Memory Size"))
        # self.mem_size_label.setText(_translate("MainWindow", f"{self.inputs['Memory size']}"))
        self.partition_title.setText(_translate("MainWindow", "Process Management - FCFS"))
        self.prev_button.setText(_translate("MainWindow", "Prev"))
        self.next_button.setText(_translate("MainWindow", "Next"))
        self.simplify_cbx.setText(_translate("MainWindow", "Simplify"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuDevelopers.setTitle(_translate("MainWindow", "Developers"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAppearance.setTitle(_translate("MainWindow", "View"))
        self.menuAppearance_2.setTitle(_translate("MainWindow", "Theme"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Tool Bar"))
        self.actionHome.setText(_translate("MainWindow", "Home"))
        self.actionLyra.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua.setText(_translate("MainWindow", "Joshua"))
        self.actionLyra_2.setText(_translate("MainWindow", "Lyra"))
        self.actionRyan_2.setText(_translate("MainWindow", "Ryan"))
        self.actionJoshua_2.setText(_translate("MainWindow", "Joshua"))
        self.actionKent.setText(_translate("MainWindow", "Kent"))
        self.actionGrant.setText(_translate("MainWindow", "Grant"))
        self.actionThis_partition.setText(_translate("MainWindow", "This partition"))
        self.actionHow_to_use.setText(_translate("MainWindow", "How to use"))
        self.actionCSV.setText(_translate("MainWindow", "CSV"))
        self.actionPNG.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG.setText(_translate("MainWindow", "JPEG"))
        self.actionCSV_2.setText(_translate("MainWindow", "CSV"))
        self.actionPNG_2.setText(_translate("MainWindow", "PNG"))
        self.actionJPEG_2.setText(_translate("MainWindow", "JPEG"))
        self.actionJPEG_3.setText(_translate("MainWindow", "JPEG"))
        self.actionSave_image.setText(_translate("MainWindow", "Save Image"))
        self.actionclose.setText(_translate("MainWindow", "Close"))
        self.actionExport_csv.setText(_translate("MainWindow", "Export (.csv)"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen_Recent.setText(_translate("MainWindow", "Open Recent"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionDark_Mode.setText(_translate("MainWindow", "Dark"))
        self.actionLight_Mode.setText(_translate("MainWindow", "Light"))
        self.actionJump_to.setText(_translate("MainWindow", "Jump to"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionShow_ATA_Table.setText(_translate("MainWindow", "Summary"))

        self.message_label.setText(_translate("MainWindow", f'{self.message[self.idx]}'))
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.adjustSize()

        self.next_button.clicked.connect(self.next_clicked)
        self.prev_button.clicked.connect(self.prev_clicked)
        self.actionJump_to.triggered.connect(self.jump_to)
        self.actionShow_ATA_Table.triggered.connect(self.show_ATA_table)
        self.actionLight_Mode.triggered.connect(self.light_theme)
        self.actionDark_Mode.triggered.connect(self.dark_theme)
        self.simplify_cbx.stateChanged.connect(self.simplify_mem_map)
        self.actionNew.triggered.connect(self.new_input)
        self.actionExit.triggered.connect(self.quitting)

        self.actionSave_image.triggered.connect(self.message_to_user)
        self.actionExport_csv.triggered.connect(self.message_to_user)
        self.actionOpen.triggered.connect(self.message_to_user)
        self.actionHow_to_use.triggered.connect(self.message_to_user)
        self.actionThis_partition.triggered.connect(self.message_to_user)

        self.actionclose.triggered.connect(self.closing)
        self.actionHome.triggered.connect(self.goto_home)
    
    def goto_home(self):
        self.new_window = MyWindow()
        self.activate_window = UI_MainWindow(self.new_window)
        self.new_window.show()
        self.MainWindow.hide()

    def message_to_user(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setText("Sorry not available right now, we're still working on this.      ")
        info.setWindowTitle("Info")
        info.exec_()

    def closing(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('This will bring you to the home window, continue?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.goto_home()
            
    def quitting(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to quit?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            sys.exit()

    def new_input(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        notify_user = QtWidgets.QMessageBox()
        # notify_user.question()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.Yes)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('New file?      ')
        notify_user.setWindowTitle("Notify")

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            self.new_window = MyWindow()
            self.activate_window = PM_InputWindow(self.new_window)
            self.new_window.show()
            self.MainWindow.hide()

    def create_remaining_table(self):
        global pick
        if (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            print('SSSSSSSSSSSSSSSSSSSSSSS')
            self.Group_Entry_table.setGeometry(QtCore.QRect(20, 80, 451, 291))
            self.Group_Remaining_table = QtWidgets.QGroupBox(self.centralwidget)
            self.Group_Remaining_table.setGeometry(QtCore.QRect(451+60, 80, 319, 291))
            font = QtGui.QFont()
            font.setFamily("Poppins Medium")
            font.setPointSize(8)
            font.setBold(False)
            font.setItalic(True)
            font.setWeight(50)
            self.Group_Remaining_table.setTitle('Remaining')
            self.Group_Remaining_table.setFont(font)
            self.Group_Remaining_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.Group_Remaining_table.setCheckable(False)
            self.Group_Remaining_table.setChecked(False)
            self.Group_Remaining_table.setObjectName("Group_Remaining_table")
            self.Remaining_Table = QtWidgets.QTableWidget(self.Group_Remaining_table)
            self.Remaining_Table.setGeometry(QtCore.QRect(10, 27, 300, 251))
            self.Remaining_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.Remaining_Table.horizontalHeader().setSortIndicatorShown(False)

            font = QtGui.QFont()
            font.setFamily("Poppins Medium")
            font.setPointSize(9)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(50)

            self.Remaining_Table.setFont(font)
            self.Remaining_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.Remaining_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.Remaining_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
            self.Remaining_Table.verticalHeader().setVisible(False) # Row Index
            self.Remaining_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
            self.Remaining_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
            
            font = QtGui.QFont()
            font.setFamily("Poppins Medium")
            font.setPointSize(8)
            font.setBold(True)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(90)

            self.Remaining_Table.setColumnCount(len(self.PROCESS))
            self.Remaining_Table.setRowCount(0)
            for i in range(len(self.PROCESS)):
                item = QtWidgets.QTableWidgetItem()
                self.Remaining_Table.setHorizontalHeaderItem(i, item)
                item = self.Remaining_Table.horizontalHeaderItem(i)
                item.setText(f'P{i+1}')
                self.Remaining_Table.setItemDelegateForColumn(i, AlignDelegate(self.Remaining_Table))
                self.Remaining_Table.horizontalHeaderItem(i).setFont(font)
                self.Remaining_Table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                self.Remaining_Table.show()
            
            self.Remaining_Table.setAutoScroll(True)
            self.Remaining_Table.setAlternatingRowColors(True)
            self.Remaining_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
            self.Remaining_Table.verticalHeader().setDefaultSectionSize(44)
            self.Remaining_Table.setObjectName("Remaining_Table")

    def show_remaining(self, idx):
        if (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.Remaining_Table.clearContents()
            
            burst_time = fcn.sort_by_process(self.remaining_T[idx])
            burst_time = list(burst_time.values())
            self.Remaining_Table.setRowCount(len(max(burst_time, key=len)))

            for column in range(len(burst_time)):
                for row in range(len(burst_time[column])):
                    self.Remaining_Table.setItem(row, column, QtWidgets.QTableWidgetItem(str(burst_time[column][row])))
                    
    def dark_theme(self):
        # Palette to switch to dark colors:
        # app.setStyle("Fusion")
        global dark
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette().Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette().AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette().ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette().ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette().BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette().Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette().HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)

        self.Entry_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        if (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.Remaining_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")
        self.dark_theme_enabled = True
        dark = True

        for i in range(len(self.mem_labels)):
            if self.mem_labels[f"self.memory_label{i+1}"].text() == 'idle':
                self.mem_labels[f"self.memory_label{i+1}"].setStyleSheet("color: #DBDBDB")
            else:
                self.mem_labels[f"self.memory_label{i+1}"].setStyleSheet("color: #A569BD") 
    
    def light_theme(self):
        global dark
        palette = QtGui.QPalette()
        app.setPalette(palette)

        self.Entry_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        if (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.Remaining_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #6C3483;}')
        self.toolBar.setStyleSheet("QToolBar{spacing:10px;}")
        self.dark_theme_enabled = False
        dark = False

        for i in range(len(self.mem_labels)):
            if self.mem_labels[f"self.memory_label{i+1}"].text() == 'idle':
                self.mem_labels[f"self.memory_label{i+1}"].setStyleSheet("color: #4F4F4F")  
            else:
                self.mem_labels[f"self.memory_label{i+1}"].setStyleSheet("color: #8E44AD") 
    
    def show_entry_table(self):
        process_id = self.inputs['Process']
        burst_time = self.inputs['Burst Time']
        arrival_time = self.inputs['Arrival Time']
        global pick
        if (pick == 'priority_p' or pick == 'priority_np'):
            priority = self.inputs['Priority No.']

        self.Entry_Table.clearContents()
        self.Entry_Table.setRowCount(len(arrival_time))

        for row in range(len(arrival_time)):
            self.Entry_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(process_id[row])))
            self.Entry_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(burst_time[row])))
            self.Entry_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(arrival_time[row])))
            if (pick == 'priority_p' or pick == 'priority_np'):
                self.Entry_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(priority[row])))
    
    def simplify_mem_map(self):
        if self.simplify_cbx.isChecked():
            if self.fixed == False:
                self.fixed = True
        else:
            if self.fixed == True:
                self.fixed = False

        if len(self.gantt_list) > 1:
            self.new_mem_map = fcn.margin_memory_loc(self.gantt_list, self.H_END, y=30, fixed=self.fixed)
            self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)

            for i in range(len(self.d)):
                self.d[f"vertical_line{i+1}"].setGeometry(QtCore.QRect(self.new_mem_map[i]+19, 35, 10, 85))
                self.labels[f"pointer_label{i+1}"].setGeometry(QtCore.QRect(self.new_mem_map[i]+19, 127, 10, 85))
                self.labels[f"pointer_label{i+1}"].adjustSize()
                self.labels[f"pointer_label{i+1}"].setAlignment(QtCore.Qt.AlignRight)
                self.mem_labels[f"self.memory_label{i+1}"].setGeometry(QtCore.QRect(self.memory_label_yloc[0][i]+19, 70, 270, 13))
                self.mem_labels[f"self.memory_label{i+1}"].adjustSize()
                self.mem_labels[f"self.memory_label{i+1}"].setAlignment(QtCore.Qt.AlignCenter)
    
            
        # self.show_label_LOC(self.mem_map[self.idx], self.fixed)
        # self.show_MMlabel_LOC(self.mem_map[self.idx], self.fixed)
    
    def button_state(self):
        if self.idx == len(self.gantt_list):
            self.next_button.setEnabled(False)
            self.end_show = True
        else:
            self.next_button.setEnabled(True)
        
        if self.idx == 0:
            self.prev_button.setEnabled(False)
        else:
            self.prev_button.setEnabled(True)

    def next_clicked(self):
        try:
            self.show_line_LOC(self.idx)
            self.show_pointer_labels(self.idx)
            self.show_memory_labels(self.idx)
            self.idx += 1
            self.show_remaining(self.idx)
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()
        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1

        self.button_state()
    
    def prev_clicked(self):
        try:
            self.remove()
            self.idx -= 1
            self.show_remaining(self.idx)
            self.message_label.setText(self.message[self.idx])
            self.message_label.setAlignment(QtCore.Qt.AlignCenter)
            self.message_label.adjustSize()

        except IndexError:
            if self.error_msg_value == 0:
                self.MainWindow.setWindowTitle('An error as occured when processing your data :(')
                self.show_error_message()
                self.error_msg_value = 1

        self.button_state()
    
    def show_error_message(self):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)

        info = QtWidgets.QMessageBox()
        info.setIcon(QtWidgets.QMessageBox.Information)
        info.setFont(font)
        info.setTextFormat(QtCore.Qt.RichText)
        info.setText("Sorry, an error has occured when I begin to process your data. We're still working on this, please try another input. \
                    <a href='https://www.facebook.com/xtnctx'><br><br>Tell me about the error</br></br></a>    ")
        info.setWindowTitle("Developer message")
        info.exec_()

    # Make unique objects returning in different memory location (of Python)
    def show_line_LOC(self, idx):
        if len(self.gantt_list) == 1:
            self.d[f"vertical_line{len(self.d)+1}"] = QtWidgets.QFrame(self.Group_memoryMap)
            self.d[f"vertical_line{len(self.d)}"].setGeometry(QtCore.QRect(self.H_END+19, 35, 10, 85))
            self.d[f"vertical_line{len(self.d)}"].setLineWidth(2)
            self.d[f"vertical_line{len(self.d)}"].setFrameShape(QtWidgets.QFrame.VLine)
            self.d[f"vertical_line{len(self.d)}"].setFrameShadow(QtWidgets.QFrame.Raised)
            self.d[f"vertical_line{len(self.d)}"].setObjectName(f"vertical_line{len(self.d)}")
            self.d[f"vertical_line{len(self.d)}"].show()
        else:
            self.new_mem_map = fcn.margin_memory_loc(self.gantt_list, self.H_END, y=30, fixed=self.fixed)
            self.d[f"vertical_line{len(self.d)+1}"] = QtWidgets.QFrame(self.Group_memoryMap)
            self.d[f"vertical_line{len(self.d)}"].setGeometry(QtCore.QRect(self.new_mem_map[idx]+19, 35, 10, 85))
            self.d[f"vertical_line{len(self.d)}"].setLineWidth(2)
            self.d[f"vertical_line{len(self.d)}"].setFrameShape(QtWidgets.QFrame.VLine)
            self.d[f"vertical_line{len(self.d)}"].setFrameShadow(QtWidgets.QFrame.Raised)
            self.d[f"vertical_line{len(self.d)}"].setObjectName(f"vertical_line{len(self.d)}")
            self.d[f"vertical_line{len(self.d)}"].show()
        print(self.d)
    
    def remove(self):
        self.d[f"vertical_line{len(self.d)}"].hide()
        self.labels[f"pointer_label{len(self.labels)}"].hide()
        self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].hide()

        del self.d[f"vertical_line{len(self.d)}"]
        del self.labels[f"pointer_label{len(self.labels)}"]
        del self.mem_labels[f"self.memory_label{len(self.mem_labels)}"]
        print(self.d)

    def show_pointer_labels(self, idx):
        if len(self.gantt_list) == 1:
            self.labels[f"pointer_label{len(self.labels)+1}"] = QtWidgets.QLabel(self.Group_memoryMap)
            self.labels[f"pointer_label{len(self.labels)}"].setText(f"{self.gantt_list[idx]}")
            self.labels[f"pointer_label{len(self.labels)}"].setGeometry(QtCore.QRect(self.H_END+19, 127, 10, 85))
            self.labels[f"pointer_label{len(self.labels)}"].adjustSize()
            self.labels[f"pointer_label{len(self.labels)}"].setAlignment(QtCore.Qt.AlignRight)
            self.labels[f"pointer_label{len(self.labels)}"].setObjectName(f"pointer_label{len(self.labels)}")
            self.labels[f"pointer_label{len(self.labels)}"].show()
        else:
            self.new_mem_map = fcn.margin_memory_loc(self.gantt_list, self.H_END, y=30, fixed=self.fixed)
            self.labels[f"pointer_label{len(self.labels)+1}"] = QtWidgets.QLabel(self.Group_memoryMap)
            self.labels[f"pointer_label{len(self.labels)}"].setText(f"{self.gantt_list[idx]}")
            self.labels[f"pointer_label{len(self.labels)}"].setGeometry(QtCore.QRect(self.new_mem_map[idx]+19, 127, 10, 85))
            self.labels[f"pointer_label{len(self.labels)}"].adjustSize()
            self.labels[f"pointer_label{len(self.labels)}"].setAlignment(QtCore.Qt.AlignRight)
            self.labels[f"pointer_label{len(self.labels)}"].setObjectName(f"pointer_label{len(self.labels)}")
            self.labels[f"pointer_label{len(self.labels)}"].show()
    
    def show_memory_labels(self, idx):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        font.setKerning(True)

        if len(self.gantt_list) == 1:
            self.mem_labels[f"self.memory_label{len(self.mem_labels)+1}"] = QtWidgets.QLabel(self.Group_memoryMap)
            self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setText(f"{self.gantt_label[idx]}")
            self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setGeometry(QtCore.QRect((self.H_END // 2)+19, 70, 270, 13))
        else:
            self.new_mem_map = fcn.margin_memory_loc(self.gantt_list, self.H_END, y=30, fixed=self.fixed)
            self.memory_label_yloc = fcn.memory_label_yloc([self.new_mem_map], self.fixed)

            self.mem_labels[f"self.memory_label{len(self.mem_labels)+1}"] = QtWidgets.QLabel(self.Group_memoryMap)
            self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setText(f"{self.gantt_label[idx]}")
            self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setGeometry(QtCore.QRect(self.memory_label_yloc[0][idx]+19, 70, 270, 13))

        if self.gantt_label[idx] == 'idle':
            if self.dark_theme_enabled:
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setFont(font)
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setStyleSheet("color: #DBDBDB")
            else:
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setFont(font)
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setStyleSheet("color: #4F4F4F")
        else:
            if self.dark_theme_enabled:
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setFont(font)
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setStyleSheet("color: #A569BD")
            else:
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setFont(font)
                self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setStyleSheet("color: #8E44AD")
            

        self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].adjustSize()
        self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setAlignment(QtCore.Qt.AlignCenter)
        self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].setObjectName("memory_label")
        self.mem_labels[f"self.memory_label{len(self.mem_labels)}"].show()
    
    def show_ATA_table(self):
        self.second_ui = PM_SummaryTableWindow([self.PROCESS, self.Start, self.Finish, self.ARRIVAL, self.idle_sum, self.CPU_Utilization, self.gantt_list])
    
    def jump_to(self):
        self.timelist_window = QtWidgets.QMainWindow()
        self.timelist_ui = PM_TimeList(self.timelist_window, self.gantt_list)
        self.timelist_ui.pushButton.clicked.connect(self.go_)
        self.timelist_window.show()

    def go_(self):
        for _ in range(len(self.d)):
            self.prev_clicked()
        
        for _ in range(self.timelist_ui.comboBox.currentIndex()):
            self.next_clicked()
        
        self.button_state()

class PM_SummaryTableWindow(QtWidgets.QMainWindow):
    def __init__(self, D):
        super().__init__()
        self.PROCESS, self.Start, self.Finish = D[0], D[1], D[2]
        self.ARRIVAL, self.idle_sum, self.CPU_Utilization, self.gantt_list = D[3], D[4], D[5], D[6]
        print(self.PROCESS)
        if not (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.xATA = self.sort_by_process(self.PROCESS.copy(), self.Finish.copy(), self.ARRIVAL.copy())
            self.xAWT = self.sort_by_process(self.PROCESS.copy(), self.Start.copy(), self.ARRIVAL.copy())
        print(self.PROCESS)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        w = 451
        h = 400
        x = 500-w-((500-w)//2)
        y = 390-291-((390-291)//2)

        screen_resolution = QtWidgets.QDesktopWidget().availableGeometry()
        width = screen_resolution.width()
        height = screen_resolution.height()

        self.Group_ATA_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_ATA_table.setGeometry(QtCore.QRect( ((width//4)-(w//2)), y, w, h))
        self.Group_ATA_table.setStyleSheet('QGroupBox:title {color: rgb(231, 118, 108);}')
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Group_ATA_table.setFont(font)
        self.Group_ATA_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_ATA_table.setTitle('Average Turnaround time')
        self.Group_ATA_table.setCheckable(False)
        self.Group_ATA_table.setChecked(False)
        self.Group_ATA_table.setObjectName("Group_ATA_table")

        self.close_btn = QtWidgets.QPushButton(self.centralwidget)
        self.close_btn.setText("x")
        self.close_btn.setGeometry(QtCore.QRect( (width)-35, 5, self.close_btn.width(), self.close_btn.height()))
        font = QtGui.QFont()
        font.setPixelSize(25)
        font.setBold(True)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet("color: white; border: 0px")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.hide)

        self.ATA_Table = QtWidgets.QTableWidget(self.Group_ATA_table)
        self.ATA_Table.setGeometry(QtCore.QRect(10, 76, 432, 251))
        self.ATA_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ATA_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ATA_Table.setFont(font)
        self.ATA_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ATA_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ATA_Table.verticalHeader().setVisible(False) # Row Index
        self.ATA_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.ATA_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #E74C3C;}')
        
        self.ATA_Table.setAutoScroll(True)
        self.ATA_Table.setAlternatingRowColors(True)
        self.ATA_Table.setObjectName("ATA_Table")
        self.ATA_Table.setColumnCount(4)
        self.ATA_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ATA_Table.setHorizontalHeaderItem(0, item)
        self.ATA_Table.setItemDelegateForColumn(0, AlignDelegate(self.ATA_Table))
        item = QtWidgets.QTableWidgetItem()
        self.ATA_Table.setHorizontalHeaderItem(1, item)
        self.ATA_Table.setItemDelegateForColumn(1, AlignDelegate(self.ATA_Table))
        item = QtWidgets.QTableWidgetItem()
        self.ATA_Table.setHorizontalHeaderItem(2, item)
        self.ATA_Table.setItemDelegateForColumn(2, AlignDelegate(self.ATA_Table))
        item = QtWidgets.QTableWidgetItem()
        self.ATA_Table.setHorizontalHeaderItem(3, item)
        self.ATA_Table.setItemDelegateForColumn(3, AlignDelegate(self.ATA_Table))
        self.ATA_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.ATA_Table.horizontalHeaderItem(0).setText("Process")
        self.ATA_Table.horizontalHeaderItem(1).setText("Finish")
        self.ATA_Table.horizontalHeaderItem(2).setText("Arrival")
        self.ATA_Table.horizontalHeaderItem(3).setText("Turnaround time")

        self.ATA_Table.horizontalHeaderItem(0).setFont(font)
        self.ATA_Table.horizontalHeaderItem(1).setFont(font)
        self.ATA_Table.horizontalHeaderItem(2).setFont(font)
        self.ATA_Table.horizontalHeaderItem(3).setFont(font)
             
        self.ATA_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ATA_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ATA_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.ATA_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.ATA_Table.verticalHeader().setDefaultSectionSize(44)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)

        self.TAT_sum = QtWidgets.QLabel(self.Group_ATA_table)
        self.TAT_sum.setFont(font)
        self.TAT_sum.setStyleSheet("color: #FFFFFF")

        if not (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.Turnaround_Time = [self.xATA[1][i] - self.xATA[2][i] for i in range(len(self.xATA[2]))]
            self.TAT_sum.setText(f"SUM(Turnaround):\n{sum(self.Turnaround_Time)}")
        else:
            self.T_sum = fcn.generate_str_SUM(self.Finish)[1]
            self.TAT_sum.setText(f"SUM(Turnaround):\n{self.T_sum}")
        self.TAT_sum.adjustSize()
        self.TAT_sum.setGeometry(QtCore.QRect((451//8) - (self.TAT_sum.width() // 8), 340, self.TAT_sum.width(), self.TAT_sum.height()))
        self.TAT_sum.setAlignment(QtCore.Qt.AlignCenter)
        self.TAT_sum.setObjectName("TAT_sum")

        self.TAT_Average = QtWidgets.QLabel(self.Group_ATA_table)
        self.TAT_Average.setFont(font)
        self.TAT_Average.setStyleSheet("color: #FFFFFF")
        if not (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            average = sum(self.Turnaround_Time)/len(self.PROCESS)
            print(average)
            if len(str(average).split('.')[1]) == 1 and str(average).split('.')[1] == '0':
                self.TAT_Average.setText(f"Average:\n{int(average)}")
            else:
                averagex = '{:.2f}'.format(average)
                self.TAT_Average.setText(f"Average:\n{averagex} ≈ {fcn.xround(average)}")
        else:
            T_average = self.T_sum / len(self.PROCESS)
            if len(str(T_average).split('.')[1]) == 1 and str(T_average).split('.')[1] == '0':
                self.TAT_Average.setText(f"Average:\n{int(T_average)}")
            else:
                averagex = '{:.2f}'.format(T_average)
                self.TAT_Average.setText(f"Average:\n{averagex} ≈ {fcn.xround(T_average)}")

        self.TAT_Average.adjustSize()
        self.TAT_Average.setGeometry(QtCore.QRect(((451) - (self.TAT_Average.width())) - 40, 340, self.TAT_Average.width(), self.TAT_Average.height()))
        self.TAT_Average.setAlignment(QtCore.Qt.AlignCenter)
        self.TAT_Average.setObjectName("TAT_Average")

        ###
        self.Group_AWT_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_AWT_table.setGeometry(QtCore.QRect( width - (w + (w//4)), y, w, h))
        self.Group_AWT_table.setStyleSheet('QGroupBox:title {color: rgb(53, 187, 51);}')
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Group_AWT_table.setFont(font)
        self.Group_AWT_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_AWT_table.setTitle('Average Waiting Time')
        self.Group_AWT_table.setCheckable(False)
        self.Group_AWT_table.setChecked(False)
        self.Group_AWT_table.setObjectName("Group_AWT_table")

        self.AWT_Table = QtWidgets.QTableWidget(self.Group_AWT_table)
        self.AWT_Table.setGeometry(QtCore.QRect(10, 76, 432, 251))
        self.AWT_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.AWT_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.AWT_Table.setFont(font)
        self.AWT_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        if (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.AWT_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        else:
            self.AWT_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.AWT_Table.verticalHeader().setVisible(False) # Row Index
        self.AWT_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.AWT_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #35BB33;}')
        
        self.AWT_Table.setAutoScroll(True)
        self.AWT_Table.setAlternatingRowColors(True)
        self.AWT_Table.setObjectName("ATA_Table")
        self.AWT_Table.setColumnCount(4)
        self.AWT_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.AWT_Table.setHorizontalHeaderItem(0, item)
        self.AWT_Table.setItemDelegateForColumn(0, AlignDelegate(self.AWT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.AWT_Table.setHorizontalHeaderItem(1, item)
        self.AWT_Table.setItemDelegateForColumn(1, AlignDelegate(self.AWT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.AWT_Table.setHorizontalHeaderItem(2, item)
        self.AWT_Table.setItemDelegateForColumn(2, AlignDelegate(self.AWT_Table))
        item = QtWidgets.QTableWidgetItem()
        self.AWT_Table.setHorizontalHeaderItem(3, item)
        self.AWT_Table.setItemDelegateForColumn(3, AlignDelegate(self.AWT_Table))
        self.AWT_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.AWT_Table.horizontalHeaderItem(0).setText("Process")
        self.AWT_Table.horizontalHeaderItem(1).setText("Start")
        self.AWT_Table.horizontalHeaderItem(2).setText("Arrival")
        self.AWT_Table.horizontalHeaderItem(3).setText("Waiting time")

        self.AWT_Table.horizontalHeaderItem(0).setFont(font)
        self.AWT_Table.horizontalHeaderItem(1).setFont(font)
        self.AWT_Table.horizontalHeaderItem(2).setFont(font)
        self.AWT_Table.horizontalHeaderItem(3).setFont(font)
             
        self.AWT_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.AWT_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.AWT_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.AWT_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.AWT_Table.verticalHeader().setDefaultSectionSize(44)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)

        self.WT_sum = QtWidgets.QLabel(self.Group_AWT_table)
        self.WT_sum.setFont(font)
        self.WT_sum.setStyleSheet("color: #FFFFFF")

        if not (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            self.Waiting_Time = [self.xAWT[1][i] - self.xAWT[2][i] for i in range(len(self.xAWT[2]))]
            self.WT_sum.setText(f"SUM(Waiting):\n{sum(self.Waiting_Time)}")
        else:
            self.W_sum = fcn.generate_str_SUM(self.Start)[1]
            self.WT_sum.setText(f"SUM(Waiting):\n{self.W_sum}")

        self.WT_sum.adjustSize()
        self.WT_sum.setGeometry(QtCore.QRect((451//8) - (self.WT_sum.width() // 8), 340, self.WT_sum.width(), self.WT_sum.height()))
        self.WT_sum.setAlignment(QtCore.Qt.AlignCenter)
        self.WT_sum.setObjectName("WT_sum")

        self.WT_Average = QtWidgets.QLabel(self.Group_AWT_table)
        self.WT_Average.setFont(font)
        self.WT_Average.setStyleSheet("color: #FFFFFF")
        if not (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            W_average = sum(self.Waiting_Time)/len(self.PROCESS)
            print(W_average)
            if len(str(W_average).split('.')[1]) == 1 and str(W_average).split('.')[1] == '0':
                self.WT_Average.setText(f"Average:\n{int(W_average)}")
            else:
                W_averagex = '{:.2f}'.format(W_average)
                self.WT_Average.setText(f"Average:\n{W_averagex} ≈ {fcn.xround(W_average)}")
        else:
            W_average = self.W_sum/len(self.PROCESS)
            print(W_average)
            if len(str(W_average).split('.')[1]) == 1 and str(W_average).split('.')[1] == '0':
                self.WT_Average.setText(f"Average:\n{int(W_average)}")
            else:
                W_averagex = '{:.2f}'.format(W_average)
                self.WT_Average.setText(f"Average:\n{W_averagex} ≈ {fcn.xround(W_average)}")

        self.WT_Average.adjustSize()
        self.WT_Average.setGeometry(QtCore.QRect(((451) - (self.WT_Average.width())) - 40, 340, self.WT_Average.width(), self.WT_Average.height()))
        self.WT_Average.setAlignment(QtCore.Qt.AlignCenter)
        self.WT_Average.setObjectName("WT_Average")

        #######
        self.Group_Util = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_Util.setGeometry(QtCore.QRect( (width//2) - (w//2), y+450, w, h-250))
        self.Group_Util.setStyleSheet('QGroupBox:title {color: rgb(51, 90, 187);}')
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Group_Util.setFont(font)
        self.Group_Util.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_Util.setTitle('CPU Utilization')
        self.Group_Util.setCheckable(False)
        self.Group_Util.setChecked(False)
        self.Group_Util.setObjectName("Group_Util")

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)

        CPU_Util = '{:.2f}'.format(self.CPU_Utilization)
        self.C_Util = QtWidgets.QLabel(self.Group_Util)
        self.C_Util.setFont(font)
        self.C_Util.setStyleSheet("color: #FFFFFF")
        self.C_Util.setText(f"CPU Utilization = [1 - (Idle time / Completion time)] * 100\n= [1 - ({self.idle_sum} / {self.gantt_list[-1]})] * 100 \n\n= {CPU_Util}%")
        self.C_Util.adjustSize()
        self.C_Util.setGeometry(QtCore.QRect((self.Group_Util.width()//2) - (self.C_Util.width() // 2), 
                                ((self.Group_Util.height()//2) - (self.C_Util.height() // 2)) + 20, self.C_Util.width(), self.C_Util.height()))
        self.C_Util.setAlignment(QtCore.Qt.AlignCenter)
        self.C_Util.setObjectName("C_Util")

        self.show_ATA_table()
        self.show_AWT_table()

        # this will hide the title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # setting  the geometry of window
        self.setGeometry(100, 100, 400, 300)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.showFullScreen()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.9)
        painter.setBrush(QtCore.Qt.black)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))   
        painter.drawRect(self.rect())
    
    def sort_by_process(self, process, x, arrival):
        for i in range(len(process)-1):
            for j in range(0, len(process)-i-1):
                if int(re.search('P(.*)', process[j]).group(1)) > int(re.search('P(.*)', process[j+1]).group(1)):
                    process[j], process[j+1] = process[j+1], process[j]
                    x[j], x[j+1] = x[j+1], x[j]
                    arrival[j], arrival[j+1] = arrival[j+1], arrival[j]
        return [process, x, arrival]
    
    def show_ATA_table(self):
        self.ATA_Table.setRowCount(len(self.ARRIVAL))
        if not (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            for row in range(len(self.ARRIVAL)):
                self.ATA_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(self.xATA[0][row])))
                self.ATA_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.xATA[1][row])))
                self.ATA_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(self.xATA[2][row])))
                self.ATA_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.Turnaround_Time[row])))
        else:
            Finish = fcn.sort_by_process(self.Finish)
            for i in Finish:
                Finish[i] = sorted(Finish[i], reverse=True)
            Finish_key = list(Finish.keys())
            Finish_val = list(Finish.values())
            print(Finish_val, 'sd')
            for row in range(len(self.ARRIVAL)):
                self.ATA_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(Finish_key[row])))
                self.ATA_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(Finish_val[row][0])))
                self.ATA_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(Finish_val[row][1])))
                self.ATA_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(Finish_val[row][0] - Finish_val[row][1])))
    
    def show_AWT_table(self):
        self.AWT_Table.setRowCount(len(self.ARRIVAL))
        if not (pick == 'priority_p' or pick == 'srtf' or pick == 'rr'):
            for row in range(len(self.ARRIVAL)):
                self.AWT_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(self.xAWT[0][row])))
                self.AWT_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.xAWT[1][row])))
                self.AWT_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(self.xAWT[2][row])))
                self.AWT_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.Waiting_Time[row])))
        else:
            Start = fcn.sort_by_process(self.Start)
            for i in Start:
                Start[i] = sorted(Start[i], reverse=True)
            Start_key = list(Start.keys())
            Start_val = list(Start.values())
            print(Start_val, 'sd')
            for row in range(len(self.ARRIVAL)):
                self.AWT_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(Start_key[row])))
                if len(Start_val[row]) > 2:
                    self.AWT_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{Start_val[row][::2]}'))
                    self.AWT_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{Start_val[row][1::2]}'))
                else:
                    self.AWT_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(Start_val[row][0])))
                    self.AWT_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(Start_val[row][1])))
                self.AWT_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(sum(Start_val[row][::2]) - sum(Start_val[row][1::2]))))

class PM_TimeList:
    def __init__(self, MainWindow, gantt_list):
        self.MainWindow = MainWindow
        self.gantt_list = gantt_list
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Time List")
        MainWindow.setFixedSize(251, 170)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("Icons/clock.png")))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(resource_path("Icons/clock-history.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(91, 111, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("Icons/arrow-skip.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(True)
        # self.pushButton.clicked.connect(self.change_txt)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.comboBox.addItem(self.icon, f'Time 0')
        for time in self.gantt_list:
            if time == self.gantt_list[-1]:
                self.comboBox.addItem(self.icon, f'Time {time} (Finished)')
            else:
                self.comboBox.addItem(self.icon, f'Time {time}')



# ................Shared class...................
class AlignDelegate(QtWidgets.QStyledItemDelegate): # Table.cell.alignCenter 
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

class JobTableWindow:
    def __init__(self, Window):
        # super(SummaryTableWindow, self).__init__()
        Window.setObjectName("Window")
        Window.setWindowIcon(QtGui.QIcon(resource_path('Icons\checklist.png')))
        Window.setFixedSize(450, 200)
        Window.setWindowModality(QtCore.Qt.NonModal)
        self.centralwidget = QtWidgets.QWidget(Window)
        self.centralwidget.setObjectName("centralwidget")

        self.Job_Table = QtWidgets.QTableWidget(self.centralwidget)
        self.Job_Table.setGeometry(QtCore.QRect(10, 10, 432, 181))
        self.Job_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Job_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Job_Table.setFont(font)
        self.Job_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Job_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Job_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.Job_Table.verticalHeader().setVisible(False) # Row Index
        self.Job_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.Job_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        
        self.Job_Table.setAutoScroll(True)
        self.Job_Table.setAlternatingRowColors(True)
        self.Job_Table.setObjectName("Job_Table")
        self.Job_Table.setColumnCount(4)
        self.Job_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(0, item)
        self.Job_Table.setItemDelegateForColumn(0, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(1, item)
        self.Job_Table.setItemDelegateForColumn(1, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(2, item)
        self.Job_Table.setItemDelegateForColumn(2, AlignDelegate(self.Job_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Job_Table.setHorizontalHeaderItem(3, item)
        self.Job_Table.setItemDelegateForColumn(3, AlignDelegate(self.Job_Table))
        self.Job_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.Job_Table.horizontalHeaderItem(0).setFont(font)
        self.Job_Table.horizontalHeaderItem(1).setFont(font)
        self.Job_Table.horizontalHeaderItem(2).setFont(font)
        self.Job_Table.horizontalHeaderItem(3).setFont(font)
             
        self.Job_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.Job_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        Window.setCentralWidget(self.centralwidget)
        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

        self.job_table()
    
    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Job Table"))
        item = self.Job_Table.horizontalHeaderItem(0)
        item.setText(_translate("Window", "Job"))
        item = self.Job_Table.horizontalHeaderItem(1)
        item.setText(_translate("Window", "Size"))
        item = self.Job_Table.horizontalHeaderItem(2)
        item.setText(_translate("Window", "Arrival time"))
        item = self.Job_Table.horizontalHeaderItem(3)
        item.setText(_translate("Window", "Run time"))
    
    def job_table(self):
        global D
        job_size = D['Size']
        arrival_time = D['Arrival time']
        run_time = D['Run time']
        self.Job_Table.clearContents()
        self.Job_Table.setRowCount(len(arrival_time))
        for row in range(len(arrival_time)):
            self.Job_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
            self.Job_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(job_size[row])))
            self.Job_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(arrival_time[row])))
            self.Job_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(run_time[row])))

class SummaryTableWindow(QtWidgets.QMainWindow):
    def __init__(self, D):
        super().__init__()
        self.start_time, self.finish, self.cpu_wait = D[0], D[1], D[2]
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        w = 451
        h = 340
        x = 500-w-((500-w)//2)
        y = 390-291-((390-291)//2)
        self.Group_job_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_job_table.setGeometry(QtCore.QRect(x, y, w, h))
        self.Group_job_table.setStyleSheet('QGroupBox:title {color: rgb(231, 118, 108);}')
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Group_job_table.setFont(font)
        self.Group_job_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_job_table.setTitle('Summary Table')
        self.Group_job_table.setCheckable(False)
        self.Group_job_table.setChecked(False)
        self.Group_job_table.setObjectName("Group_job_table")

        qr = self.Group_job_table.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.Group_job_table.move(qr.topLeft())

        self.close_btn = QtWidgets.QPushButton(self.Group_job_table)
        self.close_btn.setText("x")
        self.close_btn.setGeometry(QtCore.QRect(451-28, 35 , 0, 0))
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet("color: white; border: 0px")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.hide)

        self.Summary_Table = QtWidgets.QTableWidget(self.Group_job_table)
        self.Summary_Table.setGeometry(QtCore.QRect(10, 76, 432, 251))
        self.Summary_Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Summary_Table.horizontalHeader().setSortIndicatorShown(False)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Summary_Table.setFont(font)
        self.Summary_Table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Summary_Table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Summary_Table.verticalHeader().setVisible(False) # Row Index
        self.Summary_Table.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.Summary_Table.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid #E74C3C;}')
        
        self.Summary_Table.setAutoScroll(True)
        self.Summary_Table.setAlternatingRowColors(True)
        self.Summary_Table.setObjectName("Summary_Table")
        self.Summary_Table.setColumnCount(4)
        self.Summary_Table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Summary_Table.setHorizontalHeaderItem(0, item)
        self.Summary_Table.setItemDelegateForColumn(0, AlignDelegate(self.Summary_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Summary_Table.setHorizontalHeaderItem(1, item)
        self.Summary_Table.setItemDelegateForColumn(1, AlignDelegate(self.Summary_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Summary_Table.setHorizontalHeaderItem(2, item)
        self.Summary_Table.setItemDelegateForColumn(2, AlignDelegate(self.Summary_Table))
        item = QtWidgets.QTableWidgetItem()
        self.Summary_Table.setHorizontalHeaderItem(3, item)
        self.Summary_Table.setItemDelegateForColumn(3, AlignDelegate(self.Summary_Table))
        self.Summary_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(90)
        self.Summary_Table.horizontalHeaderItem(0).setText("Job")
        self.Summary_Table.horizontalHeaderItem(1).setText("Start")
        self.Summary_Table.horizontalHeaderItem(2).setText("Finish")
        self.Summary_Table.horizontalHeaderItem(3).setText("CPU Wait")

        self.Summary_Table.horizontalHeaderItem(0).setFont(font)
        self.Summary_Table.horizontalHeaderItem(1).setFont(font)
        self.Summary_Table.horizontalHeaderItem(2).setFont(font)
        self.Summary_Table.horizontalHeaderItem(3).setFont(font)
             
        self.Summary_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.Summary_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.Summary_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.Summary_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.Summary_Table.verticalHeader().setDefaultSectionSize(44)

        self.show_summary_table()

        # this will hide the title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # setting  the geometry of window
        self.setGeometry(100, 100, 400, 300)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.showFullScreen()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.7)
        painter.setBrush(QtCore.Qt.black)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))   
        painter.drawRect(self.rect())
    
    def show_summary_table(self):
        self.Summary_Table.setRowCount(len(self.start_time))
        for row in range(len(self.start_time)):
            self.Summary_Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
            self.Summary_Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.start_time[row])))
            self.Summary_Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(self.finish[row])))
            self.Summary_Table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(self.cpu_wait[row])))


# Customed QMainWindow:
    # closeEvent
class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self,event):
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        
        notify_user = QtWidgets.QMessageBox()
        notify_user.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        notify_user.setDefaultButton(QtWidgets.QMessageBox.No)
        notify_user.setIcon(QtWidgets.QMessageBox.Question)
        notify_user.setFont(font)
        notify_user.setText('Are you sure you want to quit?      ')
        notify_user.setWindowTitle("Notify")
        event.ignore()

        if notify_user.exec_() == QtWidgets.QMessageBox.Yes:
            event.accept()


if __name__ == "__main__":
    suppress_qt_warnings()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(Style)
    MainWindow = MyWindow()
    ui = UI_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

