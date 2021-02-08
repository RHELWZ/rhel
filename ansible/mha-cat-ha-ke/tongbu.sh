#!/bin/bash
log=`ssh root@mha-0001 "mysql -uroot -p'123qqq...A' -e 'show master status'" | awk 'NR==2{print $1}'`
pos=`ssh root@mha-0001 "mysql -uroot -p'123qqq...A' -e 'show master status'" | awk 'NR==2{print $2}'`
mysql -uroot -p'123qqq...A' -e "change master to master_host='192.168.1.41',master_user='repluser',master_password='123qqq...A',master_log_file='$log',master_log_pos=$pos"
mysql -uroot -p'123qqq...A' -e "start slave"
