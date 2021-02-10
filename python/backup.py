#!/usr/local/bin/python3
def shend_icmp_packet(ip_address,times):
    try:
        response = os.popen('ping -c ' + str(times) + ' '+ ip_address).read()
        print(response)
        # 取出丢包率
        lost = response[response.rindex(',',0,response.index("%"))+1:response.index("%")].strip()
        #取出指定的延时字符串
        res = list(response)
        index = 0
        count = 0
        for r in res:
            count += 1
            if r == "=" :
                index = count
        response = response[index + 1:-4]

        # 取出执行的延迟
        i = 0
        j = []
        res1 = list(response)
        for r in res1:
            i += 1
            if r == "/" :
                j.append(i)

        min = response[:j[0]-1]
        avg = response[j[0]:j[1]-1]
        max = response[j[1]:j[2]-1]
        return min,avg,max,lost
    except Exception as e:
        print("ping exec error",e)
postgres操作
		云pg添加权限
			select control_extension('create', 'pg_trgm');
		清除wal日志：pg_archivecleanup /home/pgsql_arch 00000002000000320000005F	（10.4版本的大多在pg_wal下，此命令会删掉此之前的所有数据）
					 若数据库起不来可用命令恢复：pg_resetwal /home/pgsql_data
		给vrp用户授权表的读权限
			grant select on 表 to vrp
		
		数据库重命名
			alter database [] rename to []
			
		备份恢复单表,到处表结构 加-s参数
			备份：pg_dump -h 10.1.13.48 -U postgres -t TABLE_NAME -f 备份文件 gitlabhq_production
			恢复：psql -h 10.1.13.48 -U postgres -d gitlabhq_production -f 备份文件
			
		备份数据库
			备份：pg_dump -h 10.1.13.48 -U postgres -f /postgres.sql  postgres(数据库名)
			恢复：psql -h 10.1.13.48 -U postgres -f /postgres.sql postgres
            
            1、登录数据库
```
/* 切换到数据库用户 */
su - postgres

/* 登录 */
psql
```
登录成功显示如下：
```
bash-4.2$ psql
psql (9.3.17)
Type "help" for help.

postgres=> 
```
2、切换数据库
```
/* 登录指定数据库 */
psql -U user -d dbname

/* 列举数据库 */
\l

/* 切换数据库 */
\c dbname
```
3、用户管理
```
/* 创建用户 */
CREATE ROLE rolename;
CREATE USER username WITH PASSWORD '*****';

/* 显示所有用户 */
\du

/* 修改用户权限 */
ALTER ROLE username WITH privileges;
/* 赋给用户表的所有权限 */
GRANT ALL ON tablename TO user; 
/* 赋给用户数据库的所有权限 */
GRANT ALL PRIVILEGES ON DATABASE dbname TO dbuser;

/* 撤销用户权限 */
REVOKE privileges ON tablename FROM user;


/* 撤销用户权限 */
```
4、数据库操作
```
/* 创建数据库 */
create database dbname; 

/* 删除数据库 */
drop database dbname;  
```
5、表操作
```
/* 增加让主键自增的权限 */
grant all on sequence tablename_keyname_seq to webuser;

 /* 重命名一个表 */
alter table [表名A] rename to [表名B]; 

/* 删除一个表 */
drop table [表名]; 

/* 在已有的表里添加字段 */
alter table [表名] add column [字段名] [类型]; 

/* 删除表中的字段 */
alter table [表名] drop column [字段名]; 

/* 重命名一个字段 */
alter table [表名] rename column [字段名A] to [字段名B]; 

/* 给一个字段设置缺省值 */
alter table [表名] alter column [字段名] set default [新的默认值];

/* 去除缺省值 */
alter table [表名] alter column [字段名] drop default; 

/* 插入数据 */
insert into 表名 ([字段名m],[字段名n],......) values ([列m的值],[列n的值],......); 

/* 修改数据 */
update [表名] set [目标字段名]=[目标值] where ...; 

/* 删除数据 */
delete from [表名] where ...; 

/* 删除表 */
delete from [表名];

/* 查询 */
SELECT * FROM dbname WHERE ...;

/* 创建表 */
create table (
    [字段名1] [类型1] primary key,
    [字段名2] [类型2],
    ......,
    [字段名n] [字段名n] )
```
6、退出
```
\q
quit
```

  """
  Desc：python luban pager发送短信，邮件，espace方法
  Remarks：安装python，然后pip3 install --proxy="http://域账号:域密码@proxy.huawei.com:8080" requests
  """

  import requests
  import json

  # 应用ID
  id = "luban_pager"
  # 密钥
  appkey = "*************"
  sms_url = "http://openapi.luban.inhuawei.com/api/newPager/send/sms"
  email_url = "http://openapi.luban.inhuawei.com/api/newPager/send/email"
  espace_url = "http://openapi.luban.inhuawei.com/api/newPager/send/espace"


  def send_sms(phone, content):
      # 短信发送
      headers = {
          "X-HW-ID": id,
          'X-HW-APPKEY': appkey,
          "content-type": "application/json",
      }
      body = {
          "address": phone,
          "content": content,
      }
      res = requests.post(url=sms_url, data=json.dumps(body), headers=headers)
      return res.text

  def send_email(address, subject, content):
    # 邮件发送
      headers = {
          "X-HW-ID": id,
          'X-HW-APPKEY': appkey,
          "content-type": "application/json",
      }
      body = {
          "address": address,
          "title": subject,
          "content": content,
      }
      res = requests.post(url=email_url, data=json.dumps(body), headers=headers)
      return res.text


  def send_espace(account, title, content):
    # espace发送
      headers = {
          "X-HW-ID": id,
          'X-HW-APPKEY': appkey,
          "content-type": "application/json",
      }
      body = {
          "address": account,
          "title": title,
          "content": content,
      }
      res = requests.post(url=espace_url, data=json.dumps(body), headers=headers)
      return res.text

  # 使用示例
  res1 = send_sms("l00471413","python, cloudpager, sms service test!")
  res2 = send_email("l00471413","pager", "python, cloudpager, email service test!")
  res3 = send_espace("l00471413","pager", "python, cloudpager, espace service test!")
  print(res1)
  print(res2)
  print(res3)
  

