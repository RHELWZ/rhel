#!/bin/bash
#服务端PXE部署
####搭建yum仓库
read -p "请输入本机ip："  ip
read -p "请再输入一次ip："  ip3
if [ $ip3 == $ip ] ; then
 echo "ip输入正确"
else
 echo "ip输入错误" && exit
fi
read -p "请输入本机子网掩码(8/16/24)："  x
if [ $x -eq 8 ] ; then
ip2=255.0.0.0
m=${ip%%.*}
ip1=$m.0.0
elif [ $x -eq 16 ] ; then
ip2=255.255.0.0
n=${ip%.*}
m=${n%.*}
ip1=$m.0
elif [ $x -eq 24 ] ; then
ip2=255.255.255.0
m=${ip%.*}
ip1=$m
else
echo "掩码不识别" && exit
fi
mkdir /dvd 
mount /dev/cdrom /dvd  &> /dev/null
rm -rf /etc/yum.repos.d/*
echo "[development]
name=kkkk
baseurl=file:///dvd
enabled=1
gpgcheck=0" > /etc/yum.repos.d/yum.repo
yum repolist  &> /dev/null
####搭建ftp更新yum仓库
yum -y install vsftpd &> /dev/null
mkdir /var/ftp/centos
echo "/dev/cdrom /var/ftp/centos iso9660 defaults 0 0" >> /etc/fstab
mount -a   &> /dev/null
umount /dvd
rm -rf /dvd
sed -i '3s/dvd/var\/ftp\/centos/' /etc/yum.repos.d/yum.repo
yum clean all  &> /dev/null
yum repolist   &> /dev/null
####安装软件部署DHCP
#ip为本机ip，ip1为网络位，ip2为掩码
yum -y install dhcp tftp-server syslinux  &> /dev/null
cat /usr/share/doc/dhcp-4.2.5/dhcpd.conf.example >> /etc/dhcp/dhcpd.conf
sed -i 's/^[^#]/#&/g' /etc/dhcp/dhcpd.conf
sed -i '52,60s/#//' /etc/dhcp/dhcpd.conf
sed -i "/^subnet/s/10.5.5/$ip1/;/^subnet/s/255.255.255.224/$ip2/" /etc/dhcp/dhcpd.conf
sed -i "/range/s/10.5.5.26 10.5.5.30/$ip1.100 $ip1.200/" /etc/dhcp/dhcpd.conf
sed -i "/ns1.internal./s/ns1.*/$ip;/" /etc/dhcp/dhcpd.conf
sed -i '/name "internal./s/.*//' /etc/dhcp/dhcpd.conf
sed -i "/option routers/s/10.5.5.1/$ip1.254/" /etc/dhcp/dhcpd.conf
sed -i '/address 10.5/s/.*//' /etc/dhcp/dhcpd.conf
sed -i "/^\s*max/a next-server $ip;" /etc/dhcp/dhcpd.conf
sed -i '/^\}/i filename "pxelinux.0";' /etc/dhcp/dhcpd.conf
####安装tftp/syslinux
yum -y install tftp-server syslinux &> /dev/null
mkdir /var/lib/tftpboot/pxelinux.cfg
cd /usr/share/syslinux
cp pxelinux.0 /var/lib/tftpboot
cd /var/ftp/centos/isolinux
cp initrd.img splash.png vesamenu.c32 vmlinuz /var/lib/tftpboot
cp isolinux.cfg /var/lib/tftpboot/pxelinux.cfg/default
####部署菜单文件
sed -i '66,120s/^[^#]/#&/'  /var/lib/tftpboot/pxelinux.cfg/default
sed -i '2s/600/60/' /var/lib/tftpboot/pxelinux.cfg/default
sed -i '/bel ^Install CentOS 7/a menu default' /var/lib/tftpboot/pxelinux.cfg/default
sed -i "/64 quiet/s/inst.*/ks=ftp:\/\/$ip\/ks.cfg/"  /var/lib/tftpboot/pxelinux.cfg/default
####重启服务
systemctl restart dhcpd tftp vsftpd
####生成应答文件
echo "#platform=x86, AMD64, 或 Intel EM64T
#version=DEVEL
# Install OS instead of upgrade
install
# Keyboard layouts
keyboard 'us'
# Root password
rootpw --iscrypted $1$v1Fg53Ja$5m4lNJvHQA3FMeXolf3xx/
# Use network installation
url --url="ftp://$ip/centos"
# System language
lang en_US
# System authorization information
auth  --useshadow  --passalgo=sha512
# Use graphical install
graphical
firstboot --disable
# Firewall configuration
selinux --disabled

# Firewall configuration
firewall --disabled
# Network information
network  --bootproto=dhcp --device=eth0
# Reboot after installation
reboot
# System timezone
timezone Africa/Abidjan
# System bootloader configuration
bootloader --location=mbr
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all --initlabel
# Disk partitioning information
part /boot --fstype="xfs" --size=500
part swap --fstype="swap" --size=500
part / --fstype="xfs" --grow --size=1
%packages
@base
%end
%post --interpreter=/bin/bash" > /var/ftp/ks.cfg
echo 'echo "1" |  passwd --stdin root  
sed -i "/auto/s/et/et net.ifnames=0 biosdevname=0/" /etc/default/grub   
b=`ls /etc/sysconfig/network-scripts/ifcfg-en*`;v=${b##*-}
mv /etc/sysconfig/network-scripts/ifcfg-{$v,eth0}
sed -i "s/$v/eth0/" /etc/sysconfig/network-scripts/ifcfg-eth0
grub2-mkconfig -o /boot/grub2/grub.cfg
rm -rf /etc/yum.repos.d/*                                       
echo "[centos7]
name=centos'  >> /var/ftp/ks.cfg
echo "baseurl=ftp://$ip/centos" >> /var/ftp/ks.cfg
echo 'enabled=1
gpgcheck=0" > /etc/yum.repos.d/yum.repo' >> /var/ftp/ks.cfg
echo 'reboot' >> /var/ftp/ks.cfg
echo "%end" >> /var/ftp/ks.cfg
setsebool ftpd_full_access=on
ss -atnulp | grep dhcpd;ss -atnulp | grep vsftpd;ss -atnulp | grep tftpd  && echo "PXE部署成功" || echo "PXE部署失败"