#!/bin/bash
#当nginx进程不存在时，就干掉keepalived
 
if [ "$(ps -ef | grep "nginx: master process"| grep -v grep )" == "" ]
 then
 killall keepalived
fi