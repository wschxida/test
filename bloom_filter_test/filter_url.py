#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : filter_url.py
# @Author: Cedar
# @Date  : 2020/11/3
# @Desc  :


import bloompy


# bf = bloompy.BloomFilter(element_num=10, error_rate=0.1)

# 从一个文件里恢复过滤器。自动识别过滤器的种类。
# recoverd_bf = bloompy.get_filter_fromfile('url.suffix')
# 或者使用过滤器类的类方法‘fromfile’ 来进行过滤器的复原。对应的类只能恢复对应的过滤器。
bf = bloompy.BloomFilter.fromfile('url.suffix')


# 返回已经插入的元素个数
print(bf.count)
# 过滤器的容量
print(bf.capacity)
# 过滤器的位向量
print(bf.bit_array)
# 过滤器位数组长度
print(bf.bit_num)
# 过滤器的哈希种子，默认是素数，可修改
print(bf.seeds)
# 过滤器的哈希函数个数
print(bf.hash_num)

# 添加元素
print(bf.add(1))
print(bf.add(2))
print(bf.add(3))
print(bf.add(4))
print(bf.add(5))
# 判断元素是否存在
print(bf.exists(1))


# 将过滤器存储在一个文件里
bf.tofile('url.suffix')
