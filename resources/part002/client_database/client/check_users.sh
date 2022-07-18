#!/bin/sh
echo 'SELECT user,host,password FROM user WHERE (user="root" AND host="localhost");' | mysql -u root -proot -h database mysql
echo 'SELECT user,host,password FROM user WHERE (user="testuser");' | mysql -u root -proot -h database mysql