sendMessage(){
        /usr/bin/curl --request POST 'http://openapi.luban.inhuawei.com:80/api/newPager/send/sms' \
        --header 'X-HW-ID: isource-sms-notification' \
        --header 'X-HW-APPKEY: sFLebUitQWxAlHaaEug=' \
        --header 'Content-Type: application/json' \
        --data "{'address':'y00498850,lwx308218', 'content':\"$1\"}"
}


git config --global core.quotepath false  # 让带中文的文件能上传到代码仓

要每30秒执行一次脚本，要么写sleep 30的while脚本，要么在crontab增加延迟
* * * * * sleep 30; /var/script/run.sh >> log.txt

#!/bin/bash
sendMessage(){     # 发送短信函数
/usr/bin/curl --request POST 'http://openapi.luban.inhuawei.com:80/api/newPager/send/sms' \
--header 'X-HW-ID: isource-sms-notification' \
--header 'X-HW-APPKEY: sFLebUitQWxAlHaaEug=' \
--header 'Content-Type: application/json' \
--data "{'address':'y00498850,lwx308218', 'content':\"$1\"}"
}
while :
do
    p=0
    for i in {1..5}
    do
        #nums1=`ps -ef | grep sidekiq | grep -v grep | grep -Po "\[.*\]" | sed -nr 's/\[(.*)\]/\1/p' | awk '{print $1}'`
        #nums2=`ps -ef | grep sidekiq | grep -v grep | grep -Po "\[.*\]" | sed -nr 's/\[(.*)\]/\1/p' | awk '{print $3}'`
        n=`ps -ef | grep sidekiq | grep -v grep | grep -Po "\[.*\]" | sed -nr 's/\[(.*)\]/\1/p' | awk '{print $1/$3}'`
        #n=`echo "scale=3;$nums1/$nums2*100"`
        let p=$p+$n
    done
    if [ "$p" -ge 90 ]; then
        #echo $p
        sendMessage "当前磁盘使用率$p,超过90"
    #else
        #echo "当前磁盘使用率$p,正常"
    fi
    sleep 30
done

telnet 192.168.1.2:5432  # 可以查看防火墙
/devcloud/log/catalina.out  # tomcat日志位置，172.31.224.130 黄dg；devcloud用户要对web.xml文件有属组属主和644权限

clouddragon.huawei.com/release/home/release  # 版本包地址

