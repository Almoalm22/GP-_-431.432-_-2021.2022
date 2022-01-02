CREATE DATABASE  IF NOT EXISTS `wd_cctv` ;
USE `wd_cctv`;

DROP TABLE IF EXISTS `camera`;

CREATE TABLE `camera` (
  `c_id` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(11) NOT NULL,
  `c_location` varchar(255) NOT NULL,
  PRIMARY KEY (`c_id`)
);

INSERT INTO `camera` VALUES (1,'webcam','MyPC');

DROP TABLE IF EXISTS `object`;

CREATE TABLE `object` (
  `ob_id` int NOT NULL AUTO_INCREMENT,
  `ob_kind` varchar(45) NOT NULL,
  `ob_name` varchar(11) NOT NULL,
  PRIMARY KEY (`ob_id`)
);


DROP TABLE IF EXISTS `photo`;

CREATE TABLE `photo` (
  `p_id` int NOT NULL AUTO_INCREMENT,
  `c_id` int NOT NULL,
  `u_id` int NOT NULL,
  `ob_id` int NOT NULL,
  `p_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `p_photo` blob NOT NULL,
  PRIMARY KEY (`p_id`),
  KEY `id_user` (`u_id`),
  KEY `c_id` (`c_id`),
  KEY `ob_id` (`ob_id`),
  CONSTRAINT `c_id` FOREIGN KEY (`c_id`) REFERENCES `camera` (`c_id`),
  CONSTRAINT `id_user` FOREIGN KEY (`u_id`) REFERENCES `user` (`u_id`),
  CONSTRAINT `ob_id` FOREIGN KEY (`ob_id`) REFERENCES `object` (`ob_id`)
);


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `u_id` int NOT NULL AUTO_INCREMENT,
  `u_name` varchar(11) NOT NULL,
  `u_password` text NOT NULL,
  `u_email` varchar(255) NOT NULL,
  `u_phone` int NOT NULL,
  `u_shift` int NOT NULL,
  `u_admination` tinyint NOT NULL,
  PRIMARY KEY (`u_id`)
);

INSERT INTO `user` VALUES (1,'Admin','123456','admin@wd-cctv.com',566666666,1,1);
