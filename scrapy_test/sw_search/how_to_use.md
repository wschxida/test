- #如何运行
在项目路径执行 python3 run_sw_search_all.py

- #查看结果
##在[kibana](http://192.168.1.231:5601)中查看

```
POST _xpack/sql?format=txt
{
  "query":"select * from sw limit 10"
}

POST _xpack/sql?format=txt
{
  "query":"select count(*) from sw"
}

GET sw/doc/_search
{
  "query": {
    "match_all": {}
  }
}
```