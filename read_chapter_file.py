#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/3/29 15:48
# @Author : jingwei
# @Site : https://github.com/jingwei1205
# @File : read_chapter_file.py
# @Software: PyCharm

import os
import string


def read_chapter_file_by_chapter(file_id):
    # 对传入的名字进行首位去空位符操作
    file_id = file_id.strip()
    # 分开目录以及文件名称
    classify, name = file_id.split("_")
    # 储存单词列表
    words = []
    # 储存多重意思的中文列表
    chinese = []
    # 储存所有单词的意思
    final_chinese = []
    # 储存所有行的列表
    wrong_words_line = []
    # 打开相应文件
    file = open(classify + "/" + name + ".txt", "r", encoding="utf-8")
    # 读入文本第一行
    line = file.readline()
    # 循环读行 跳过空行
    while line and line != "":
        wrong_words_line.append(line)
        a, b = line.split("@")
        words.append(a)
        chinese.append(b)
        line = file.readline()
    # 关闭文件
    file.close()
    for tran in chinese:
        divide_chinese = tran.split("*")
        final_chinese.append(divide_chinese)
    return words, final_chinese, wrong_words_line


def write_wrong_words(file_id, wrong_words_line):
    wrong_dir_file, wrong_dir = handle_file_dir(file_id)
    if not os.path.exists(wrong_dir):
        os.mkdir(wrong_dir)
    if not os.path.exists(wrong_dir_file):
        wrong_file = open(wrong_dir_file, "w", encoding="utf-8")
        wrong_file.close()
    check_wrong_file = open(wrong_dir_file, "r", encoding="utf-8")
    line = check_wrong_file.readline()
    while line and line != "":
        if wrong_words_line == line:
            check_wrong_file.close()
            return
        line = check_wrong_file.readline()
    check_wrong_file.close()
    wrong_file = open(wrong_dir_file, "a+", encoding="utf-8")
    wrong_file.write(wrong_words_line)
    wrong_file.close()


def count_wrong_num(file_id):
    wrong_count = 0
    wrong_dir_file = handle_file_dir(file_id)[0]
    if os.path.exists(wrong_dir_file):
        check_wrong_file = open(wrong_dir_file, "r", encoding="utf-8")
        line = check_wrong_file.readline()
        while line and line != "":
            wrong_count += 1
            line = check_wrong_file.readline()
        check_wrong_file.close()
    return wrong_count


def handle_file_dir(file_id):
    file_id = file_id.strip()
    dir_head = file_id.split("_")[0]
    wrong_dir = dir_head + "wrong"
    wrong_file_name = wrong_dir + ".txt"
    wrong_dir_file = wrong_dir + "/" + wrong_file_name
    return wrong_dir_file, wrong_dir


def delete_from_file(file_id, chosen_line):
    file_id = file_id.strip()
    classify, name = file_id.split("_")
    wrong_dir_file = classify + "/" + name + ".txt"
    check_wrong_file = open(wrong_dir_file, "r", encoding="utf-8")
    line = check_wrong_file.readline()
    lines = []
    while line and line != "":
        if chosen_line == line:
            line = check_wrong_file.readline()
            print("找到啦！")
            continue
        lines.append(line)
        line = check_wrong_file.readline()
    check_wrong_file.close()
    wrong_file = open(wrong_dir_file, "w", encoding="utf-8")
    wrong_file.writelines(lines)
    wrong_file.close()


def join_each_file(dir_dictionary, mode):
    file_now_num = 0
    dir_now_num = 0
    for key in dir_dictionary:
        dir_now_num += 1
        now_dir = dir_dictionary[key] + "/"
        now_file_dir = now_dir + "/all.txt"
        file_num = len(os.listdir(now_dir))
        dir_num = len(dir_dictionary)
        if file_num == 0:
            continue
        if mode == "init":
            if os.path.exists(now_file_dir):
                global check_file
                check_file = "exist"
            else:
                write_in_all(now_file_dir, now_dir, file_now_num, file_num)
        if mode == "redone":
            write_in_all(now_file_dir, now_dir, file_now_num, file_num)


def write_in_all(now_file_dir, now_dir, file_now_num, file_num):
    all_file = open(now_file_dir, "w", encoding="utf-8")
    all_file.close()
    all_file = open(now_file_dir, "a+", encoding="utf-8")
    for file in os.listdir(now_dir):
        lines = []
        file_now_num += 1
        file = now_dir + file
        opened_file = open(file, "r", encoding="utf-8")
        line = opened_file.readline()
        while line:
            lines.append(line)
            line = opened_file.readline()
        all_file.writelines(lines)
        opened_file.close()
    all_file.close()


# 装饰者模式实现静态变量的方法
# def static_vars(**kwargs):
#     def decorate(func):
#         for k in kwargs:
#             setattr(func, k, kwargs[k])
#         return func
#     return decorate
#
#
# @static_vars(line2="", line3="")
# def foo(line2, line3, mode):
#     if mode == "use":
#         return foo.line2, foo.line3
#     foo.line2 = line2
#     foo.line3 = line3

def write_log(mode, class_id, rest_list):
    if not os.path.exists("log"):
        os.mkdir("log")
    rest_string = ""
    for rest in rest_list:
        rest_string += str(rest) + "@"
    print(mode)
    print(class_id)
    file = open("log/" + class_id.split("_")[0] + mode + ".txt", "w", encoding="utf-8")
    file.write(rest_string)
    file.close()


def read_log(mode, class_id):
    print("log/" + class_id + mode + ".txt")
    file = open("log/" + class_id + mode + ".txt", "r", encoding="utf-8")
    rest_list = file.read()
    file.close()
    rest_list = rest_list.split("@")
    get_list = []
    print(rest_list)
    for rest in rest_list:
        print(rest)
        if rest == "":
            continue
        get_list.append(int(rest))
    return get_list
