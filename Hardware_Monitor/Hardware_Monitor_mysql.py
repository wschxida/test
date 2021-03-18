# coding=utf8
import psutil
import time
from datetime import datetime
import json
import os
import pymysql


# 获取网卡名称和其ip地址，不包括回环
def get_netcard():
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and '192.168.1.' in item[1]:
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


if __name__ == '__main__':
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
        fl = open(file_name, 'w', encoding='utf-8')
        fl.write(json_result)
        fl.close()

        # # 复制文件到184
        # source_filename = file_name
        # destination_filename = "\\\\184\\kwm\\Common\\Server_Monitor\\Node_Monitor_OS\\Hardware_Status_All_Result\\" + file_name
        # copy_command = 'cp %s %s' % (source_filename, destination_filename)
        # os.popen(copy_command)

        # 连接mysql
        config = {
            'host': '192.168.1.118',
            'port': 3306,
            'user': 'root',
            'passwd': 'poms@db',
            'db': 'mymonitor',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        conn = pymysql.connect(**config)
        conn.autocommit(1)
        # 使用cursor()方法获取操作游标
        cur = conn.cursor()

        # 1.查询操作
        # 编写sql 查询语句
        node_id = int(result["ip"].split('.')[-1]) - 100
        monitor_time = result["time"]
        Executor_Count = result["executor_count"]["executor"]
        CPU_Count = result["cpu_info"]["count"]
        CPU_Percent = result["cpu_info"]["usage_percent"]
        Memory_Size = result["mem_info"]["total"]
        Memory_Percent = result["mem_info"]["usage_percent"]
        Network_Count = len(result["net_usage"])
        Network_Percent = result["net_usage"][0]["usage_percent"]
        Sys_Drive_Free_M = result["disk_info"][0]["free"]
        Sys_Drive_Free_Percent = result["disk_info"][0]["percent"]
        Drive_Free_Space_JSON = result['disk_info']
        Drive_Free_Space_JSON = json.dumps(Drive_Free_Space_JSON, ensure_ascii=False)

        sql = "insert into node_monitor_os(node_id, monitor_time, Executor_Count, CPU_Count, CPU_Percent, Memory_Size, " \
              "Memory_Percent,Network_Count, Network_Percent,Sys_Drive_Free_M, Sys_Drive_Free_Percent, Drive_Free_Space_JSON) " \
              "values({}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}');" \
            .format(node_id, monitor_time, Executor_Count, CPU_Count, CPU_Percent, Memory_Size, Memory_Percent,
                    Network_Count, Network_Percent, Sys_Drive_Free_M, Sys_Drive_Free_Percent, Drive_Free_Space_JSON)
        # print(sql)
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
        conn.close()

    except Exception as e:
        print(e)








