CREATE USER IF NOT EXISTS 'debezium_user'@'%' IDENTIFIED BY 'debezium_pw';

GRANT ALL PRIVILEGES ON *.* TO 'debezium_user'@'%';

FLUSH PRIVILEGES;