CREATE USER 'nali'@'%' IDENTIFIED BY 'nali';

GRANT ALL PRIVILEGES ON *.* TO 'nali'@'%';


CREATE DATABASE IF NOT EXISTS ip2post;

USE ip2post;

CREATE TABLE users (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE `login_attempts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_address` varchar(45) NOT NULL,
  `attempts` int(11) NOT NULL DEFAULT 0,
  `last_attempt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
)