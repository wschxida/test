import requests
import json
import time

url = 'http://lumtest.com/myip.json'

proxies_template = {"http": "http://{0}:8213",
                    "https": "http://{0}:8213"}


ip_list = ["39.108.176.97",
"39.108.142.251",
"120.77.181.86",
"39.108.143.134",
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



# proxies["http"] = proxies["http"].format("1.1.1.1")
# proxies["https"] = proxies["https"].format("1.1.1.1")
# print(proxies)
proxies = {}

for i in ip_list:

    proxies["http"] = proxies_template["http"].format(i)
    proxies["https"] = proxies_template["https"].format(i)
    print(i)
    # print(proxies)

    try:
        data = requests.get(url, proxies=proxies, timeout=5)
        text = data.text
        print(text)
    except:
        pass

# data = requests.get(url, timeout=5)

# text = data.text
# text_dict = json.loads(text)
# ip = text_dict["ip"]
#
# print(ip)


