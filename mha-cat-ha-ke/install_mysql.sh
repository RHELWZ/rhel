#!/bin/bash
ls /var/log/mysqld.log &> /dev/null
if [ `echo $?` -ne 0 ]; then
yum -y install /root/mysql/* &> /dev/null
systemctl enable --now mysqld
n=`sed -n '/localhost:/s/.*localhost://p' /var/log/mysqld.log`
mysqladmin -uroot -p`echo $n` password '123qqq...A' &> /dev/null
else
exit 
fi
