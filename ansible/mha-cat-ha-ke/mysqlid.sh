#!/bin/bash
n=`ifconfig eth0 | awk -F[.] 'NR==2{print $4}' | awk '{print $1}'`
grep "server_id=$n" /etc/my.cnf
if [ `echo $?` -ne 0 ]; then
sed -i "/\[mysqld\]/a server_id=$n" /etc/my.cnf
systemctl restart mysqld
else
exit
fi

