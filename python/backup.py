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

telnet 192.168.1.2 5432  # 可以查看防火墙
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

网络爬虫

pip3 install requests    # http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
pip3 install beautifulsoup4    # http://beautifulsoup.readthedocs.io/zh_CN/latest/
爬虫的第一步，获取整个网页的HTML信息，我们已经完成
爬虫的第二步，解析HTML信息，提取我们感兴趣的内容
提取的方法有很多，例如使用 正则表达式、Xpath、Beautiful Soup等

小说下载，小说网站-笔趣看：URL：http://www.biqukan.com/
《一念永恒》小说的第一章内容，URL：http://www.biqukan.com/1_1094/5403177.html
右击网页，可以审查网站元素，来获得信息

from bs4 import BeautifulSoup
import requests
if __name__ == "__main__":
    target = 'http://www.biqukan.com/1_1094/5403177.html'
    req = requests.get(url = target) 
    html = req.text
    bf = BeautifulSoup(html)  # 会返回一个对象
    texts = bf.find_all('div', class_ = 'showtxt')  # find_all方法会在对象中
    print(texts[0].text.replace('\xa0'*8,'\n\n'))


[Unit]
Description=PostgreSQL database server
After=network.target

[Service]
Type=forking

User=postgres
Group=postgres

# Location of database directory
Environment=PGDATA=/home/pgsql_data
Environment=PGLOGS=/home/pgsql_logs


# Where to send early-startup messages from the server (before the logging
# options of postgresql.conf take effect)
# This is normally controlled by the global default set by systemd
# StandardOutput=syslog

# Disable OOM kill on the postmaster
OOMScoreAdjust=-1000

ExecStart=/opt/pgsql/current/bin/pg_ctl -D ${PGDATA} -l ${PGLOGS}/postgresql.log start
ExecStop=/opt/pgsql/current/bin/pg_ctl -D ${PGDATA} stop -m fast

# Do not set any timeout value, so that systemd will not kill postmaster
# during crash recovery.
TimeoutSec=300

[Install]
WantedBy=multi-user.target

pip3 install pymysql -i http://mirrors.tools.huawei.com/pypi/simple/ --trusted-host mirrors.tools.huawei.com

# encoding:utf-8
import json
dic = {"a": "null", "b": "false", "c": 1}


js = json.dumps(dic, sort_keys=True, indent=4, separators=(',', ':'))
print(js)


本文转载自以下链接:https://www.makcyun.top/web_scraping_withpython8.html

目的是万一博主网站无法访问到的话自己需要学习的东西可就不存在了.

 

本文需要学习的地方,使用三种不同的方式爬取需要登录才能获取数据的网站数据

POST 请求方法：需要在后台获取登录的 URL并填写请求体参数，然后 POST 请求登录，相对麻烦；
添加 Cookies 方法：先登录将获取到的 Cookies 加入 Headers 中，最后用 GET 方法请求登录，这种最为方便；
Selenium 模拟登录：代替手工操作，自动完成账号和密码的输入，简单但速度比较慢。
 

 

对于很多要先登录的网站来说，模拟登录往往是爬虫的第一道坎。本文介绍 POST 请求登录、获取 Cookies 登录、Seleium 模拟登录三种方法。

摘要： 在进行爬虫时，除了常见的不用登录就能爬取的网站，还有一类需要先登录的网站。比如豆瓣、知乎，以及上一篇文章中的桔子网。这一类网站又可以分为：只需输入帐号密码、除了帐号密码还需输入或点击验证码等类型。本文以只需输入账号密码就能登录的桔子网为例，介绍模拟登录常用的 3 种方法。

POST 请求方法：需要在后台获取登录的 URL并填写请求体参数，然后 POST 请求登录，相对麻烦；
添加 Cookies 方法：先登录将获取到的 Cookies 加入 Headers 中，最后用 GET 方法请求登录，这种最为方便；
Selenium 模拟登录：代替手工操作，自动完成账号和密码的输入，简单但速度比较慢。
下面，我们用代码分别实现上述 3 种方法。