对F12 中返回的时间戳，可以在作业平台 grep -rnw /devcloud/log/gitlab -e '时间戳' 进行定位机器
在welog中搜索时间戳也会找到底层日志编码，再根据编码到weblog中检索


一、sar的概述
在我使用的众多linux分析工具中，sar是一个非常全面的一个分析工具，可以比较瑞士军刀，对文件的读写，系统调用的使用情况，磁盘IO，CPU相关使用情况，内存使用情况，进程活动等都可以进行有效的分析。sar工具将对系统当前的状态进行取样，然后通过计算数据和比例来表达系统的当前运行状态。它的特点是可以连续对系统取样，获得大量的取样数据。取样数据和分析的结果都可以存入文件，使用它时消耗的系统资源很小。
话不多说，直接--help查看一下先
[root@lgh ~]# sar --help
Usage: sar [ options ] [ <interval> [ <count> ] ]
Options are:
[ -A ] [ -b ] [ -B ] [ -C ] [ -d ] [ -h ] [ -m ] [ -p ] [ -q ] [ -r ] [ -R ]
[ -S ] [ -t ] [ -u [ ALL ] ] [ -v ] [ -V ] [ -w ] [ -W ] [ -y ]
[ -I { <int> [,...] | SUM | ALL | XALL } ] [ -P { <cpu> [,...] | ALL } ]
[ -j { ID | LABEL | PATH | UUID | ... } ] [ -n { <keyword> [,...] | ALL } ]
[ -o [ <filename> ] | -f [ <filename> ] ] [ --legacy ]
[ -i <interval> ] [ -s [ <hh:mm:ss> ] ] [ -e [ <hh:mm:ss> ] ]
-A：所有报告的总和
-u：输出CPU使用情况的统计信息
-v：输出inode、文件和其他内核表的统计信息
-d：输出每一个块设备的活动信息
-r：输出内存和交换空间的统计信息
-b：显示I/O和传送速率的统计信息-R：输出内存页面的统计信息
-y：终端设备活动情况
-w：输出系统交换活动信息
-B：显示换页状态；
-e：设置显示报告的结束时间
-f：从指定文件提取报告
-i：设状态信息刷新的间隔时间
-p：报告每个CPU的状态
-q：平均负载分析
使用语法：
sar [options] [-A] [-o file] [ <interval> [ <count> ] ]
其中：interval为采样间隔，count为采样次数，默认值是1； -o file表示将命令结果以二进制格式存放在文件中，file 是文件名

二、统计CPU使用情况
sar -u  #统计CPU的使用情况，每间隔1秒钟统计一次总共统计三次：#sar -u 1 3
[root@lgh ~]# sar -u 1 3
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
09:42:45 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
09:42:46 PM     all      0.00      0.00      0.00      0.00      0.00    100.00
09:42:47 PM     all      0.03      0.00      0.03      0.00      0.00     99.94
09:42:48 PM     all      0.03      0.00      0.03      0.00      0.00     99.94
Average:        all      0.02      0.00      0.02      0.00      0.00     99.96
[root@lgh ~]# sar -o test.txt -u 1 3  #其中-o表示以二进制的格式把结果存入到test.txt文件中，不能使用cat，more，less等查看
[root@lgh ~]# sar -u -f test.txt   #查看该二进制结果文件
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
09:46:14 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
09:46:15 PM     all      0.00      0.00      0.00      0.00      0.00    100.00
09:46:16 PM     all      0.03      0.00      0.03      0.00      0.00     99.94
09:46:17 PM     all      0.00      0.00      0.03      0.00      0.00     99.97
Average:        all      0.01      0.00      0.02      0.00      0.00     99.97
%user #用户空间的CPU使用
%nice 改变过优先级的进程的CPU使用率
%system 内核空间的CPU使用率
%iowait CPU等待IO的百分比
%steal 虚拟机的虚拟机CPU使用的CPU
%idle 空闲的CPU
在以上的显示当中，主要看%iowait和%idle，%iowait过高表示存在I/O瓶颈，即磁盘IO无法满足业务需求，如果%idle过低表示CPU使用率比较严重，需要结合内存使用等情况判断CPU是否瓶颈。

