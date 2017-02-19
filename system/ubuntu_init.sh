"echo 输入你的email"
read y_email
"echo 输入你的名称"
read y_name
sudo apt-get install git python-pip python-dev libevent-dev build-essential python-setuptools libxml2-dev libxslt-dev openssh-server
ssh-keygen -t rsa -C "${y_email}" # ssh配置
git config --global user.name "${y_name}" # git配置
git config --global user.email "${y_email}"
# vim 配置
echo "set fileencodings=utf-8,gb2312,gbk,gb18030">>~/.vimrc
echo "set termencoding=utf-8">>~/.vimrc
echo "set number">>~/.vimrc
echo "set encoding=prc">>~/.vimrc
# 数据库
sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient-dev
sudo apt-get install mongodb
sudo apt-get install redis-server
# docker
sudo apt-get install docker.io 
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart
#supervisor 
sudo apt-get install supervisor