1. 目标网页
这是我们要获取内容的网页：

http://radar.itjuzi.com/investevent



这个网页需要先登录才能看到数据信息，登录界面如下：



可以看到，只需要输入账号和密码就可以登录，不用输验证码，比较简单。下面我们利用一个测试账号和密码，来实现模拟登录。

2. POST 提交请求登录
首先，我们要找到 POST 请求的 URL。

有两种方法，第一种是在网页 devtools 查看请求，第二种是在 Fiddler 软件中查看。

先说第一种方法。



在登录界面输入账号密码，并打开开发者工具，清空所有请求，接着点击登录按钮，这时便会看到有大量请求产生。哪一个才是 POST 请求的 URL呢？这个需要一点经验，因为是登录，所以可以尝试点击带有 「login」字眼的请求。这里我们点击第四个请求，在右侧 Headers 中可以看到请求的 URL，请求方式是 POST类型，说明 URL 找对了。



接着，我们下拉到 Form Data，这里有几个参数，包括 identify 和 password，这两个参数正是我们登录时需要输入的账号和密码，也就是 POST 请求需要携带的参数。



参数构造非常简单，接下来只需要利用 Requests.post 方法请求登录网站，然后就可以爬取内容了。

下面，我们尝试用 Fiddler 获取 POST 请求。

如果你对 Fiddler 还不太熟悉或者没有电脑上没有安装，可以先了解和安装一下。

Fiddler 是位于客户端和服务器端的 HTTP 代理，也是目前最常用的 HTTP 抓包工具之一 。 它能够记录客户端和服务器之间的所有 HTTP 请求，可以针对特定的 HTTP 请求，分析请求数据、设置断点、调试 web 应用、修改请求的数据，甚至可以修改服务器返回的数据，功能非常强大，是 web 调试的利器。

Fiddler 下载地址：

https://www.telerik.com/download/fiddler

使用教程：

https://zhuanlan.zhihu.com/p/37374178

http://www.hangge.com/blog/cache/detail_1697.html

下面，我们就通过 Fiddler 截取登录请求。

当点击登录时，官场 Fiddler 页面，左侧可以看到抓取了大量请求。通过观察，第15个请求的 URL中含有「login」字段，很有可能是登录的 POST 请求。我们点击该请求，回到右侧，分别点击「inspectors」、「Headers」，可以看到就是 POST 请求，该 URL 和上面的方法获取的 URL 是一致的。



接着，切换到右侧的 Webforms 选项，可以看到 Body 请求体。也和上面方法中得到的一致。



获取到 URL 和请求体参数之后，下面就可以开始用 Requests.post 方法模拟登录了。

代码如下：

import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
data = {
    'identity':'irw27812@awsoo.com',   
    'password':'test2018',
}
url ='https://www.itjuzi.com/user/login?redirect=&flag=&radar_coupon='
session = requests.Session()
session.post(url,headers = headers,data = data)
# 登录后，我们需要获取另一个网页中的内容
response = session.get('http://radar.itjuzi.com/investevent',headers = headers)
print(response.status_code)
print(response.text)
使用 session.post 方法提交登录请求，然后用 session.get 方法请求目标网页，并输出 HTML代码。可以看到，成功获取到了网页内容。



下面，介绍第 2 种方法。

3. 获取 Cookies，直接请求登录
上面一种方法，我们需要去后台获取 POST 请求链接和参数，比较麻烦。下面，我们可以尝试先登录，获取 Cookie，然后将该 Cookie 添加到 Headers 中去，然后用 GET 方法请求即可，过程简单很多。

代码如下：

import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Cookie': '你的cookie',
}
url = 'https://www.itjuzi.com/user/login?redirect=&flag=&radar_coupon='
session = requests.Session()
response = session.get('http://radar.itjuzi.com/investevent', headers=headers)

print(response.status_code)
print(response.text)
可以看到，添加了 Cookie 后就不用再 POST 请求了，直接 GET 请求目标网页即可。可以看到，也能成功获取到网页内容。

