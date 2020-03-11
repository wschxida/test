#! /bin/bash
# 若不存在，则启动

function check(){
  count=`ps -ef |grep $1 |grep -v "grep" |wc -l`
  #echo $count
  if [ 0 == $count ];then
    cd /home/grs/scrapy_project/sw_search/;python3 $1
  fi
}

check run.py