三、平均负载统计分析
sar -q #查看平均负载：其中每间隔1秒钟统计一次总共统计三次  #sar -q 1 3
[root@lgh ~]# sar -q 1 3
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
09:58:39 PM   runq-sz  plist-sz   ldavg-1   ldavg-5  ldavg-15
09:58:40 PM         0      1535      0.00      0.03      0.00
09:58:41 PM         0      1535      0.00      0.03      0.00
09:58:42 PM         0      1535      0.00      0.03      0.00
Average:            0      1535      0.00      0.03      0.00
runq-sz 运行队列的长度（等待运行的进程数，每核的CP不能超过3个）
plist-sz 进程列表中的进程（processes）和线程数（threads）的数量
ldavg-1 最后1分钟的CPU平均负载，即将多核CPU过去一分钟的负载相加再除以核心数得出的平均值，5分钟和15分钟以此类推
ldavg-5 最后5分钟的CPU平均负载
ldavg-15 最后15分钟的CPU平均负载

四、内存统计分析
sar -r #查看内存使用情况，每间隔1秒钟统计一次总共统计三次：#sar -r 1 3
[root@lgh ~]# sar -r 1 3
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
10:01:15 PM kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit
10:01:16 PM 233550984  30597240     11.58    758212  20745900  14822388      5.44
10:01:17 PM 233550836  30597388     11.58    758212  20745900  14822388      5.44
10:01:18 PM 233551972  30596252     11.58    758212  20745900  14822388      5.44
Average:    233551264  30596960     11.58    758212  20745900  14822388      5.44
kbmemfree 空闲的物理内存大小
kbmemused 使用中的物理内存大小
%memused 物理内存使用率
kbbuffers 内核中作为缓冲区使用的物理内存大小，kbbuffers和kbcached:这两个值就是free命令中的buffer和cache.
kbcached 缓存的文件大小
kbcommit 保证当前系统正常运行所需要的最小内存，即为了确保内存不溢出而需要的最少内存（物理内存+Swap分区）
commit 这个值是kbcommit与内存总量（物理内存+swap分区）的一个百分比的值

五、统计swap分区
sar -W #查看系统swap分区的统计信息：每间隔1秒钟统计一次总共统计三次：#sar -W 1 3
[root@lgh ~]# sar -W 1 3
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
10:03:21 PM  pswpin/s pswpout/s
10:03:22 PM      0.00      0.00
10:03:23 PM      0.00      0.00
10:03:24 PM      0.00      0.00
Average:         0.00      0.00
pswpin/s 每秒从交换分区到系统的交换页面（swap page）数量
pswpott/s 每秒从系统交换到swap的交换页面（swap page）的数量

六、查看磁盘IO
sar -b #查看I/O和传递速率的统计信息，每间隔1秒钟统计一次总共统计三次：#sar -b 1 3
[root@lgh ~]# sar -b 1 3
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
10:06:16 PM       tps      rtps      wtps   bread/s   bwrtn/s
10:06:17 PM     30.00      0.00     30.00      0.00    240.00
10:06:18 PM      0.00      0.00      0.00      0.00      0.00
10:06:19 PM      0.00      0.00      0.00      0.00      0.00
Average:        10.00      0.00     10.00      0.00     80.00
tps 磁盘每秒钟的IO总数，等于iostat中的tps
rtps 每秒钟从磁盘读取的IO总数
wtps 每秒钟从写入到磁盘的IO总数
bread/s 每秒钟从磁盘读取的块总数
bwrtn/s 每秒钟此写入到磁盘的块总数

七、查看磁盘使用情况
sar -d #磁盘使用详情统计，每间隔1秒钟统计一次总共统计三次：#sar -d 1 3
[root@lgh ~]# sar -d 1 3
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
10:08:16 PM       DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
10:08:17 PM    dev8-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:08:17 PM  dev253-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:08:17 PM  dev253-1      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
 
10:08:17 PM       DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
10:08:18 PM    dev8-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:08:18 PM  dev253-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:08:18 PM  dev253-1      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
 
10:08:18 PM       DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
10:08:19 PM    dev8-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:08:19 PM  dev253-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:08:19 PM  dev253-1      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
 
