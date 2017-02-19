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
