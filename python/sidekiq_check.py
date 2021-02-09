#!/bin/bash
sendMessage(){     # 发送短信函数，报警sidekiq核心使用率
/usr/bin/curl --request POST 'http://openapi.luban.inhuawei.com:80/api/newPager/send/sms' \
--header 'X-HW-ID: isource-sms-notification' \
--header 'X-HW-APPKEY: sFLebUitQWxAlHaaEug=' \
--header 'Content-Type: application/json' \
--data "{'address':'y00498850,lwx308218', 'content':\"$1\"}"
}
ips=$(ifconfig eth0 | awk '{print $2}')
while :
do
    p=0
    for i in {1..5}
    do
        #nums1=`ps -ef | grep sidekiq | grep -v grep | grep -Po "\[.*\]" | sed -nr 's/\[(.*)\]/\1/p' | awk '{print $1}'`
        #nums2=`ps -ef | grep sidekiq | grep -v grep | grep -Po "\[.*\]" | sed -nr 's/\[(.*)\]/\1/p' | awk '{print $3}'`
        n=`ps -ef | grep sidekiq | grep -v grep | grep -Po "\[.*\]" | sed -nr 's/\[(.*)\]/\1/p' | awk '{print $1/$3}'`
        #n=`echo "scale=3;$nums1/$nums2*100"`
        #let p=$p+$n
        p=\$(echo "\$p+\$n" | bc)
    sleep 30
    done
    avg=$(echo "scale=2;$p/5" | bc)
    if [ "$avg" -ge 90 ]; then
        #echo $avg
        sendMessage "主机ips 当前磁盘使用率$avg,超过90"
    #else
        #echo "主机ips 当前磁盘使用率$avg,正常"
    fi
done
