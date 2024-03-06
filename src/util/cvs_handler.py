#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv

class CsvHandler:

  """
  将制定的信息保存到新建的excel表格中;

  :param wbname:
  :param data: 往excel中存储的数据;
  :param sheetname:
  :return:
  """
  @staticmethod
  def export_csv(save_path=None, header=None, data=None):

    # 创建一个 CSV 文件
    with open("my_file.csv", "w", newline="") as csvfile:
      # 创建一个 CSV 写入器
      writer = csv.writer(csvfile)

      # 写入标题行
      writer.writerow(header)

      # 写入数据行
      for row in data:
        writer.writerow(row)
