# -*- coding: UTF-8 -*-
import psutil
import time
from datetime import datetime
import json
import os
import sys, getopt


# 获取网卡名称和其ip地址，不包括回环
def get_netcard():
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and '192.168.' in item[1]:
                netcard_info.append((k, item[1]))
    return netcard_info


# 获取CPU信息
def get_cpu_info():
    cpu = dict()
    cpu['usage_percent'] = psutil.cpu_percent(interval=1)
    cpu['count'] = psutil.cpu_count()
    return cpu


# 获取内存信息
def get_mem_info():
    mem = dict()
    virtual_memory = psutil.virtual_memory()
    mem['total'] = round(virtual_memory.total / 1024.0 / 1024.0 / 1024.0)
    mem['available'] = round(virtual_memory.available / 1024.0 / 1024.0 / 1024.0)
    mem['usage_percent'] = virtual_memory.percent
    mem['used'] = round(virtual_memory.used / 1024.0 / 1024.0 / 1024.0)
    mem['free'] = round(virtual_memory.free / 1024.0 / 1024.0 / 1024.0)
    return mem


# 获取磁盘
def get_disk_info():
    disks = []
    for partition in psutil.disk_partitions():
        if 'cdrom' in partition.opts or partition.fstype == '':
            continue
        disk_name = partition.device.split(':')[0]
        info = psutil.disk_usage(partition.mountpoint)
        disk_total = round(info.total / 1024.0 / 1024.0)
        disk_used = round(info.used / 1024.0 / 1024.0)
        disk_free = round(info.free / 1024.0 / 1024.0)
        usage_percent = info.percent

        disk = {'name': disk_name, 'total': disk_total, 'used': disk_used,
                'free': disk_free, 'percent': usage_percent}
        disks.append(disk)

    return disks


# 获取采集进程数
def get_executor_count():
    executor = {'executor': 0}
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        pname = p.name()
        if pname == "WebDataMiner.exe" or pname == "WebCrawler.exe" or pname == "TextDataMiner.exe" or pname == "MiniDataMiner.exe":
            executor['executor'] = executor['executor'] + 1
    return executor


# 计算网络使用率
def __check_speeds():
    rs = {}
    for net_name, stats in psutil.net_if_stats().items():
        if type(stats) is tuple or not stats.isup:
            continue
        rs[net_name] = stats.speed
    return rs


def __snapshoot():
    rs = {}
    for net_name, stats in psutil.net_io_counters(pernic=True).items():
        rs[net_name] = stats.bytes_recv
    return rs


# 网络使用率
def get_net_usage():
    net_usages = []
    nets = __check_speeds()
    snap_prev = __snapshoot()
    time.sleep(1)
    snap_now = __snapshoot()
    for net_name, speed in nets.items():
        if speed > 0:
            recv_prev = snap_prev[net_name]
            recv_now = snap_now[net_name]
            usage_percent = round((recv_now - recv_prev) * 100 / (speed * 1024 * 1024 / 8.), 2)
            if usage_percent > 0:
                item = {'net_name': net_name, 'usage_percent': usage_percent}
                net_usages.append(item)
    return net_usages


def main(argv):
    output_file = None
    try:
        opts, args = getopt.getopt(argv, "ho:", ["ofile="])
    except getopt.GetoptError:
        print('Hardware_Monitor.py -o <output_file>')
        # sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print('Hardware_Monitor.py -o <output_file>')
            # sys.exit()
        elif opt in ("-o", "--ofile"):
            output_file = arg
            print(output_file)

    try:
        ip = get_netcard()[0][1]
        cpu_info = get_cpu_info()
        mem_info = get_mem_info()
        disk_info = get_disk_info()
        executor_count = {'executor': 0}
        net_usage = get_net_usage()
        result = {"time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "ip": ip, "cpu_info": cpu_info,
                  "mem_info": mem_info, "disk_info": disk_info,
                  "executor_count": executor_count, "net_usage": net_usage}
        json_result = json.dumps(result, ensure_ascii=False)
        # 记录到file
        curpath = os.path.dirname(os.path.realpath(__file__))
        file_name = curpath + '/' + ip + '.txt'
        if output_file:
            file_name = output_file
        fl = open(file_name, 'w', encoding='utf-8')
        fl.write(json_result)
        fl.close()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(sys.argv[1:])









