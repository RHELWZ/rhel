#!/bin/bash
cecho () {
   echo -e "\033[$1m$2\033[0m"
}
a=1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM
m=${#a}
for i in {1..8}
do
x=$[RANDOM%m]
y=${a:x:1}
q=$y$q
done
read -t5 -p "输入用户名:" t || exit
[ -z "$t" ] && sleep 1 && cecho 33 "不能为空"  && exit
while [ "$b" != "y" ] && [ "$b" != "n" ] && [ "$b" != "Y" ] && [ "$b" != "N" ]
do
sleep 1
read -p "是否使用随机生成密码`cecho 35 $q`  y/Y|n/N:" b
done
useradd $t  &> /dev/null
  if [ "$b" == "y" ] || [ "$b" == "Y" ]; then
   echo "$q" | passwd --stdin $t &> /dev/null
  else
   stty -echo
   read -p "请输入`cecho 33 $t`用户密码：" m
   stty echo
   echo "${m:-123456}" | passwd --stdin $t &> /dev/null
   cecho 31 "   请稍等" && sleep 1
  fi
cecho 32 "恭喜！用户创建成功"
