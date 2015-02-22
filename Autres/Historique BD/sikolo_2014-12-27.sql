# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Hôte: localhost (MySQL 5.6.21)
# Base de données: sikolo
# Temps de génération: 2014-12-27 00:27:00 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Affichage de la table class
# ------------------------------------------------------------

DROP TABLE IF EXISTS `class`;

CREATE TABLE `class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `id_classtype` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Class_ClassType1_idx` (`id_classtype`),
  CONSTRAINT `fk_Class_ClassType1` FOREIGN KEY (`id_classtype`) REFERENCES `ClassType` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table classtype
# ------------------------------------------------------------

DROP TABLE IF EXISTS `classtype`;

CREATE TABLE `classtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table comment
# ------------------------------------------------------------

DROP TABLE IF EXISTS `comment`;

CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(45) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_exam` int(11) NOT NULL,
  `comment` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`,`date`,`id_user`,`id_exam`),
  KEY `fk_Comment_User1_idx` (`id_user`),
  KEY `fk_Comment_Exam1_idx` (`id_exam`),
  CONSTRAINT `FKIDX_COMMENT_EXAM` FOREIGN KEY (`id_exam`) REFERENCES `exam` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FKIDX_COMMENT_USER` FOREIGN KEY (`id_user`) REFERENCES `User` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table concern
# ------------------------------------------------------------

DROP TABLE IF EXISTS `concern`;

CREATE TABLE `concern` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `exam_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `matter_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`exam_id`,`class_id`,`matter_id`),
  KEY `fk_concern_Exam1_idx` (`exam_id`),
  KEY `fk_Concern_Class1_idx` (`class_id`),
  KEY `fk_Concern_Matter1_idx` (`matter_id`),
  CONSTRAINT `FKIDX_CONCERN_CLASS` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FKIDX_CONCERN_EXAM` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FKIDX_CONCERN_MATTER` FOREIGN KEY (`matter_id`) REFERENCES `matter` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table correction
# ------------------------------------------------------------

DROP TABLE IF EXISTS `correction`;

CREATE TABLE `correction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table course
# ------------------------------------------------------------

DROP TABLE IF EXISTS `course`;

CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `matter_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`matter_id`),
  KEY `FKIDXmatter` (`matter_id`),
  CONSTRAINT `fk_Coursematter` FOREIGN KEY (`matter_id`) REFERENCES `matter` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table exam
# ------------------------------------------------------------

DROP TABLE IF EXISTS `exam`;

CREATE TABLE `exam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table matter
# ------------------------------------------------------------

DROP TABLE IF EXISTS `matter`;

CREATE TABLE `matter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table propose
# ------------------------------------------------------------

DROP TABLE IF EXISTS `propose`;

CREATE TABLE `propose` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `id_exam` int(11) NOT NULL,
  `id_correction` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  PRIMARY KEY (`id`,`date`,`id_exam`,`id_correction`,`id_user`),
  KEY `fk_Propose_Exam1_idx` (`id_exam`),
  KEY `fk_Propose_Correction1_idx` (`id_correction`),
  KEY `fk_Propose_User1_idx` (`id_user`),
  CONSTRAINT `FKIDX_PROPOSE_CORRECTION` FOREIGN KEY (`id_correction`) REFERENCES `Correction` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FKIDX_PROPOSE_EXAM` FOREIGN KEY (`id_exam`) REFERENCES `exam` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FKIDX_PROPOSE_USER` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table read
# ------------------------------------------------------------

DROP TABLE IF EXISTS `read`;

CREATE TABLE `read` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `mark` decimal(2,0) NOT NULL,
  `id_exam` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  PRIMARY KEY (`id`,`id_user`,`id_exam`,`date`),
  KEY `fk_Read_Exam1_idx` (`id_exam`),
  KEY `fk_Read_User1_idx` (`id_user`),
  CONSTRAINT `FKIDX_READ_EXAM` FOREIGN KEY (`id_exam`) REFERENCES `exam` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FKIDX_READ_USER` FOREIGN KEY (`id_user`) REFERENCES `User` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Affichage de la table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `pseudo` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
