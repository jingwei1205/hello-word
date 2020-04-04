#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/4/3 12:44
# @Author : jingwei
# @Site : 
# @File : join_file_thread.py
# @Software: PyCharm
import os
import time

from PyQt5 import QtCore

import read_chapter_file as reader


class join_file_thread(QtCore.QThread):
    """连接单词文件，组成全单词模式"""
    # 声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(list)

    # 构造函数里增加形参
    def __init__(self, t, parent=None):
        super(join_file_thread, self).__init__(parent)
        self.t = t
        # 储存参数

    # 重写 run() 函数，在里面干大事。
    def run(self):
        dir_dictionary = {"cet4": "cet4",
                          "cet6": "cet6",
                          "study": "study"
                          }
        try:
            reader.join_each_file(dir_dictionary, self.t)
        except:
            print("文件合成失败")
        # 大事干完了，发送一个信号告诉主线程窗口
        self.finishSignal.emit(["文件合成状态正常！您可以进行整书自测！"])