Cookie的使用

用 Python 来登录网站, 用Cookies记录登录信息, 然后就可以抓取登录之后才能看到的信息。

什么是cookies?

Cookie，指某些网站为了辨别用户身份、进行session跟踪而储存在用户本地终端上的数据（通常经过加密）。
比如说有些网站需要登录后才能访问某个页面，在登录之前，你想抓取某个页面内容是不允许的。那么我们可以利用Urllib库保存我们登录的Cookie，然后再抓取其他页面就达到目的了。
opener的概念
当你获取一个URL你使用一个opener(一个urllib2.OpenerDirector的实例)。在前面，我们都是使用的默认的opener，也就是urlopen。

urlopen是一个特殊的opener，可以理解成opener的一个特殊实例，传入的参数仅仅是url，data，timeout。
如果我们需要用到Cookie，只用这个opener是不能达到目的的，所以我们需要创建更一般的opener来实现对Cookie的设置。
Cookielib
cookielib模块的主要作用是提供可存储cookie的对象，以便于与urllib2模块配合使用来访问Internet资源。Cookielib模块非常强大，我们可以利用本模块的CookieJar类的对象来捕获cookie并在后续连接请求时重新发送，比如可以实现模拟登录功能。该模块主要的对象有CookieJar、FileCookieJar、MozillaCookieJar、LWPCookieJar。
它们的关系：CookieJar —-派生—->FileCookieJar  —-派生—–>MozillaCookieJar和LWPCookieJar

使用cookie登录的步骤
1）获取Cookie保存到变量

import urllib.request
import http.cookiejar

URL_ROOT = r'http://d.weibo.com/'

cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
opener = urllib.request.build_opener(handler)  # 通过handler来构建opener

response = opener.open(URL_ROOT)  # 此处的open方法同urllib2的urlopen方法，也可以传入request

for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)
我们使用以上方法将cookie保存到变量中，然后打印出了cookie中的值，运行结果如下
Name = YF-Page-G0

Value = dc8d8d4964cd93a7c3bfa7640c1bd10c

Note:py3中opener也可以这样使用：

request = urllib.request.Request(URL_ROOT, postdata, headers)
response = opener.open(request)
或者：

urllib.request.install_opener(opener)
request = urllib.request.Request(URL_ROOT, postdata, headers)
response = urllib.request.urlopen(request)2）保存Cookie到文件上面我们将cookie保存到了cookie这个变量中，如果我们想将cookie保存到文件中该怎么做呢？这时，我们就要用到FileCookieJar这个对象了，在这里我们使用它的子类MozillaCookieJar来实现Cookie的保存
 

import urllib.request, urllib.parse, urllib.error
import http.cookiejar

URL_ROOT = 'http://www.jobbole.com/login/'
values = {'name': '******', 'password': '******'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent}

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.LWPCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(URL_ROOT, postdata, headers)
try:
    response = opener.open(request)
except urllib.error.URLError as e:
    print(e.reason)

cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)
 

Note: 

1. 不同cookie写入文件方法的解释：

FileCookieJar(filename)：创建FileCookieJar实例，检索cookie信息并将信息存储到文件中，filename是文件名。

MozillaCookieJar(filename)：创建与Mozilla cookies.txt文件兼容的FileCookieJar实例。

LWPCookieJar(filename)：创建与libwww-perl Set-Cookie3文件兼容的FileCookieJar实例。

2. save方法的两个参数的官方解释：

ignore_discard: save even cookies set to be discarded. 即使cookies将被丢弃也将它保存下来

ignore_expires: save even cookies that have expiredThe file is overwritten if it already exists.如果在该文件中cookies已经存在，则覆盖原文件写入

3. python3中如果直接使用http.cookiejar.CookieJar(filename)的方式会出错：self._policy._now = self._now = int(time.time()) AttributeError: 'str' object has no attribute '_now'。注意要将CookieJar改为LWPCookieJar。