Average:          DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
Average:       dev8-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
Average:     dev253-0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
Average:     dev253-1      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
DEV 磁盘设备的名称，如果不加-p，会显示dev253-0类似的设备名称，因此加上-p显示的名称更直接
tps：每秒I/O的传输总数
rd_sec/s 每秒读取的扇区的总数
wr_sec/s 每秒写入的扇区的总数
avgrq-sz 平均每次次磁盘I/O操作的数据大小（扇区）
avgqu-sz 磁盘请求队列的平均长度
await 从请求磁盘操作到系统完成处理，每次请求的平均消耗时间，包括请求队列等待时间，单位是毫秒（1秒等于1000毫秒），等于寻道时间+队列时间+服务时间
svctm I/O的服务处理时间，即不包括请求队列中的时间
%util I/O请求占用的CPU百分比，值越高，说明I/O越慢

八、网络使用分析
sar -n #统计网络信息
sar -n选项使用6个不同的开关：DEV，EDEV，NFS，NFSD，SOCK，IP，EIP，ICMP，EICMP，TCP，ETCP，UDP，SOCK6，IP6，EIP6，ICMP6，EICMP6和UDP6 ，DEV显示网络接口信息，EDEV显示关于网络错误的统计数据，NFS统计活动的NFS客户端的信息，NFSD统计NFS服务器的信息，SOCK显示套接字信息，ALL显示所有5个开关。它们可以单独或者一起使用。
1.10.1：sar -n DEV 1 1： 每间隔1秒统计一次，总计统计1次，下面的average是在多次统计后的平均值
#IFACE 本地网卡接口的名称
#rxpck/s 每秒钟接受的数据包
#txpck/s 每秒钟发送的数据库
#rxKB/S 每秒钟接受的数据包大小，单位为KB
#txKB/S 每秒钟发送的数据包大小，单位为KB
#rxcmp/s 每秒钟接受的压缩数据包
#txcmp/s 每秒钟发送的压缩包
#rxmcst/s 每秒钟接收的多播数据包
sar -n EDEV 1 1 #统计网络设备通信失败信息：
[root@lgh ~]# sar -n DEV 1 1
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
10:13:52 PM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
10:13:53 PM        lo     16.00     16.00      1.86      1.86      0.00      0.00      0.00
10:13:53 PM      eth0    132.00     25.00     14.28      2.34      0.00      0.00      0.00
10:13:53 PM      eth1      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:13:53 PM      eth2      0.00      0.00      0.00      0.00      0.00      0.00      0.00
10:13:53 PM      eth3      0.00      0.00      0.00      0.00      0.00      0.00      0.00
 
Average:        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
Average:           lo     16.00     16.00      1.86      1.86      0.00      0.00      0.00
Average:         eth0    132.00     25.00     14.28      2.34      0.00      0.00      0.00
Average:         eth1      0.00      0.00      0.00      0.00      0.00      0.00      0.00
Average:         eth2      0.00      0.00      0.00      0.00      0.00      0.00      0.00
Average:         eth3      0.00      0.00      0.00      0.00      0.00      0.00      0.00
IFACE 网卡名称
rxerr/s 每秒钟接收到的损坏的数据包
txerr/s 每秒钟发送的数据包错误数
coll/s 当发送数据包时候，每秒钟发生的冲撞（collisions）数，这个是在半双工模式下才有
rxdrop/s 当由于缓冲区满的时候，网卡设备接收端每秒钟丢掉的网络包的数目
txdrop/s 当由于缓冲区满的时候，网络设备发送端每秒钟丢掉的网络包的数目
txcarr/s 当发送数据包的时候，每秒钟载波错误发生的次数
rxfram 在接收数据包的时候，每秒钟发生的帧对其错误的次数
rxfifo 在接收数据包的时候，每秒钟缓冲区溢出的错误发生的次数
txfifo 在发生数据包 的时候，每秒钟缓冲区溢出的错误发生的次数
1.10.3：sar -n SOCK 1 1 #统计socket连接信息
sar -n SOCK 1 1 #统计socket连接信息
totsck 当前被使用的socket总数
tcpsck 当前正在被使用的TCP的socket总数
udpsck 当前正在被使用的UDP的socket总数
rawsck 当前正在被使用于RAW的skcket总数
if-frag 当前的IP分片的数目
tcp-tw TCP套接字中处于TIME-WAIT状态的连接数量
########如果你使用FULL关键字，相当于上述DEV、EDEV和SOCK三者的综合
sar -n TCP 1 3 #TCP连接的统计
active/s 新的主动连接
passive/s 新的被动连接
iseg/s 接受的段
oseg/s 输出的段
sar -n 使用总结
-n DEV ： 网络接口统计信息。
-n EDEV ： 网络接口错误。
-n IP ： IP数据报统计信息。
-n EIP ： IP错误统计信息。
-n TCP ： TCP统计信息。
-n ETCP ： TCP错误统计信息。
-n SOCK ： 套接字使用。

