# -- coding: utf-8 -- 
# @Author:  Kaixiang Song
# @Project: 数据结构与算法 
# @File:    combine_wx_zfb.py
# @Time:    2020/7/6 13:51 


import pandas as pd
from helper import print_data_info, get_data, update_data_types

"""
基于以下假设，适用于2020年7月以来下载的账单文件：

微信账单中包含的项目为11个：交易时间，交易类型，交易对方，商品，收/支，金额(元)，支付方式，当前状态，交易单号，商户单号，备注
支付宝账单中包含的项目为16个：交易号，商家订单号，交易创建时间，付款时间，最近修改时间，交易来源地，类型，交易对方，商品名称，金额（元），收/支，交易状态，服务费（元），成功退款（元），备注，资金状态

微信账单和支付宝账单前16行和前4行是废掉的，csv文件编码格式分别为utf-8和gbk。

交易时间分别在“交易时间”和“交易创建时间”中。

如官方下载的文档有名称修改，请相应的修改本脚本涉及的字符串常量。

若仍有考虑不周的方面，欢迎提建议改进。

注意，合并后的账单不包含银行卡收入，例如工资、他人的银行卡转账等项目，需自行添加。

"""


def transaction_checking_wx(data, column_types=None):
    """
    在微信账单中，资金转移时有时需要服务费，需要计入记为“支付”，并去掉收支为“/”的项目。
    :param data:
    :return:
    """
    # 删除“收支”为空且“备注”为空的项目。
    data = data.drop(data[(data['收/支'] == '/') & (data['备注'] == '/')].index)
    # 从备注中提取出有服务费的项目，填写进入收支明细中。
    data.ix[data['备注'].str.contains('服务费'), ['收/支']] = '支出'
    data.ix[data['备注'].str.contains('服务费'), ['金额(元)']] = data.ix[data['备注'].str.contains('服务费'), ['备注']].applymap(lambda x: float(x.strip('服务费¥'))).values
    # 更新数据格式。
    data = update_data_types(data, column_types)
    return data


def transaction_checking_zfb(data, column_types=None):
    """
    在支付宝账单中，有些资金状态为“空”或“资金转移”的，将服务费算作支出。
    :param data:
    :return:
    """
    # 对于资金状态为空的情况，是交易关闭，不计入结算。
    data = data.drop(data[data['资金状态'] == ''].index)
    # 对于资金状态为“资金转移”的，如果服务费为零，那么也删除该行。
    data = data.drop(data[(data['资金状态'] == '资金转移') & (data['服务费（元）'] == 0.0)].index)
    # 将服务费算作支出，填写到金额中。
    data.ix[data['服务费（元）'] > 0.0, ['收/支']] = '支出'
    # print(data.ix[data['服务费（元）'] > 0.0, ['交易号']])  # 这些是出手续费的交易号
    # 将手续费金额填写进收支金额中。
    data.ix[data['服务费（元）'] > 0.0, ['金额（元）']] = data.ix[data['服务费（元）'] > 0.0, ['服务费（元）']].values
    # 更新数据格式。
    data = update_data_types(data, column_types)
    return data


def extract_and_rename(data, columns, column_corr):
    """
    从原始表格中提取出数据，并更换为指定的列名。
    :param data:
    :param columns:
    :param column_corr:
    :return:
    """

    assert isinstance(columns, (list, tuple))
    assert isinstance(column_corr, dict)
    data = data.rename(columns=column_corr)
    data = data[list(columns)]
    return data


def merge(path_wx, path_zfb, rules_list, save_path, start='2020/6/1 0:0:0', end='2020/7/1 0:0:0'):
    wx, zfb, hb, dt = list(zip(*rules_list))

    data_wx = get_data(path_wx, start_line=16, encoding='utf-8')
    data_zfb = get_data(path_zfb, start_line=4, encoding='gbk')

    data_wx = transaction_checking_wx(data_wx, {k: v for k, v in zip(wx, dt)})
    data_zfb = transaction_checking_zfb(data_zfb, {k: v for k, v in zip(zfb, dt)})

    data_wx = extract_and_rename(data_wx, hb, {k: v for k, v in zip(wx, hb)})
    data_zfb = extract_and_rename(data_zfb, hb, {k: v for k, v in zip(zfb, hb)})

    data = pd.concat([data_wx, data_zfb], axis=0, sort=False)       # 合并
    data = data.sort_values(by='交易时间')              # 按照交易时间排序
    data = data.ix[(data['交易时间'] > start) & (data['交易时间'] < end)]  # 筛选出满足时间要求的记录
    print_data_info(data, '合并后账单')

    print('\n{}至{}期间数据统计：'.format(start, end))
    data_analysis(data)

    data.to_excel(save_path, encoding='gbk')

#
# def post_process(data):
#     """
#     对合并后的数据做一些后处理。
#     :param data:
#     :return:
#     """
#     return data


def data_analysis(data):
    print('总收入：{}元。'.format(sum(data.ix[data['收支'] == '收入', ['交易金额']].values)[0]))
    print('总支出：{}元。'.format(sum(data.ix[data['收支'] == '支出', ['交易金额']].values)[0]))


if __name__ == "__main__":
    path_wx = 'G:/事务/账本/下载下的/微信/微信支付账单(20200101-20200401)/微信支付账单(20200101-20200401).csv'
    path_zfb = 'G:/事务/账本/下载下的/支付宝/alipay_record_20200706_1143_1.csv'
    save_path = 'G:/事务/账本/last.xlsx'

    #                微信          支付宝         合并后    数据类型
    rules_list = [['交易时间', '交易创建时间', '交易时间', 'datetime64'],
                  ['交易对方', '交易对方',     '交易对方', 'object'],
                  ['商户单号', '商家订单号',   '商户单号', 'object'],
                  ['交易类型', '类型',         '交易类型', 'object'],
                  ['交易单号', '交易号',       '交易单号', 'object'],
                  ['当前状态', '资金状态',     '当前状态', 'object'],
                  ['商品',     '商品名称',     '商品名称', 'object'],
                  ['收/支',    '收/支',        '收支',     'object'],
                  ['金额(元)', '金额（元）',   '交易金额', 'float64'],
                  ['备注',     '备注',         '备注',     'object'],
                  ]

    merge(path_wx, path_zfb, rules_list, save_path,
          start='2020/2/1 0:0:0', end='2020/3/1 0:0:0')