3）从文件中获取Cookie并访问
那么我们已经做到把Cookie保存到文件中了，如果以后想使用，可以利用下面的方法来读取cookie并访问网站，感受一下

import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar

cookie_filename = 'cookie_jar.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

get_url = 'http://www.jobbole.com/'  # 利用cookie请求访问另一个网址
get_request = urllib.request.Request(get_url)
get_response = opener.open(get_request)
print(get_response.read().decode())

下面介绍第 3 种方法。

4. Selenium 模拟登录
这个方法很直接，利用 Selenium 代替手动方法去自动输入账号密码然后登录就行了。

关于 Selenium 的使用，在之前的一篇文章中有详细介绍，如果你不熟悉可以回顾一下：

https://www.makcyun.top/web_scraping_withpython5.html

代码如下：

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
browser = webdriver.Chrome()
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 10) # 等待加载10s

def login():
    browser.get('https://www.itjuzi.com/user/login')
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="create_account_email"]')))
    input.send_keys('irw27812@awsoo.com')
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="create_account_password"]')))
    input.send_keys('test2018')
    submit = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="login_btn"]')))
    submit.click() # 点击登录按钮
    get_page_index()

def get_page_index():
    browser.get('http://radar.itjuzi.com/investevent')
    try:
        print(browser.page_source)  # 输出网页源码
    except Exception as e:
        print(str(e))
login()
这里，我们在网页中首先定位了账号节点位置：'//*[@id="create_account_email"]'，然后用 input.send_keys 方法输入账号，同理，定位了密码框位置并输入了密码。接着定位 登录 按钮的位置：//*[@id="login_btn"]，然后用 submit.click() 方法实现点击登录按钮操作，从而完成登录。可以看到，也能成功获取到网页内容。



以上就是模拟需登录网站的几种方法。当登录进去后，就可以开始爬取所需内容了。

5. 总结：
本文分别实现了模拟登录的 3 种操作方法，建议优先选择第 2 种，即先获取 Cookies 再 Get 请求直接登录的方法。
本文模拟登录的网站，仅需输入账号密码，不需要获取相关加密参数，比如 Authenticity_token ，同时也无需输入验证码，所以方法比较简单。但是还有很多网站模拟登录时，需要处理加密参数、验证码输入等问题。后续将会介绍

tomcat 日志配置
https://blog.csdn.net/WEB_CEO_INFO/article/details/1775895?utm_medium=distribute.pc_relevant.none-task-blog-searchFromBaidu-6.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-searchFromBaidu-6.control
https://blog.csdn.net/qiuyinthree/article/details/72677173
Tomcat日志设定
Tomcat日志概述
Tomcat 日志信息分为两类：

运行中的日志，它主要记录运行的一些信息，尤其是一些异常错误日志信息。
访问日志信息，它记录的访问的时间,IP,访问的资料等相关信息。
访问日志
启用访问日志
默认 tomcat 不记录访问日志，如下方法可以使 tomcat 记录访问日志

编辑${catalina}/conf/server.xml 文件(注:{catalina}是tomcat的安装目录)，把以下的注释 (<!-- -->) 去掉即可。

 <!--
        <Valve className="org.apache.catalina.valves.AccessLogValve"
         directory="logs"  prefix="localhost_access_log." suffix=".txt"
         pattern="common" resolveHosts="false"/>
  -->
配置tomcat写出更详细的日志
通过对 2.1 示例中 pattern 项的修改，可以改变日志输出的内容。

该项值可以为： common 与 combined ，这两个预先设置好的格式对应的日志输出内容如下：

common 的值： %h %l %u %t %r %s %b
combined 的值： %h %l %u %t %r %s %b %{Referer}i %{User-Agent}i
pattern 也可以根据需要自由组合 , 例如 pattern="%h %l"

对 于各 fields 字段的含义请参照:

http://tomcat.apache.org/tomcat-6.0-doc/config/valve.html 中的 Access Log Valve 项。

