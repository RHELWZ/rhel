#!/bin/bash
#判断ip类别，指定范围的ping    
cecho () {
 echo -e "\033[$1m$2\033[0m"
}         
x=0
y=0
read -p "请输入要测试的网段/子网掩码：" p
ip1=${p#*/}          #ip1为子网掩码
while [ "$ip1" != "8" ] && [ "$ip1" != "16" ] && [ "$ip1" != "24" ] 
do
[ $? -eq 0] && echo "子网掩码类型不正确"
sleep 1
read -p "请输入要测试的网段/子网掩码：" p
ip1=${p#*/}          
done
if [ "$ip1" -eq 8 ] ; then   #ip2为网络位
ip2=${p%%.*}
read -p "输入第1个主机位始/末范围：" n
n1=${n%/*};n2=${n#*/}
read -p "输入第2个主机位始/末范围：" m
m1=${m%/*};m2=${m#*/}
read -p "输入第3个主机位始/末范围：" k
k1=${k%/*};k2=${k#*/}
for i in $(seq $n1 $n2)
do
  for l in $(seq $m1 $m2)
  do
     for s in $(seq $k1 $k2)
     do
       ping -c 3 -i 0.2 -W 1 $ip2.$i.$l.$s > /dev/null
       if [ $? -eq 0 ] ; then
         echo "`cecho 32 $ip2.$i.$l.$s` 能通"
         let x++
       else
         echo "`cecho 31 $ip2.$i.$l.$s` 没通"
         let y++
       fi
    done
  done
done
elif [ "$ip1" -eq 16 ] ; then
t=${p%.*};ip2=${t%.*}
read -p "输入第1个主机位始/末范围：" m
m1=${m%/*};m2=${m#*/}
read -p "输入第2个主机位始/末范围：" k
k1=${k%/*};k2=${k#*/}
for l in $(seq $m1 $m2)
  do
     for s in $(seq $k1 $k2)
     do
       ping -c 3 -i 0.2 -W 1 $ip2.$l.$s > /dev/null
       if [ $? -eq 0 ] ; then
         echo "`cecho 32 $ip2.$l.$s` 能通"
         let x++
       else
         echo "`cecho 31 $ip2.$l.$s` 没通"
         let y++
       fi
    done
done
else
ip2=${p%.*} 
read -p "输入第1个主机位始/末范围：" k
k1=${k%/*};k2=${k#*/}
for s in $(seq $k1 $k2)
do
       ping -c 3 -i 0.2 -W 1 $ip2.$s > /dev/null
       if [ $? -eq 0 ] ; then
         echo "`cecho 32 $ip2.$s` 能通"
         let x++
       else
         echo "`cecho 31 $ip2.$s` 没通"
         let y++
       fi
done
fi
echo "$x台通了，$y台不通"