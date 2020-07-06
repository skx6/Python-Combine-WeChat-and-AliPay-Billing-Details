# Python-

This is a blog with usefull tools for merging WeChat and Ali Pay billing details. which is mainly for Chinese users, that is why it written in Chinese.

使用Python语言快速合并微信和支付宝账单csv文件，用到pandas扩展包。

账单是我们生活中随处需要的一部分，在互联网中的账单往往分布在不同的公司，成为数据孤岛，给用户自身数据的整合造成不便。

本文旨在解决微信和支付宝账单的问题。该项目是一个离线的工程，需要用户自行下载微信账单和支付宝账单的csv文件，使用前记得修改主程序combine_wx_zfb.py中的三个路径参数：

path_wx：微信账单路径，
path_zfb：支付宝账单路径，
save_path：合并后的路径，可以自己取，但是文件夹一定要存在。

rules_list是合并规则，正常情况下不用动了，除了你有特殊的需要。

参数start和end表示合并后的账单的时间段，按照指定格式书写，需要注意的是，你需要保证在微信账单文件和支付宝账单文件中，涵盖着这一时间段。

只要你可以成功地把程序运行起来，就可以生成合并后的账单，且按照时间排好了顺序，如图所示。

有一些注意事项在脚本开头，读者可以自行查看。