%a - Remote IP address
%A - Local IP address
%b - Bytes sent, excluding HTTP headers, or '-' if zero
%B - Bytes sent, excluding HTTP headers
%h - Remote host name (or IP address if resolveHosts is false)
%H - Request protocol
%l - Remote logical username from identd (always returns '-')
%m - Request method (GET, POST, etc.)
%p - Local port on which this request was received
%q - Query string (prepended with a '?' if it exists)
%r - First line of the request (method and request URI)
%s - HTTP status code of the response
%S - User session ID
%t - Date and time, in Common Log Format
%u - Remote user that was authenticated (if any), else '-'
%U - Requested URL path
%v - Local server name
%D - Time taken to process the request, in millis
%T - Time taken to process the request, in seconds
%I - current request thread name (can compare later with stacktraces)
%{xxx}i for incoming headers
%{xxx}o for outgoing response headers
%{xxx}c for a specific cookie
%{xxx}r xxx is an attribute in the ServletRequest
%{xxx}s xxx is an attribute in the HttpSession
运行日志
日志类型与级别
Tomcat日志分为5类：catalina 、localhost 、manager 、admin 、host-manager
日志的级别分为7种：SEVERE (highest value) > WARNING > INFO > CONFIG > FINE > FINER > FINEST (lowest value)
设定日志级别
修改 conf/logging.properties 中的内容，设定某类日志的级别

示例：

设置 catalina 日志的级别为： FINE
1catalina.org.apache.juli.FileHandler.level = FINE
禁用 catalina 日志的输出：
1catalina.org.apache.juli.FileHandler.level = OFF
输出 catalina 所有的日志消息均输出：
1catalina.org.apache.juli.FileHandler.level = ALL
应用程序日志或系统日志
输出详细系统日志
使用Log4j输出详细系统日志信息，快速诊断启动故障

此例可弥补tomcat启动异常时输出的错误信息不足的问题，使用commons-logging和log4j搭配输出详尽的日志信息。

以window环境下tomcat5.5.27为例：

tomcat解压目录为：E: /tomcat5.5
设置环境变量：CATALINA_HOME=E: /tomcat5.5
下载 log4j 与 commons-logging
Log4j 下载地址：http://logging.apache.org/log4j/1.2/download.html
Commons-logging 下载地址：http://apache.freelamp.com/commons/logging/binaries/commons-logging-1.1.1-bin.zip
本例将 commons-logging-1.1.1.jar 与 log4j-1.2.15.jar 放在 %TOMCAT_HOME%/bin 目录下（可根据需要放置在其位置）
在 %TOMCAT_HOME%/bin 目录下新建两个文件 commons-logging.properties 、log4j.properties
commons-logging.properties 文件内容如下：
org.apache.commons.logging.Log=org.apache.commons.logging.impl.Log4JLogger
log4j.properties 文件内容如下：
log4j.rootLogger=WARN,stdout,file

## 日志直接输出到控制台 ###

log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.Target=System.out
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%d{ABSOLUTE} %l - %m%n

