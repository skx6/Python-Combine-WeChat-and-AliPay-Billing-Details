# -- coding: utf-8 -- 
# @Author:  Kaixiang Song
# @Project: 数据结构与算法 
# @File:    helper.py
# @Time:    2020/7/6 14:10 

import os
import pandas as pd


def print_data_info(data_frame, data_name='未命名表格'):
    assert isinstance(data_frame, pd.DataFrame)
    i, c = data_frame.shape
    print('\n表格“{}”的信息如下：'.format(data_name))
    print('表格的规模为：{}行{}列。'.format(i, c))
    columns = data_frame.columns
    print("表格包含{}列，列名为：{}。".format(len(columns), '，'.join(map(lambda x: str(x).strip(), list(columns)))))
    print("数据类型为：")
    print(data_frame.dtypes)


def strip_in_data(data):
    """
    把列名中和数据中首尾的空格都去掉。
    :param data:
    :return:
    """
    data = data.rename(columns={column_name: column_name.strip() for column_name in data.columns})
    data = data.applymap(lambda x: x.strip().strip('¥') if isinstance(x, str) else x)
    return data


def get_data(path, start_line=0, encoding='UTF-8'):
    """

    :param path: 微信或支付宝账单文件路径。
    :param start_line: 列名之前的无效行的数目。
    :return:
    """

    # path = 'G:/事务/账本/下载下的/微信/微信支付账单(20200401-20200701)/微信支付账单(20200401-20200701)_processed.csv'
    assert os.path.exists(path), 'File path not found: "{}".'.format(path)
    f = open(path, 'r', encoding=encoding)
    for _ in range(start_line):
        next(f)
    data = pd.read_csv(f)

    # 去除列名与数值中的空格。
    data = strip_in_data(data)

    return data


def update_data_types(data, column_types):
    """
    更新表格指定列的数据类型。
    :param data:
    :param column_types:
    :return:
    """
    assert isinstance(column_types, dict)
    if column_types is not None:
        for column_name, column_type in column_types.items():
            data[column_name] = data[column_name].astype(column_type)
    return data


if __name__ == "__main__":
    pass
