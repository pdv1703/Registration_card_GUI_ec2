#
# Cookbook:: pet_cookbook
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.
data = data_bag_item('db_data', 'db_data')
Pregnant_Admin = data['Pregnant_Admin']
Pregnant_Admin_pass = data['Pregnant_Admin_pass']

remote_user_name = data['Remote_user']
remote_user_pass = data['Remote_pass']

user 'remote' do
  password  'remote'
  home '/home/remote'
end

directory '/home/remote' do
  owner 'remote'
  group 'remote'
  mode '0755'
end

cookbook_file '/home/remote/HistoryStatistic.py' do
  source 'history_statistic.py'
end

swap_file '/mnt/swap' do
  size      1024    
end

yum_package 'yum-utils'

yum_package 'wget'

execute 'download the file using Wget' do
  command 'wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm'
  live_stream true
end

rpm_package 'epel-release-latest-7.noarch.rpm' do
  source './epel-release-latest-7.noarch.rpm'
  action :install
end

yum_package 'epel-release'
rpm_package 'ius-release-1.0-15.ius.centos7.noarch' do
  source 'https://centos7.iuscommunity.org/ius-release.rpm'
  action :install
end

yum_package 'python36u'

yum_package 'python36u-pip'

execute 'install mysql-connector==2.1.6' do
  command 'pip3.6 install mysql-connector==2.1.6'
  not_if 'pip3.6 show mysql-connector'
  live_stream true
end

execute 'install pyqt5' do
  command 'pip3.6 install pyqt5'
  not_if 'pip3.6 show PyQt5'
  live_stream true
end

execute 'install gnome desktop' do
  command 'sudo yum -y groups install "KDE Desktop" --skip-broken' #sudo yum remove mariadb-libs.x86_64
  not_if "sudo yum grouplist | sed '/^Installed Groups:/,$!d;/^Available Groups:/,$d;/^Installed Groups:/d;s/^[[:space:]]*//' | grep 'KDE Desktop'"
  live_stream true
end

execute 'allow password authentication' do
  command "sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config"
  live_stream true
end

yum_package 'xrdp'

# Make xfce4 the default window manager for RDP connections
execute 'set default window manager' do
  command 'sudo echo xfce4-session> /home/remote/.xsession'
  live_stream true
end

# Copy .xsession to the /etc/skel folder so that xfce4 is set as the default window manager for any new user accounts that are created.
execute 'set as the default window manager for any new user accounts that are created' do
  command 'sudo cp /home/remote/.xsession /etc/skel'
  live_stream true
end

# Run the sed command to update the [xrdp1] section of /etc/xrdp/xrdp.ini to allow changing of the host port you will connect to.
execute 'allow changing of the host port you will connect to' do
  command "sudo sed -i '0,/-1/s//ask-1/' /etc/xrdp/xrdp.ini"
  live_stream true
end

service "xrdp" do
  action :restart
end
