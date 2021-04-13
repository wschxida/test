该程序用于获取西瓜数据接口，再将其push到redis中


## Requirements
- Python 3.7;
- sys;
- requests;
- hashlib;
- json;
- hashlib;
- re;
- redis;
- time;
- copy;


#调用方式

命令行
xiaohongshu_search.exe argv[1] argv[2]

argv[1]：搜索词列表路径，支持绝对路径和相对路径
argv[2]：翻页数，最多翻5页


#备注

- 运行完毕后，数据将直接push到redis，作为一条website_no为S16296的数据插入到MySQL中;






