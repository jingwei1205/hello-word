##!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 15:44
# @Author  : jingwei
# @FileName: main_window.py
# @Software: PyCharm
# @Blog    ：https://www.cnblogs.com/Jewish/

import random
import threading
from decimal import Decimal

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys
import qtawesome
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QLabel, QScrollArea, QWidget, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QMessageBox
import read_chapter_file as reader
import os
from join_file_thread import join_file_thread, open_url_thread, read_file_thread
import send_mail


# 声明主窗口类


class MainUi(QtWidgets.QMainWindow):
    # 构造函数，初始化窗口
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cet4_wrong_num = 0
        self.cet6_wrong_num = 0
        self.study_wrong_num = 0
        self.word = []
        self.chines = []
        self.wrong_words_line = []
        self.terminal_visible = False
        self.terminal_line_1 = ""
        self.terminal_line_2 = ""
        self.terminal_line_3 = ""
        self.study_mode_dictionary = {
            "read": "阅读\t模式",
            "cn_to_en": "默单词\t模式",
            "en_to_cn": "背中文\t模式"
        }
        self.delete_old_study_mode = ""

    # 初始化窗口
    def init_ui(self):
        # 储存未被获取的单词序号 0到个数-1
        self.random_num = []
        # 单词总个数
        self.random_len = 0
        # 中文解释合成的字符串
        self.join_explain = ""
        # 剩余单词个数
        self.changeLen = 0
        # 储存完成百分比
        self.already = 0
        # 是否完成一轮的标志
        self.window_flag = False
        # 储存目前的文件名
        self.class_final_id = ""
        # 判断是否隐藏的标志
        self.hide_flag = False
        # 判断是否能够使用enter键操作
        self.enter_use = False
        # 储存错误的个数
        self.check_wrong = 0
        # 储存正确的个数
        self.check_right = 0
        # 当前全局模式 默认为read模式
        self.now_mode = "read"
        # 旧的全局模式 默认为read模式
        self.old_mode = "read"
        # 旧的文件名称
        self.old_class_id = ""
        # 当前被选中的行
        self.chosen_lines = ""
        # 当前是否为错词模式
        self.wrong_word_mode = False

        # 设置主窗口固定大小
        self.setFixedSize(960, 700)
        # 创建窗口主部件
        self.main_widget = QtWidgets.QWidget()
        # 创建主部件的网格布局
        self.main_layout = QtWidgets.QGridLayout()
        # 设置窗口主部件布局为网格布局
        self.main_widget.setLayout(self.main_layout)

        # 创建左侧部件
        self.left_widget = QtWidgets.QWidget()
        # 创建左侧部件的网格布局层
        self.left_widget.setObjectName('left_widget')
        # 设置左侧部件布局为网格
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        # 创建右侧部件
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName('right_widget')
        # 设置右侧部件布局为网格
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        # 左侧部件在第1行第1列，占12行2列
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)
        # 右侧部件在第1行第3列，占12行10列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 15)
        # 设置窗口主部件
        self.setCentralWidget(self.main_widget)

        # 关闭按钮
        self.left_close = QtWidgets.QPushButton("")
        # 空白按钮
        self.left_visit = QtWidgets.QPushButton("")
        # 最小化按钮
        self.left_mini = QtWidgets.QPushButton("")

        # 设置菜单大类名称，设置名称为左面板
        self.left_label_1 = QtWidgets.QPushButton("词汇自测")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("错词集")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("版本与说明")
        self.left_label_3.setObjectName('left_label')

        # 设置菜单小类按钮，命名为左按钮
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.paw', color='white'), "四级词汇")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.book', color='white'), "六级词汇")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.graduation-cap', color='white'), "考研词汇")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.edit', color='white'), "四级错词册")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.history', color='white'), "六级错词册")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.leaf', color='white'), "考研错词册")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关于软件")
        self.left_button_8.setObjectName('left_button')

        # 将按钮放置到左面板布局
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)

        # 右面版加入右面布局
        self.right_label = QLabel(self)
        self.right_layout.addWidget(self.right_label)
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
                border-image: url('images/welcome.jpg');
            }
        ''')
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;}
        ''')

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

        # 设置关闭， 最小化按钮监听
        self.left_close.clicked.connect(QCoreApplication.instance().quit)
        self.left_mini.clicked.connect(self.showMinimized)

        # 设置单词自测部分跳转对应页面的按钮监听
        self.left_button_1.clicked.connect(
            lambda: self.word_page("新东方四级词汇（乱序版）", 35, 'images/cet4.png', "cet4_", self.left_button_1.text()))
        self.left_button_2.clicked.connect(
            lambda: self.word_page("新东方六级词汇（乱序版）", 30, 'images/cet6.png', "cet6_", self.left_button_2.text()))
        self.left_button_3.clicked.connect(
            lambda: self.word_page("新东方考研词汇（正序版）", 50, 'images/study.png', "study_", self.left_button_3.text()))

        self.left_button_4.clicked.connect(lambda: self.wrong_handle("cet4_wrong"))
        self.left_button_5.clicked.connect(lambda: self.wrong_handle("cet6_wrong"))
        self.left_button_6.clicked.connect(lambda: self.wrong_handle("study_wrong"))

        self.left_button_7.clicked.connect(self.send_mail_to_me)
        self.left_button_8.clicked.connect(self.open_about)

    def open_about(self):
        threading.Thread(target=os.system, args=("AboutSoftware\\index.html",)).start()

    # 以下三个函数设置拖动窗口
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.Qt.LeftButton:
            self.flag = True
            self.m_Position = QMouseEvent.globalPos() - self.pos()
            QMouseEvent.accept()
            self.setCursor(Qt.QCursor(Qt.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.Qt.LeftButton and self.flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.flag = False
        self.setCursor(Qt.QCursor(Qt.Qt.ArrowCursor))

    # 选择章节界面
    def word_page(self, book_name, list_num, book_img, class_id, button_text):
        # 清空组件
        self.clean_right_layout()
        self.back_to_right_original_label()
        self.wrong_word_mode = False
        self.enter_use = False

        # 采用书籍
        self.right_recommend_label = QtWidgets.QLabel("Books 采用书籍")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget()  # 封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout()  # 封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        # 第一本书籍
        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText(book_name)  # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon(book_img))  # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(100, 100))  # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文

        # 第二本书籍
        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("更多词汇书籍敬请期待……")
        self.recommend_button_2.setIcon(QtGui.QIcon('images/soon.png'))
        self.recommend_button_2.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        # 将两本书籍加入介绍网格布局
        self.right_recommend_layout.addWidget(self.recommend_button_1, 0, 0, 1, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_2, 0, 1, 1, 3)

        # 将介绍标签以及介绍组件加入右面板网格布局
        self.right_layout.addWidget(self.right_recommend_label, 0, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 1, 0, 2, 9)

        # 目录和更多操作
        self.right_newsong_lable = QtWidgets.QLabel("Contents 目录")
        self.right_newsong_lable.setObjectName('right_lable')

        self.right_playlist_lable = QtWidgets.QLabel("More 更多操作")
        self.right_playlist_lable.setObjectName('right_lable')

        self.right_newsong_widget = QtWidgets.QWidget()  # 最新歌曲部件
        self.right_newsong_layout = QtWidgets.QGridLayout()  # 最新歌曲部件网格布局
        self.right_newsong_widget.setLayout(self.right_newsong_layout)

        # 创建新的窗口类 并且设置大小
        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setMinimumSize(250, list_num * 40)

        # 声明章节按钮列表
        self.bt_list = []
        # 生成章节按钮
        for filename in range(list_num):
            MapButton = QtWidgets.QPushButton(self.topFiller)
            MapButton.setText("Word List " + str(filename + 1) + " ")
            MapButton.move(10, filename * 40)
            self.bt_list.append(MapButton)

        # 以全局模式的参数设置章节按钮的监听方法
        for i in range(len(self.bt_list)):
            self.bt_list[i].clicked.connect(
                lambda: self.start_chapter_show(class_id + self.sender().text(), self.now_mode, self.sender().text()))

        # 创建一个滚动条
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)
        self.right_newsong_layout.addWidget(self.scroll)

        # 右下方按钮集合
        self.right_playlist_widget = QtWidgets.QWidget()
        self.right_playlist_layout = QtWidgets.QGridLayout()
        self.right_playlist_widget.setLayout(self.right_playlist_layout)

        self.playlist_button_1 = QtWidgets.QToolButton()
        self.playlist_button_1.setText("整书自测")
        self.playlist_button_1.setIcon(QtGui.QIcon('images/book.png'))
        self.playlist_button_1.setIconSize(QtCore.QSize(100, 100))
        self.playlist_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.playlist_button_2 = QtWidgets.QToolButton()
        self.playlist_button_2.setText("继续上次(仅限整书自测）")
        self.playlist_button_2.setIcon(QtGui.QIcon('images/fight.png'))
        self.playlist_button_2.setIconSize(QtCore.QSize(100, 100))
        self.playlist_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.playlist_button_3 = QtWidgets.QToolButton()
        self.playlist_button_3.setText("单元自测请点击目录中按钮")
        self.playlist_button_3.setIcon(QtGui.QIcon('images/unit.png'))
        self.playlist_button_3.setIconSize(QtCore.QSize(100, 100))
        self.playlist_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.playlist_button_4 = QtWidgets.QToolButton()
        self.playlist_button_4.setText("退出")
        self.playlist_button_4.setIcon(QtGui.QIcon('images/exit.png'))
        self.playlist_button_4.setIconSize(QtCore.QSize(100, 100))
        self.playlist_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        # 按钮加入布局
        self.right_playlist_layout.addWidget(self.playlist_button_1, 0, 0)
        self.right_playlist_layout.addWidget(self.playlist_button_2, 0, 1)
        self.right_playlist_layout.addWidget(self.playlist_button_3, 1, 0)
        self.right_playlist_layout.addWidget(self.playlist_button_4, 1, 1)
        self.right_layout.addWidget(self.right_newsong_lable, 4, 0, 1, 5)
        self.right_layout.addWidget(self.right_playlist_lable, 4, 5, 1, 4)
        self.right_layout.addWidget(self.right_newsong_widget, 5, 0, 1, 5)
        self.right_layout.addWidget(self.right_playlist_widget, 5, 5, 1, 4)

        self.terminal_tip()
        self.hide_terminal("no-change")
        self.terminal_line_1 = button_text
        self.show_terminal()

        # 设置按钮监听
        self.playlist_button_4.clicked.connect(self.init_ui)
        self.playlist_button_1.clicked.connect(self.muti_thread)

        # 设置样式
        self.right_recommend_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')
        self.right_playlist_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')
        self.topFiller.setStyleSheet('''
            QPushButton{
                border:none;
                color:gray;
                font-size:12px;
                height:40px;
                padding-left:5px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')

    # 清空组件
    def clean_right_layout(self):
        for i in range(self.right_layout.count()):
            self.right_layout.itemAt(i).widget().deleteLater()

    # 章节单词页面
    def start_chapter_show(self, class_id, mode, button_name):
        # 给当前文件名赋值
        self.class_final_id = class_id
        # 激活enter键
        self.enter_use = True
        # 设置全局文件id为当前文件id
        self.class_final_id = class_id
        # 清空当前组件
        self.clean_right_layout()

        # 单词进度条
        self.right_process_bar = QtWidgets.QProgressBar()
        # 设置进度为当前全局进度变量，默认为0
        self.right_process_bar.setValue(self.already)
        # 设置进度条高度
        self.right_process_bar.setFixedHeight(4)
        # 不显示进度条文字
        self.right_process_bar.setTextVisible(False)

        # 播放控制部件
        self.right_playconsole_widget = QtWidgets.QWidget()
        # 播放控制部件网格布局层
        self.right_playconsole_layout = QtWidgets.QGridLayout()
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        # 最底排按钮
        self.words_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.language', color='#6698cb'), "背中文\t")
        self.words_button_1.setObjectName('word_button')
        self.words_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.language', color='#F76677'), "默英文\t")
        self.words_button_2.setObjectName('word_button')
        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#1f9baa'), "Next\t")
        self.console_button_2.setObjectName('word_button')
        self.process_info_label1 = QtWidgets.QPushButton(qtawesome.icon('fa.check', color='#82c8a0'), "")
        self.process_info_label1.setObjectName('word_button')
        self.process_info_label2 = QtWidgets.QPushButton(qtawesome.icon('fa.remove', color='#fa5a5a'), "")
        self.process_info_label2.setObjectName('word_button')
        self.process_info_label3 = QtWidgets.QPushButton(qtawesome.icon('fa.refresh', color='grey'),
                                                         str(self.already) + "%\t")
        self.process_info_label3.setObjectName('word_button')
        self.process_info_label4 = QtWidgets.QPushButton(qtawesome.icon('fa.search', color='#cb99c5'),
                                                         str(self.random_len) + "\t")
        self.process_info_label4.setObjectName('word_button')
        self.process_info_label5 = QtWidgets.QPushButton(qtawesome.icon('fa.wrench', color='#7fccde'),
                                                         str(self.changeLen) + "\t")
        self.process_info_label5.setObjectName('word_button')
        self.process_info_label6 = QtWidgets.QPushButton(qtawesome.icon('fa.book', color='#7fccde'),
                                                         "Read\t")
        self.process_info_label6.setObjectName('word_button')

        # 设置图标大小
        self.console_button_2.setIconSize(QtCore.QSize(30, 30))
        self.words_button_1.setIconSize(QtCore.QSize(30, 30))
        self.words_button_2.setIconSize(QtCore.QSize(30, 30))
        self.process_info_label1.setIconSize(QtCore.QSize(30, 30))
        self.process_info_label2.setIconSize(QtCore.QSize(30, 30))
        self.process_info_label3.setIconSize(QtCore.QSize(30, 30))
        self.process_info_label4.setIconSize(QtCore.QSize(30, 30))
        self.process_info_label5.setIconSize(QtCore.QSize(30, 30))
        self.process_info_label6.setIconSize(QtCore.QSize(30, 30))

        self.terminal_tip()
        self.hide_terminal("no-change")
        # 加入布局
        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 8)
        self.right_playconsole_layout.addWidget(self.words_button_1, 0, 7)
        self.right_playconsole_layout.addWidget(self.words_button_2, 0, 6)
        self.right_playconsole_layout.addWidget(self.process_info_label1, 0, 3)
        self.right_playconsole_layout.addWidget(self.process_info_label2, 0, 4)
        self.right_playconsole_layout.addWidget(self.process_info_label3, 0, 2)
        self.right_playconsole_layout.addWidget(self.process_info_label5, 0, 1)
        self.right_playconsole_layout.addWidget(self.process_info_label4, 0, 0)
        self.right_playconsole_layout.addWidget(self.process_info_label6, 0, 5)
        self.right_playconsole_layout.addWidget(self.terminal_tip_button_2, 0, 9)
        self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignBottom)  # 设置布局内部件居右显示
        self.right_layout.addWidget(self.right_process_bar, 9, 0, 1, 9)
        self.right_layout.addWidget(self.right_playconsole_widget, 10, 0, 1, 9)

        if self.delete_old_study_mode != "":
            self.terminal_line_1 = self.terminal_line_1.replace(self.delete_old_study_mode, "")
        if button_name.strip() in ["Read", "默英文", "背中文"]:
            self.terminal_line_1 += self.study_mode_dictionary[mode]
            self.delete_old_study_mode = self.study_mode_dictionary[mode]
        else:
            self.terminal_line_1 += "\t" + button_name.strip() + "\t" + self.study_mode_dictionary[mode]
            self.delete_old_study_mode = self.study_mode_dictionary[mode]
        self.terminal_line_2 = self.terminal_line_3
        self.terminal_line_3 = "模式切换成功"
        self.show_terminal()

        # 设置button格式
        self.right_playconsole_widget.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        # 检查文件是否变化
        self.check_file_change()

        # 划分区域块
        self.right_newsong_lable = QtWidgets.QLabel("英文单词")
        self.right_newsong_lable.setObjectName('word_test')
        self.right_newsong_lable.setAlignment(QtCore.Qt.AlignCenter)

        self.right_playlist_lable = QtWidgets.QLabel("中文释义")
        self.right_playlist_lable.setObjectName('word_test')
        self.right_playlist_lable.setAlignment(QtCore.Qt.AlignCenter)

        self.right_layout.addWidget(self.right_newsong_lable, 0, 0, 1, 4)
        self.right_layout.addWidget(self.right_playlist_lable, 0, 5, 1, 4)

        self.words_label1 = QtWidgets.QLabel("Hello!")
        self.words_label1.setObjectName('word_en')

        self.right_layout.addWidget(self.words_label1, 0, 0, 8, 4)
        self.words_label1.setAlignment(QtCore.Qt.AlignCenter)

        self.words_label2 = QtWidgets.QLabel("你好呀！")
        self.join_explain = ""
        self.words_label2.setObjectName('word_cn')
        self.right_layout.addWidget(self.words_label2, 0, 5, 8, 4)
        self.words_label2.setAlignment(QtCore.Qt.AlignCenter)

        if mode == "cn_to_en":
            self.hide_flag = True
            self.words_label1.hide()
            self.input_words = QLineEdit()
            self.input_words.setPlaceholderText("输入答案，回车确定")
            self.input_words.setAlignment(QtCore.Qt.AlignCenter)
            self.right_layout.addWidget(self.input_words, 4, 0, 5, 3)
            self.input_words.setStyleSheet('''
                QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
                font-size:20px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                color:"grey";
                border:none;
                }
            ''')
        elif mode == "en_to_cn":
            self.words_label2.hide()

        self.console_button_2.clicked.connect(lambda: self.next_words(class_id))

        self.right_playconsole_widget.setStyleSheet('''
            QPushButton#word_button{
                border:none;
                font-size:14px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                color:"grey";                
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')
        self.words_button_2.clicked.connect(
            lambda: self.start_chapter_show(class_id, "cn_to_en", self.words_button_2.text()))
        self.words_button_2.clicked.connect(self.cte_mode)
        self.process_info_label6.clicked.connect(
            lambda: self.start_chapter_show(class_id, "read", self.process_info_label6.text()))
        self.process_info_label6.clicked.connect(self.read_mode)
        self.words_button_1.clicked.connect(
            lambda: self.start_chapter_show(class_id, "en_to_cn", self.words_button_1.text()))
        self.words_button_1.clicked.connect(self.etc_mode)
        pass

    # 主页外所有界面terminal提示组件
    def terminal_tip(self):
        self.terminal_tip_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.code'), "")
        self.terminal_tip_button_1.setIconSize(QtCore.QSize(30, 30))
        self.terminal_tip_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.angle-up'), "")
        self.terminal_tip_button_2.setIconSize(QtCore.QSize(30, 30))

        self.right_layout.addWidget(self.terminal_tip_button_1, 11, 0, 1, 7)
        self.right_layout.addWidget(self.terminal_tip_button_2, 10, 8, 1, 1)

        self.terminal_tip_button_2.clicked.connect(lambda: self.hide_terminal("change"))
        self.terminal_tip_button_1.setStyleSheet('''
                    QPushButton{
                        border:none;
                        font-size:14px;
                        font-weight:500;
                        font-family: "宋体";
                        color:grey;
                        text-align:left;
                        border-radius:10px;
                    }
                ''')
        self.terminal_tip_button_2.setStyleSheet('''
            QPushButton{
                border:none;
                font-size:14px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                color:"grey";                
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')

    def hide_terminal(self, mode):
        if mode == "change":
            if self.terminal_visible == False:
                self.terminal_tip_button_1.hide()
                self.terminal_tip_button_2.setIcon(qtawesome.icon('fa.angle-down'))
                self.terminal_visible = True
            elif self.terminal_visible == True:
                self.terminal_tip_button_1.show()
                self.terminal_tip_button_2.setIcon(qtawesome.icon('fa.angle-up'))
                self.terminal_visible = False
        elif mode == "no-change":
            if self.terminal_visible == True:
                self.terminal_tip_button_1.hide()
                self.terminal_tip_button_2.setIcon(qtawesome.icon('fa.angle-down'))
            elif self.terminal_visible == False:
                self.terminal_tip_button_1.show()
                self.terminal_tip_button_2.setIcon(qtawesome.icon('fa.angle-up'))

    def show_terminal(self):
        self.terminal_tip_button_1.setText("状态:"
                                           + self.terminal_line_1 + "\n后台行 1："
                                           + self.terminal_line_2 + "\n后台行 2："
                                           + self.terminal_line_3)

    def muti_thread(self):
        # 把按钮禁用掉
        self.playlist_button_1.setDisabled(True)
        self.playlist_button_2.setDisabled(True)
        # 新建对象，传入参数
        self.bwThread = join_file_thread("init")
        # 连接子进程的信号和槽函数
        self.bwThread.finishSignal.connect(self.muti_thread_end)
        self.terminal_line_2 = "文件合并中……"
        self.terminal_line_3 = "请稍后……"
        self.show_terminal()
        # 开始执行 run() 函数里的内容
        self.bwThread.run()

    def muti_thread_end(self, ls):
        for word in ls:
            print(word)
            self.playlist_button_2.setDisabled(False)
            self.terminal_line_2 = self.terminal_line_3
            self.terminal_line_3 = word
            self.show_terminal()
            # 恢复按钮
        self.playlist_button_1.setDisabled(False)

    def cte_mode(self):
        self.now_mode = "cn_to_en"
        self.check_mode_change()
        self.hide_flag = True

    def read_mode(self):
        self.now_mode = "read"
        self.check_mode_change()
        self.hide_flag = False

    def etc_mode(self):
        self.now_mode = "en_to_cn"
        self.check_mode_change()
        self.hide_flag = True

    def check_mode_change(self):
        if self.now_mode != self.old_mode:
            self.init_value()
            self.old_mode = self.now_mode

    def check_file_change(self):
        if self.old_class_id == self.class_final_id:
            self.is_file_change = False
            return
        if self.old_class_id == "":
            self.old_class_id = self.class_final_id
            self.is_file_change = True
            return
        elif self.class_final_id != self.old_class_id:
            self.init_value()
            self.old_class_id = self.class_final_id
            self.is_file_change = True

    def chosen_words(self, class_id):
        if self.is_file_change == True:
            self.is_file_change = False
            try:
                thread = read_file_thread(class_id)
                self.words, self.chinese, self.wrong_words_line = thread.run()
                file_id = class_id.strip()
                # 分开目录以及文件名称
                classify, name = file_id.split("_")
                class_id = classify + "/" + name + ".txt"
                self.terminal_line_2 = self.terminal_line_3
                self.terminal_line_3 = "读取文件成功：" + os.path.abspath(class_id)
                self.show_terminal()
            except:
                QMessageBox.warning(self, '提示', '不好意思噢！文件打开失败！请检查程序完整性！', QMessageBox.Yes)
                return
        if len(self.random_num) == 0:
            self.random_num = list(range(0, len(self.words)))
            self.random_len = len(self.random_num)
        chosenNum = random.choice(self.random_num)
        chosenWords = self.words[chosenNum]
        self.chosen_lines = self.wrong_words_line[chosenNum]
        chosenExplain = self.chinese[chosenNum]
        for choice in chosenExplain:
            self.join_explain += choice + "\n"
        self.random_num.remove(chosenNum)
        self.changeLen = len(self.random_num)
        self.already = Decimal((self.random_len - self.changeLen) / self.random_len * 100).quantize(Decimal('0.00'))
        self.process_info_label3.setText(str(self.already) + "%\t\t")
        self.process_info_label4.setText(str(self.random_len) + "\t\t")
        self.process_info_label5.setText(str(self.changeLen) + "\t\t")
        self.right_process_bar.setValue(self.already)
        return chosenWords

    def next_words(self, class_id):
        self.terminal_line_2 = self.terminal_line_3
        if self.changeLen == 0:
            self.terminal_line_3 = "请稍后……"
        else:
            self.terminal_line_3 = "切换单词成功，剩余单词数量：" + str(self.changeLen - 1)
        self.show_terminal()
        chosenWords = self.chosen_words(class_id)
        self.words_label1.setText(chosenWords)
        self.words_label2.setText(self.join_explain)
        if self.hide_flag == True:
            if self.now_mode == "cn_to_en":
                self.words_label1.hide()
                self.input_words.setText("")
            elif self.now_mode == "en_to_cn":
                self.words_label2.hide()
        self.join_explain = ""
        if self.window_flag == True:
            self.terminal_line_2 = self.terminal_line_3
            self.terminal_line_3 = "恭喜您，完成！"
            self.show_terminal()
            self.init_ui()
            return
        if len(self.random_num) == 0:
            self.window_flag = True

    def keyPressEvent(self, event):
        key = str(event.key())
        # print("按下：" + key)
        if key == "16777220" and self.enter_use == True:
            if self.words_label1.isHidden():
                self.words_label1.show()
                self.check_answer()
                return
            elif self.words_label2.isHidden():
                self.words_label2.show()
                return
            self.next_words(self.class_final_id)

    def init_value(self):
        self.random_num = []
        self.random_len = 0
        self.join_explain = ""
        self.changeLen = 0
        self.already = 0
        self.window_flag = False
        # self.class_final_id = ""
        self.process_info_label3.setText("进度\t")
        self.process_info_label4.setText("总数\t")
        self.process_info_label5.setText("剩余个数\t")
        self.right_process_bar.setValue(0)
        self.check_wrong = 0
        self.check_right = 0
        self.is_file_change = True

    def check_answer(self):
        if self.words_label1.text().strip() == "Hello!":
            return
        if self.input_words.text().strip() == self.words_label1.text().strip():
            self.words_label1.setText(self.words_label1.text().strip() + "\n正确")
            self.check_right += 1
            self.process_info_label1.setText(str(self.check_right))
            if self.wrong_word_mode == True:
                self.random_len -= 1
                reader.delete_from_file(self.class_final_id, self.chosen_lines)
                self.terminal_line_2 = self.terminal_line_3
                self.terminal_line_3 = self.words_label1.text().replace("\n", "") + ":已自动移出错词本"
                self.show_terminal()
        else:
            self.words_label1.setText(self.words_label1.text().strip() + "\n错误")
            self.check_wrong += 1
            self.process_info_label2.setText(str(self.check_wrong))
            if self.wrong_word_mode == True:
                return
            reader.write_wrong_words(self.class_final_id, self.chosen_lines)
            self.terminal_line_2 = self.terminal_line_3
            self.terminal_line_3 = self.words_label1.text().replace("\n",
                                                                    "") + ":已自动加入错词本，您的输入为：" + self.input_words.text().strip()
            self.show_terminal()

    def wrong_handle(self, file_id):
        self.cet4_wrong_num = reader.count_wrong_num(file_id)
        if self.cet4_wrong_num == 0:
            switch = {
                "cet4": "四级",
                "cet6": "六级",
                "study": "考研"
            }
            now_class = switch.get(file_id.split("_")[0])
            QMessageBox.warning(self, '提示', '您好，' + now_class + '错词册目前还没有噢，赶快去自测吧！', QMessageBox.Yes)
            return
        else:
            self.wrong_word_mode = True
            file_new_id = "".join(file_id.split("_"))
            # 清空组件
            self.clean_right_layout()
            self.back_to_right_original_label()
            self.start_chapter_show(reader.handle_file_dir(file_id)[1] + "_" + file_new_id, self.now_mode, "错词本")

    def back_to_right_original_label(self):
        # 右边各种样式表
        self.right_widget.setStyleSheet('''
                                QWidget#right_widget{
                                    color:#232C51;
                                    background:white;
                                    border-top:1px solid darkGray;
                                    border-bottom:1px solid darkGray;
                                    border-right:1px solid darkGray;
                                    border-top-right-radius:10px;
                                    border-bottom-right-radius:10px;
                                }
                                QLabel#right_lable{
                                    border:none;
                                    font-size:16px;
                                    font-weight:700;
                                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                }
                                QLabel#word_test{
                                    border:none;
                                    font-size:30px;
                                    font-weight:700;
                                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                    color:"grey";
                                }
                                QLabel#word_en{
                                    border:none;
                                    font-size:30px;
                                    font-weight:700;
                                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                    color:"#F76677";
                                }
                                QLabel#word_cn{
                                    border:none;
                                    font-size:16px;
                                    font-weight:700;
                                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                    color:"grey";
                                }
                                QProgressBar::chunk {
                                border: none;
                                background: rgb(0, 160, 230);
                                }
                            ''')

    def send_mail_to_me(self):
        self.clean_right_layout()
        self.back_to_right_original_label()
        self.enter_use = False

        self.email_widget = QtWidgets.QWidget()
        self.email_layout = QtWidgets.QVBoxLayout()
        self.email_widget.setLayout(self.email_layout)

        self.contact_widget = QtWidgets.QWidget()
        self.contact_layout = QtWidgets.QVBoxLayout()
        self.contact_widget.setLayout(self.contact_layout)

        self.contact_us_label = QtWidgets.QLabel("感谢")
        self.contact_us_label.setObjectName("contact")

        self.contact_string = QtWidgets.QLabel('''首先，欢迎您支持本软件，在使用过程中如有bug反馈、寻求合作等问题欢迎您联系我！
                                               \n看到后将第一时间回复！软件为个人开发，仅作为免费开源的学习工具分享，不会用于
                                               \n商业用途，还请大家正规使用。谢谢大家的配合！也请大家大家关注我的个人公众号，
                                               \n会得到更多学习工具、大学课程学习内容、大作业等内容，如果想要支持苦逼的我，
                                               \n觉得文章工具不错的话，也可以进行打赏，不过不要花钱买这些免费的工具噢！
                                               ''')
        self.contact_string.setObjectName("more")

        self.claim_label = QtWidgets.QLabel("声明")
        self.claim_label.setObjectName("contact")

        self.claim_string = QtWidgets.QLabel("软件为个人享有著作权，但是免费开源分享给大家，还请大家勿用于商业行为，如果"
                                             "\n您消费得到此软件请告知于我。除此之外，软件中单词文本为个人参照手中单词书录"
                                             "\n入，如果您认为依旧侵权，也请联系，会与您及时友善地协商解决问题。")

        self.email_label_1 = QtWidgets.QLabel("火狐邮箱：jingwei.shi@foxmail.com")
        self.email_label_1.setObjectName("contact")

        self.email_label_2 = QtWidgets.QLabel("腾讯邮箱：1349281263@qq.com")
        self.email_label_2.setObjectName("contact")

        self.wechat_label = QtWidgets.QLabel("微信公众号：学生可能用得到")
        self.wechat_label.setObjectName("contact")

        self.wechat_code = QtWidgets.QLabel()
        wechat_jpg = QtGui.QPixmap("images/wechat.jpg")
        self.wechat_code.setPixmap(wechat_jpg)

        self.send_label = QtWidgets.QLabel('向我发送消息')
        self.send_label.setFont(qtawesome.font('fa', 16))
        self.send_label.setObjectName("contact")

        self.send_widget = QtWidgets.QWidget()
        self.send_layout = QtWidgets.QHBoxLayout()
        self.send_widget.setLayout(self.send_layout)

        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QHBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        self.your_mail = QtWidgets.QLabel("您的邮箱：")
        self.your_mail.setObjectName("prefab1")

        self.input_mail = QtWidgets.QLineEdit()
        self.input_mail.setPlaceholderText("为了您可以收到回复，请输入您的准确邮箱地址！")
        self.input_mail.setObjectName("prefab2")

        self.your_content = QtWidgets.QLabel("正文内容：")
        self.your_content.setObjectName("prefab1")

        self.input_content = QtWidgets.QTextEdit()
        self.input_content.setPlaceholderText("请输入您想说的话！")
        self.input_content.setObjectName("prefab2")

        self.send_layout.addWidget(self.your_mail)
        self.send_layout.addWidget(self.input_mail)

        self.content_layout.addWidget(self.your_content)
        self.content_layout.addWidget(self.input_content)

        self.district = QtWidgets.QLabel("所属地区：浦东 上海 中国\n\n")
        self.district.setObjectName("contact")

        self.website = QtWidgets.QPushButton(qtawesome.icon("fa.link", color="#463B34"), "官网链接：http://m250g10468.qicp"
                                                                                         ".vip\n/wordkiller/index.html "
                                                                                         "\n(如若失效请点击关于软件打开本地网页）")
        self.website.setIconSize(QtCore.QSize(30, 30))

        self.website_git = QtWidgets.QPushButton(qtawesome.icon("fa.github", color="#463B34"), "Github")
        self.website_git.setIconSize(QtCore.QSize(30, 30))

        self.send_button = QtWidgets.QPushButton(qtawesome.icon("fa.paper-plane", color="white"), "\n发送\n")
        self.send_button.setObjectName("loginBtn")

        self.version_code = QtWidgets.QPushButton(qtawesome.icon("fa.copyright"),
                                                  "史经伟. All rights reserved. 当前版本号：0.1.0.200406_alpha")
        self.setObjectName("version")
        self.version_code.setIconSize(QtCore.QSize(20, 20))

        self.email_layout.addWidget(self.contact_us_label)
        self.email_layout.addWidget(self.contact_string)
        self.email_layout.addWidget(self.claim_label)
        self.email_layout.addWidget(self.claim_string)
        self.email_layout.addWidget(self.send_label)
        self.email_layout.addWidget(self.send_widget)
        self.email_layout.addWidget(self.content_widget)

        self.contact_layout.addWidget(self.wechat_label)
        self.contact_layout.addWidget(self.wechat_code)
        self.contact_layout.addWidget(self.email_label_1)
        self.contact_layout.addWidget(self.email_label_2)
        self.contact_layout.addWidget(self.district)
        self.contact_layout.addWidget(self.website)
        self.contact_layout.addWidget(self.website_git)
        self.right_layout.addWidget(self.send_button, 5, 5, 3, 4)
        self.right_layout.addWidget(self.version_code, 8, 0, 3, 4)

        self.right_layout.addWidget(self.email_widget, 0, 0, 10, 4)
        self.right_layout.addWidget(self.contact_widget, 0, 5, 1, 4)

        self.email_widget.setStyleSheet('''
        QLabel#contact{
            border:none;
            font-size:16px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QLineEdit{
            border:1px solid gray;
            width:300px;
            border-radius:10px;
            padding:2px 4px;
            font-size:14px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QTextEdit{
            border:1px solid gray;
            width:300px;
            border-radius:10px;
            padding:2px 4px;
            font-size:14px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        ''')

        self.contact_widget.setStyleSheet('''
                QLabel#contact{
                    border:none;
                    font-size:16px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton{
                    border:none;
                    font-size:14px;
                    font-weight:500;
                    font-family: "宋体";
                    color:grey;
                    text-align:left;
                    border-radius:10px;
                }
                QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
                }
                ''')

        self.version_code.setStyleSheet('''
        QPushButton{
                    border:none;
                    font-size:12px;
                    font-weight:300;
                    font-family: "宋体";
                    text-align:left;
                    border-radius:10px;
                }
        ''')

        self.send_button.setStyleSheet('''
            QPushButton#loginBtn
            {
                color:white;
                background-color:rgb(14 , 150 , 254);
                border-radius:5px;
            }
             
            QPushButton#loginBtn:hover
            {
                color:white;
                background-color:rgb(44 , 137 , 255);
            }
             
            QPushButton#loginBtn:pressed
            {
                color:white;
                background-color:rgb(14 , 135 , 228);
                padding-left:3px;
                padding-top:3px;
            }
            ''')

        self.send_button.clicked.connect(self.send_mail)
        self.website_git.clicked.connect(lambda: self.web_site_thread('https://github.com/jingwei1205'))
        self.website.clicked.connect(lambda: self.web_site_thread('http://m250g10468.qicp.vip/wordkiller/index.html'))

    def send_mail(self):
        self.send_button.setText("发送中……请稍等……")
        if self.input_mail.text() == "" or self.input_content.toPlainText() == "":
            QMessageBox.warning(self, '提示', '您好,您的邮箱、发送信息不能为空噢！', QMessageBox.Yes)
            self.send_button.setText("\n发送\n")
            return
        if send_mail.do_send(self.input_mail.text(), self.input_content.toPlainText()):
            QMessageBox.warning(self, '感谢您的反馈', '您好,您的信息已经发送成功。', QMessageBox.Yes)
            self.send_button.setText("\n发送\n")
        else:
            QMessageBox.warning(self, '好像出问题了', '发送失败,可能原因为网络连接或服务器失效！', QMessageBox.Yes)
            self.send_button.setText("\n发送\n")

    def web_site_thread(self, t):
        thread = open_url_thread(t)
        thread.run()


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
