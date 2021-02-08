#!/bin/bash
while :
do
cecho () {
        echo -e "\033[$1m$2\033[0m" 
}
w=$(who | wc -l)
echo   "当前登陆的用户数为:  `cecho 33 $w`"
p=$(ps aux | wc -l)
echo   "当前系统开启的进程数为:  `cecho 31 $p`"
r=$(rpm -qa | wc -l)
echo   "当前系统安装的软件包数为:  `cecho 32 $r`"
n=`uptime | sed -n 's/.*://p'`
echo "主机平均负载量为: `cecho 34 "$n"`"
x=`ifconfig eth0 | awk  '/RX p/{print $5}'` 
echo "主机eth0网卡接收流量为: `cecho 34 "$x"` B字节"
y=`ifconfig eth0 | awk  '/TX p/{print $5}'`
echo "主机eth0网卡发送流量为: `cecho 34 "$y"` B字节"
z=`free -h | awk '/^Mem/{print $4}'`
echo "主机剩余内存容量为: `cecho 34 "$z"`"
e=`df -h | awk '/\/$/{print $4}'`
echo "主机剩余内存容量为: `cecho 34 "$e"`"
k=`awk 'END{print NR}' /etc/passwd`
echo "当前主机用户总量为: `cecho 34 "$k"`"
awk '{ip[$1]++}END{for(i in ip){print  i" 网页""被访问 "ip[i]" 次"}}' /usr/local/nginx/logs/access.log
sleep 3
clear
done