## 日志输出到文件 SystemOut.log ###
log4j.appender.file=org.apache.log4j.FileAppender
log4j.appender.file.File=E: /tomcat5.5/ logs/SystemOut.log
log4j.appender.file.Append=false
log4j.appender.file.layout=org.apache.log4j.PatternLayout
log4j.appender.file.layout.ConversionPattern=%d{ABSOLUTE} %l - %m%n
该配置文件可详细参照：http://www.minaret.biz/tips/tomcatLogging.html#log4j_properties
修改 catalina.bat 文件
将
set CLASSPATH=%CLASSPATH%;%CATALINA_HOME%/bin/bootstrap.jar
替换为
set CLASSPATH=%CLASSPATH%;%CATALINA_HOME%/bin/bootstrap.jar;%CATALINA_HOME%/bin/commons-logging-1.1.jar;%CATALINA_HOME%/bin/log4j-1.2.13.jar;%CATALINA_HOME%/bin
通过startup.bat启动就会用log4j来输出启动日志了。
在E:/tomcat5.5/logs/SystemOut.log文件中查看输出的日志
应用程序中使用log4j
从如下网址下载log4j：http://logging.apache.org/log4j/1.2/download.html
创建Java工程。
添加log4j.jar到工程的编译路径下。
创建名称为log4j.properties的文件，写入如下内容：
### direct log messages to stdout ###
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.Target=System.out
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%d{ABSOLUTE} %5p %c{1}:%L - %m%n
log4j.rootLogger=debug, stdout
创建类并添加如下内容：
import org.apache.log4j.Logger;
public class LogClass {
        private static org.apache.log4j.Logger log = Logger
                        .getLogger (LogClass. class );
        public static void main(String[] args) {
                log .trace( "Trace" );
                log .debug( "Debug" );
                log .info( "Info" );
                log .warn( "Warn" );
                log .error( "Error" );
                log .fatal( "Fatal" );
        }
}
编译运行，可在控制台中看到如下内容：
10:38:24,797 DEBUG LogClass:11 - Debug
10:38:24,812  INFO LogClass:12 - Info
10:38:24,812  WARN LogClass:13 - Warn
10:38:24,812 ERROR LogClass:14 - Error
10:38:24,812 FATAL LogClass:15 - Fatal
根据级别控制日志输出内容：
将 log4j.rootLogger= debug , stdout 变更为 log4j.rootLogger=Warn, stdout

输出内容如下：

10:41:15,488  WARN LogClass:13 - Warn
10:41:15,504 ERROR LogClass:14 - Error
10:41:15,504 FATAL LogClass:15 – Fatal
更改日志输出内容
log4j.rootCategory=INFO, stdout , R
此句为将等级为INFO的日志信息输出到stdout和R这两个目的地。

等级可分为OFF、FATAL、ERROR、WARN、INFO、DEBUG、ALL，如果配置OFF则不打出任何信息，如果配置为INFO这样只显示INFO,WARN,ERROR的log信息，而DEBUG信息不会被显示。

log4j.appender.stdout=org.apache.log4j.ConsoleAppender
此句为定义名为stdout的输出端是哪种类型，可以是：

org.apache.log4j.FileAppender	文件
org.apache.log4j.DailyRollingFileAppender	每天产生一个日志文件
org.apache.log4j.RollingFileAppender	文件大小到达指定尺寸的时候产生一个新的文件
org.apache.log4j.WriterAppender	将日志信息以流格式发送到任意指定的地方
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
此句为定义名为stdout的输出端的layout是哪种类型

org.apache.log4j.HTMLLayout	以HTML表格形式布局
org.apache.log4j.PatternLayout	可以灵活地指定布局模式
org.apache.log4j.SimpleLayout	包含日志信息的级别和信息字符串
org.apache.log4j.TTCCLayout	包含日志产生的时间、线程、类别等等信息
log4j.appender.stdout.layout.ConversionPattern= [QC] %p [%t] %C.%M(%L) | %m%n
如果使用 pattern 布局就要指定的打印信息的具体格式 ConversionPattern ，打印参数如下：

具体的设定参照：http://logging.apache.org/log4j/1.2/apidocs/org/apache/log4j/PatternLayout.html

%m	输出代码中指定的消息
%p	输出优先级，即DEBUG，INFO，WARN，ERROR，FATAL
%r	输出自应用启动到输出该log信息耗费的毫秒数
%c	输出所属的类目，通常就是所在类的全名
%t	输出产生该日志事件的线程名
%n	输出一个回车换行符，Windows平台为“rn”，Unix平台为“n”
%d	输出日志时间点的日期或时间，默认格式为ISO8601，也可以指定格式，如:%d{yyyymmddHH:mm:ss,SSS},输出:2002101822:10:28,921
%l	输出日志事件的发生位置，包括类目名、发生的线程，以及在代码中的行数。
[QC]	是log信息的开头，可以为任意字符，一般为项目简称。
	
