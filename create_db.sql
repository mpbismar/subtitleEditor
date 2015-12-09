DELETE USER IF EXISTS `django`;
CREATE USER `django`@`localhost` IDENTIFIED BY `password`;
DROP DATABASE IF EXISTS `sub_db`;
CREATE DATABASE `sub_db`
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

USE 'mysql';
GRANT ALL PRIVILEGES ON sub_db.* TO 'django'@'localhost' IDENTIFIED BY 'password'

WITH GRANT OPTION;
FLUSH PRIVILEGES;

