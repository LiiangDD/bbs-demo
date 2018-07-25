# 1. 拉代码到 /var/www/coolwater
# 2. 执行 bash deploy.sh

set -ex
deploy_directory=/var/www/coolwater

# 系统设置
apt-get -y install  zsh curl ufw
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 25
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update

debconf-set-selections database_secret.conf
debconf-set-selections postfix.conf

apt-get install -y git supervisor nginx python3.6 mysql-server postfix
curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python3.6 /tmp/get-pip.py
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy Flask-Admin flask_mail

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
ln -s -f /var/www/coolwater/coolwater.conf /etc/supervisor/conf.d/coolwater.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /var/www/coolwater/coolwater.nginx /etc/nginx/sites-enabled/coolwater
chmod -R o+rwx /var/www/coolwater

#创建数据库
cd /var/www/coolwater
python3.6 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'deploy success'