九、进程，文件状态
sar -v #进程、inode、文件和锁表状态 ，每间隔1秒钟统计一次总共统计三次：#sar -v 1 3
[root@lgh ~]# sar -v 1 3
Linux 2.6.32-696.el6.x86_64 (lgh)   10/06/2019      _x86_64_        (32 CPU)
 
10:17:06 PM dentunusd   file-nr  inode-nr    pty-nr
10:17:07 PM   2165205      5440    371435         1
10:17:08 PM   2165205      5440    371434         1
10:17:09 PM   2165205      5440    371434         1
Average:      2165205      5440    371434         1
dentunusd 在缓冲目录条目中没有使用的条目数量
file-nr 被系统使用的文件句柄数量
inode-nr 已经使用的索引数量
pty-nr 使用的pty数量

###这里面的索引和文件句柄值不是ulimit -a查看到的值，而是sysctl.conf里面定义的和内核相关的值， max-file表示系统级别的能够打开的文件句柄的数量， 而ulimit -n控制进程级别能够打开的文件句柄的数量，可以使用sysctl -a | grep inode和sysctl -a | grep file查看，具体含义如下：
file-max中指定了系统范围内所有进程可打开的文件句柄的数量限制(系统级别， kernel-level)。 （The value in file-max denotes the maximum number of file handles that the Linux kernel will allocate）。当收到"Too many open files in system"这样的错误消息时， 就应该曾加这个值了。
# cat /proc/sys/fs/file-max
4096
# echo 100000 > /proc/sys/fs/file-max
或者
# echo ""fs.file-max=65535" >> /etc/sysctl.conf
# sysctl -p
file -nr 可以查看系统中当前打开的文件句柄的数量。 他里面包括3个数字： 第一个表示已经分配了的文件描述符数量， 第二个表示空闲的文件句柄数量， 第三个表示能够打开文件句柄的最大值（跟file-max一致）。 内核会动态的分配文件句柄， 但是不会再次释放他们（这个可能不适应最新的内核了， 在我的file-nr中看到第二列一直为0， 第一列有增有减）
man bash， 找到说明ulimit的那一节：提供对shell及其启动的进程的可用资源（包括文件句柄， 进程数量， core文件大小等）的控制。 这是进程级别的， 也就是说系统中某个session及其启动的每个进程能打开多少个文件描述符， 能fork出多少个子进程等... 当达到上限时， 会报错"Too many open files"或者遇上Socket/File: Can’t open so many files等

十、常用命令
默认监控: sar 5 5     //  CPU和IOWAIT统计状态
(1) sar -b 5 5        // IO传送速率
(2) sar -B 5 5        // 页交换速率
(3) sar -c 5 5        // 进程创建的速率
(4) sar -d 5 5        // 块设备的活跃信息
(5) sar -n DEV 5 5    // 网路设备的状态信息
(6) sar -n SOCK 5 5   // SOCK的使用情况
(7) sar -n ALL 5 5    // 所有的网络状态信息
(8) sar -P ALL 5 5    // 每颗CPU的使用状态信息和IOWAIT统计状态
(9) sar -q 5 5        // 队列的长度（等待运行的进程数）和负载的状态
(10) sar -r 5 5       // 内存和swap空间使用情况
(11) sar -R 5 5       // 内存的统计信息（内存页的分配和释放、系统每秒作为BUFFER使用内存页、每秒被cache到的内存页）
(12) sar -u 5 5       // CPU的使用情况和IOWAIT信息（同默认监控）
(13) sar -v 5 5       // inode, file and other kernel tablesd的状态信息
(14) sar -w 5 5       // 每秒上下文交换的数目
(15) sar -W 5 5       // SWAP交换的统计信息(监控状态同iostat 的si so)
(16) sar -x 2906 5 5  // 显示指定进程(2906)的统计信息，信息包括：进程造成的错误、用户级和系统级用户CPU的占用情况、运行在哪颗CPU上
(17) sar -y 5 5       // TTY设备的活动状态
(18) 将输出到文件(-o)和读取记录信息(-f)

