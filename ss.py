# coding:utf-8
__author__ = "zhou"
# create by zhou on 2019/3/19
import os
import sys
import time


# 保证bbr的开启 及 基本组件的安装
with open("/etc/sysctl.conf","r") as f:
    old_config = f.read()
if 'bbr' not in old_config:
    os.system("yum install -y epel-release git svn python-setuptools python-pip vim")  # yum rpm
    os.system('rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org')
    os.system('rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm')
    os.system("rm -rf /var/lib/yum/history/*.sqlite")
    os.system("yum --enablerepo=elrepo-kernel -y install kernel-ml kernel-ml-devel")  # install kernel
    os.system("sed -i '/GRUB_DEFAULT/s/saved/0/' /etc/default/grub && grub2-mkconfig -o"
              " /boot/grub2/grub.cfg")  # grub修改
    os.system("pip install shadowsocks")
    sysctl_config = ''''
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).

# Accept IPv6 advertisements when forwarding is enabled
net.ipv6.conf.all.accept_ra = 2
net.ipv6.conf.eth0.accept_ra = 2

net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
    '''
    with open("/etc/sysctl.conf","w") as f:
        f.write(sysctl_config)

    # 加入开启启动项
    # 端口
    port = sys.argv[1].strip()
    # 密码
    secret = sys.argv[2].strip()
    with open("/etc/rc.local", "a") as f:
        f.write("\nssserver -p %s -k %s -m rc4-md5 -d start\n" % (port, secret))
    time.sleep(10)
    os.system('reboot')
else:
    pass




