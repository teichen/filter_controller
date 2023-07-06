# module setup:
export PYTHONPATH='path/to/project'

# mysql setup:
add alias in ~/.bash_profile
alias docker='/Applications/Docker.app/Contents/Resources/bin/docker'
export PATH=$PATH:/usr/local/mysql/bin
sudo /usr/local/mysql/support-files/mysql.server start
brew install rbenv/tap/openssl@1.0
ln -sfn /usr/local/Cellar/openssl@1.0/1.0.2t /usr/local/opt/openssl
mysql -u root --password -h 127.0.0.1 -P 3306

# docker mysql container setup:
sudo docker pull mysql/mysql-server:5.7.17

# mongo setup:
append to PATH in ~/.bash_profile
export PATH="/usr/local/opt/mongodb-community@4.2/bin:$PATH"

# to check database services:
docker ps
brew services list
