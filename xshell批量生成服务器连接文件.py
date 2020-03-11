
# xshell 批量生成Linux服务器连接文件
import sys


file_directory = 'C:\\Users\\DELL\\Documents\\NetSarang Computer\\6\\Xshell\\Sessions\\aliyun\\'
template_file = file_directory + 'template.xsh'
# print(file_directory)
with open(template_file, 'r', encoding="utf-16-le") as r:
    template = r.read()


ip_list = [
"119.23.46.189",
"39.108.142.210",
"39.108.177.0",
"39.108.140.186",
"39.108.177.190",
"39.108.177.19",
"120.78.64.229",
"120.78.64.66",
"39.108.238.97",
"39.108.145.189",
"39.108.188.8",
"39.108.184.235",
"120.78.64.154",
"39.108.235.57",
"120.78.64.204",
"120.78.64.200",
"47.107.149.130",
"47.107.35.70",
"47.107.76.115",
"47.107.158.94",
"120.78.12.126",
"47.107.41.150",
"47.107.56.26",
"120.79.101.83",
"47.107.72.123",
"120.79.101.137",
"120.79.102.87",
"120.79.102.164",
"120.79.102.178",
"47.106.216.24",
"119.23.46.189",
"47.107.80.43",
"120.78.227.88",
"120.79.100.182",
"120.79.102.187",
"47.106.199.101"]


for i in ip_list:
    newfile_name = file_directory + i + '.xsh'
    newfile_content = template.replace('39.108.176.97', i)
    # print(template)
    with open(newfile_name, 'w', encoding="utf-16-le") as w:
        w.write(newfile_content)
        w.close()


