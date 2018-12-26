#!/bin/sh

echo deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main >> /etc/apt/sources.list.d/pgdg.list
wget --no-check-certificate https://www.postgresql.org/media/keys/ACCC4CF8.asc
apt-key add ACCC4CF8.asc
apt-get update
apt-get -y install postgresql-9.5  

# variable: database|user name - mydb|root
su - postgres bash -c "psql -c \"CREATE USER root WITH PASSWORD 'password';\""
su - postgres bash -c "psql -c \"CREATE DATABASE root;\""
su - postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE root TO root;\""
su - postgres bash -c "psql -c \"CREATE DATABASE mydb;\""
su - postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE mydb TO root;\""
su - postgres bash -c "psql -c \"ALTER USER root SUPERUSER;\""

#rm -r /opt/edison

apt-get -y install python-psycopg2
python /root/power_monitoring/create_table.py
mv /root/power_monitoring/on_boot.sh /etc/init.d/
chmod +x /etc/init.d/on_boot.sh
update-rc.d on_boot.sh defaults

mv /root/power_monitoring/sketch.elf /sketch/
chmod +x /sketch/sketch.elf


#apt-get -y install python-requests
#python /root/power_monitoring/add_line_middle.py
cd /root/power_monitoring/requests
python setup.py install

cd /root/power_monitoring/python-firebase-master
python setup.py install




