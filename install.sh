#!/bin/bash

echo "You may need to tweak .flashenv and db/setup.sh manually"
sudo apt-get -qq coreutils
mypath=`realpath $0`
mybase=`dirname $mypath`
user=`whoami`
echo "Assume your database user name is: $user"
read -p "Enter database password and press [ENTER]: " dbpasswd

secret=`tr -dc 'a-z0-9-_' < /dev/urandom | head -c50`
cd $mybase
cp -f flaskenv-template.env .flaskenv
sed -i "s/default_secret/'$secret'/g" .flaskenv
sed -i "s/default_db_user/$user/g" .flaskenv
sed -i "s/default_db_password/$dbpasswd/g" .flaskenv

sudo apt-get -qq update
sudo apt-get -qq --yes install python3-virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
db/setup.sh
