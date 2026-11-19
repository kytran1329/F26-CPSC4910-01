-- MySQL dump 10.13  Distrib 9.6.0, for Win64 (x86_64)
--
-- Host: cpsc4910-f26.cobd8enwsupz.us-east-1.rds.amazonaws.com    Database: Team01_DB
-- ------------------------------------------------------
-- Server version	8.4.9

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ABOUT`
--

DROP TABLE IF EXISTS `ABOUT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ABOUT` (
  `SPRINT_NUM` int NOT NULL,
  `TEAM_NAME` varchar(40) DEFAULT 'Team 01 - The Fellowship of the Function',
  `START_DATE` varchar(30) DEFAULT NULL,
  `END_DATE` varchar(30) DEFAULT NULL,
  `RELE_DATE` varchar(30) DEFAULT 'December 11, 2026',
  `PROD_NAME` varchar(20) DEFAULT 'Road Reward',
  `PROD_DESC` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`SPRINT_NUM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ABOUT`
--

LOCK TABLES `ABOUT` WRITE;
/*!40000 ALTER TABLE `ABOUT` DISABLE KEYS */;
INSERT INTO `ABOUT` VALUES (1,'Team 01 - The Fellowship of the Function','September 8, 2026','September 17, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(2,'Team 01 - The Fellowship of the Function','September 15, 2026','September 24, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(3,'Team 01 - The Fellowship of the Function','September 22, 2026','October 1, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(4,'Team 01 - The Fellowship of the Function','September 29, 2026','October 8, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(5,'Team 01 - The Fellowship of the Function','October 6, 2026','October 22, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(6,'Team 01 - The Fellowship of the Function','October 20, 2026','October 29, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(7,'Team 01 - The Fellowship of the Function','October 27, 2026','November 5, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(8,'Team 01 - The Fellowship of the Function','November 3, 2026','November 12, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.'),(9,'Team 01 - The Fellowship of the Function','November 10, 2026','November 19, 2026','December 11, 2026','Road Reward','Road Reward is a driver incentive web application designed to encourage safer and better on-road performance in the trucking industry. Drivers can earn points for positive driving behavior and redeem those points for products through their sponsoring company\'s reward catalog.');
/*!40000 ALTER TABLE `ABOUT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `APPLICATIONS`
--

DROP TABLE IF EXISTS `APPLICATIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APPLICATIONS` (
  `APPLICATION_ID` int NOT NULL AUTO_INCREMENT,
  `SPONSORCOMP_ID` int NOT NULL,
  `USER_ID` int NOT NULL,
  `CREATED_DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `SPONSOR_ID` int DEFAULT NULL,
  `STATUS` varchar(20) NOT NULL DEFAULT 'Pending',
  `REASON` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`APPLICATION_ID`),
  KEY `SPONSORCOMP_ID` (`SPONSORCOMP_ID`),
  KEY `USER_ID` (`USER_ID`),
  KEY `SPONSOR_ID` (`SPONSOR_ID`),
  CONSTRAINT `APPLICATIONS_ibfk_1` FOREIGN KEY (`SPONSORCOMP_ID`) REFERENCES `SPONSORCOMP` (`SPONSORCOMP_ID`),
  CONSTRAINT `APPLICATIONS_ibfk_2` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`),
  CONSTRAINT `APPLICATIONS_ibfk_3` FOREIGN KEY (`SPONSOR_ID`) REFERENCES `SPONSOR` (`SPONSOR_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `APPLICATIONS`
--

LOCK TABLES `APPLICATIONS` WRITE;
/*!40000 ALTER TABLE `APPLICATIONS` DISABLE KEYS */;
INSERT INTO `APPLICATIONS` VALUES (1,1,3,'2026-10-01 20:13:27','2026-10-08 16:09:20',1,'Accepted',NULL),(2,1,4,'2026-10-01 20:13:27','2026-10-19 22:46:20',1,'Rejected',NULL),(3,1,5,'2026-10-01 20:13:27','2026-10-01 20:13:27',1,'Accepted',NULL),(4,2,6,'2026-10-01 20:13:27','2026-10-29 19:33:30',2,'Rejected',NULL),(5,2,8,'2026-10-01 20:13:27','2026-10-19 22:46:29',2,'Rejected',NULL),(6,1,13,'2026-10-08 16:03:45','2026-10-19 22:46:37',1,'Accepted',NULL),(7,1,12,'2026-10-08 16:04:36','2026-10-30 20:38:26',1,'Accepted',NULL),(9,2,20,'2026-10-29 17:46:02','2026-10-29 19:29:20',3,'Accepted',NULL),(10,2,21,'2026-10-29 19:38:31','2026-10-29 19:41:28',3,'Accepted',NULL),(11,2,22,'2026-10-29 23:16:52','2026-10-29 23:24:00',NULL,'Rejected','Not approved!'),(12,2,23,'2026-10-29 23:17:41','2026-10-29 23:24:06',3,'Accepted','Approved!'),(13,2,24,'2026-10-29 23:27:25','2026-10-29 23:39:16',NULL,'Rejected','Don\'t recognize this one...'),(14,2,25,'2026-10-29 23:32:26','2026-10-29 23:38:57',3,'Accepted','Is that a plane?!'),(15,2,26,'2026-10-29 23:42:19','2026-10-29 23:42:39',3,'Rejected','trying again'),(16,1,27,'2026-10-30 21:40:52','2026-11-13 18:30:14',1,'Accepted',NULL),(17,2,33,'2026-11-04 14:09:00','2026-11-09 14:39:43',3,'Rejected','No.'),(19,1,33,'2026-11-05 12:55:38','2026-11-05 12:55:38',NULL,'Pending',NULL),(20,2,34,'2026-11-06 19:22:26','2026-11-06 19:22:26',NULL,'Pending',NULL),(21,1,34,'2026-11-06 19:23:17','2026-11-06 19:24:02',1,'Accepted',NULL),(22,1,35,'2026-11-09 14:14:08','2026-11-09 14:17:27',1,'Accepted',NULL),(23,2,36,'2026-11-09 14:16:09','2026-11-09 14:21:57',3,'Accepted','Scientists reveal the Hi'),(24,2,6,'2026-11-09 14:16:43','2026-11-09 14:16:43',NULL,'Pending',NULL),(25,2,37,'2026-11-09 14:19:47','2026-11-09 14:24:42',2,'Accepted','yer'),(26,1,38,'2026-11-16 15:02:15','2026-11-16 15:03:21',1,'Accepted',NULL),(27,2,38,'2026-11-16 15:02:40','2026-11-16 15:04:31',2,'Accepted',NULL),(28,2,39,'2026-11-17 14:56:36','2026-11-17 14:56:58',3,'Accepted',NULL),(29,1,39,'2026-11-17 15:00:47','2026-11-17 15:01:45',1,'Accepted',NULL);
/*!40000 ALTER TABLE `APPLICATIONS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `BALANCE`
--

DROP TABLE IF EXISTS `BALANCE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `BALANCE` (
  `BALANCE_ID` int NOT NULL AUTO_INCREMENT,
  `SPONSORCOMP_ID` int NOT NULL,
  `BALANCE` double NOT NULL DEFAULT '0',
  `DRIVER_ID` int DEFAULT NULL,
  `IS_ACTIVE` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`BALANCE_ID`),
  KEY `fk_SPONSORCOMP_ID` (`SPONSORCOMP_ID`),
  KEY `fk_DRIVER_ID` (`DRIVER_ID`),
  CONSTRAINT `fk_DRIVER_ID` FOREIGN KEY (`DRIVER_ID`) REFERENCES `DRIVER` (`DRIVER_ID`),
  CONSTRAINT `fk_SPONSORCOMP_ID` FOREIGN KEY (`SPONSORCOMP_ID`) REFERENCES `SPONSORCOMP` (`SPONSORCOMP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BALANCE`
--

LOCK TABLES `BALANCE` WRITE;
/*!40000 ALTER TABLE `BALANCE` DISABLE KEYS */;
INSERT INTO `BALANCE` VALUES (1,1,380076,1,1),(2,1,1900,2,1),(3,1,114,3,1),(4,1,29423,4,0),(5,2,1018,5,1),(6,1,113,6,0),(7,1,20831,7,1),(8,2,5,8,1),(9,2,5,9,0),(10,2,5,10,1),(11,2,5,11,1),(17,1,0,17,0),(18,1,20,18,1),(19,2,0,19,1),(20,2,1e36,20,1),(21,1,0,21,1),(22,1,200,22,1),(23,2,490,22,1),(24,2,10,23,1),(25,1,0,23,1);
/*!40000 ALTER TABLE `BALANCE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CART_ITEM`
--

DROP TABLE IF EXISTS `CART_ITEM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CART_ITEM` (
  `CART_ITEM_ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `DRIVER_ID` int NOT NULL,
  `SPONSORCOMP_ID` int NOT NULL,
  `ITEM_ID` varchar(100) NOT NULL,
  `ADDED_AT` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CART_ITEM_ID`),
  UNIQUE KEY `uq_cart` (`DRIVER_ID`,`SPONSORCOMP_ID`,`ITEM_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CART_ITEM`
--

LOCK TABLES `CART_ITEM` WRITE;
/*!40000 ALTER TABLE `CART_ITEM` DISABLE KEYS */;
INSERT INTO `CART_ITEM` VALUES (2,12,6,1,'v1|237153425336|0','2026-10-31 04:36:29'),(3,12,6,1,'v1|920088705770|0','2026-10-31 04:38:41'),(6,12,6,1,'v1|326748511373|0','2026-11-05 19:40:20');
/*!40000 ALTER TABLE `CART_ITEM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DRIVER`
--

DROP TABLE IF EXISTS `DRIVER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DRIVER` (
  `DRIVER_ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  PRIMARY KEY (`DRIVER_ID`),
  KEY `USER_ID` (`USER_ID`),
  CONSTRAINT `DRIVER_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DRIVER`
--

LOCK TABLES `DRIVER` WRITE;
/*!40000 ALTER TABLE `DRIVER` DISABLE KEYS */;
INSERT INTO `DRIVER` VALUES (1,1),(2,3),(3,4),(4,5),(5,8),(6,12),(7,13),(8,20),(9,21),(10,23),(11,25),(21,27),(17,34),(18,35),(19,36),(20,37),(22,38),(23,39);
/*!40000 ALTER TABLE `DRIVER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `INVOICE`
--

DROP TABLE IF EXISTS `INVOICE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `INVOICE` (
  `INVOICE_ID` int NOT NULL AUTO_INCREMENT,
  `SPONSORCOMP_ID` int NOT NULL,
  `PERIOD_START` date NOT NULL,
  `PERIOD_END` date NOT NULL,
  `GENERATED_DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `TOTAL_FEE` decimal(12,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`INVOICE_ID`),
  KEY `IDX_INVOICE_SPONSORCOMP_ID` (`SPONSORCOMP_ID`),
  CONSTRAINT `FK_INVOICE_SPONSORCOMP` FOREIGN KEY (`SPONSORCOMP_ID`) REFERENCES `SPONSORCOMP` (`SPONSORCOMP_ID`),
  CONSTRAINT `CHK_INVOICE_DATE_RANGE` CHECK ((`PERIOD_END` >= `PERIOD_START`)),
  CONSTRAINT `CHK_INVOICE_TOTAL` CHECK ((`TOTAL_FEE` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `INVOICE`
--

LOCK TABLES `INVOICE` WRITE;
/*!40000 ALTER TABLE `INVOICE` DISABLE KEYS */;
INSERT INTO `INVOICE` VALUES (1,1,'2026-10-26','2026-10-26','2026-10-26 13:57:32',10.00),(2,1,'2026-11-07','2026-11-10','2026-11-09 14:38:46',80.00);
/*!40000 ALTER TABLE `INVOICE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `INVOICEDETAIL`
--

DROP TABLE IF EXISTS `INVOICEDETAIL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `INVOICEDETAIL` (
  `INVOICEDETAIL_ID` int NOT NULL AUTO_INCREMENT,
  `INVOICE_ID` int NOT NULL,
  `ORDER_ID` int NOT NULL,
  `DRIVER_ID` int NOT NULL,
  `ITEM_NAME` varchar(255) NOT NULL,
  `ITEM_AMOUNT` int NOT NULL,
  `ITEM_PRICE` decimal(10,2) NOT NULL,
  `LINE_TOTAL` decimal(12,2) NOT NULL,
  PRIMARY KEY (`INVOICEDETAIL_ID`),
  KEY `IDX_INVOICEDETAIL_INVOICE_ID` (`INVOICE_ID`),
  KEY `IDX_INVOICEDETAIL_DRIVER_ID` (`DRIVER_ID`),
  KEY `FK_INVOICEDETAIL_ORDER` (`ORDER_ID`),
  CONSTRAINT `FK_INVOICEDETAIL_DRIVER` FOREIGN KEY (`DRIVER_ID`) REFERENCES `DRIVER` (`DRIVER_ID`),
  CONSTRAINT `FK_INVOICEDETAIL_INVOICE` FOREIGN KEY (`INVOICE_ID`) REFERENCES `INVOICE` (`INVOICE_ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_INVOICEDETAIL_ORDER` FOREIGN KEY (`ORDER_ID`) REFERENCES `ORDERS` (`ORDER_ID`),
  CONSTRAINT `CHK_INVOICEDETAIL_AMOUNT` CHECK ((`ITEM_AMOUNT` > 0)),
  CONSTRAINT `CHK_INVOICEDETAIL_PRICE` CHECK ((`ITEM_PRICE` >= 0)),
  CONSTRAINT `CHK_INVOICEDETAIL_TOTAL` CHECK ((`LINE_TOTAL` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `INVOICEDETAIL`
--

LOCK TABLES `INVOICEDETAIL` WRITE;
/*!40000 ALTER TABLE `INVOICEDETAIL` DISABLE KEYS */;
INSERT INTO `INVOICEDETAIL` VALUES (1,1,6,1,'ZZ_TEST_INVOICE_ITEM',2,5.00,10.00),(2,2,7,7,'Holy Grail Chalice Disney Indiana Jones and the Last Crusade Prop Reproduction',1,80.00,80.00);
/*!40000 ALTER TABLE `INVOICEDETAIL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ITEMIZEDORDER`
--

DROP TABLE IF EXISTS `ITEMIZEDORDER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ITEMIZEDORDER` (
  `ITEMIZED_ID` int NOT NULL AUTO_INCREMENT,
  `ORDER_ID` int NOT NULL,
  `ITEM_NAME` varchar(255) NOT NULL,
  `ITEM_DESC` text,
  `ITEM_AMOUNT` int NOT NULL,
  `ITEM_PRICE` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ITEMIZED_ID`),
  KEY `IDX_ITEMIZEDORDER_ORDER_ID` (`ORDER_ID`),
  CONSTRAINT `FK_ITEMIZEDORDER_ORDER` FOREIGN KEY (`ORDER_ID`) REFERENCES `ORDERS` (`ORDER_ID`),
  CONSTRAINT `CHK_ITEMIZEDORDER_AMOUNT` CHECK ((`ITEM_AMOUNT` > 0)),
  CONSTRAINT `CHK_ITEMIZEDORDER_PRICE` CHECK ((`ITEM_PRICE` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ITEMIZEDORDER`
--

LOCK TABLES `ITEMIZEDORDER` WRITE;
/*!40000 ALTER TABLE `ITEMIZEDORDER` DISABLE KEYS */;
INSERT INTO `ITEMIZEDORDER` VALUES (1,6,'ZZ_TEST_INVOICE_ITEM','Temporary item for invoice testing',2,5.00),(2,7,'Holy Grail Chalice Disney Indiana Jones and the Last Crusade Prop Reproduction','Ceramic Holy Grail goblet (NOT FOR FOOD OR DRINK). Authentic collectible replica of relic Indiana Jones discovered during his adventures. Not for food use. I want you to receive your item as soon as possible.',1,80.00),(3,8,'Staff of Ra Headpiece - Full Scale','If you are Indiana Jones and you want to find the Lost Ark, you need the Headpiece to the Staff of Ra! While the Staff is long since lost, the Headpiece has instructions for the height of the Staff: It should be \"Six Kadams high.',1,28.00),(4,9,'THE ARK OF THE COVENANT PHOTO JESUS CHRIST SON GOD FATHER POSTER 8x10 No Frame','SHIPPING NOTE: Your photo will be shipped via USPS First-Class Mail in a protective rigid mailer. Please note: First-Class Mail does NOT include tracking, so no tracking number will be available for this order. Delivery usually takes 5-7 business…',1,100.00),(5,10,'Holy Grail Chalice Disney Indiana Jones and the Last Crusade Prop Reproduction','Ceramic Holy Grail goblet (NOT FOR FOOD OR DRINK). Authentic collectible replica of relic Indiana Jones discovered during his adventures. Not for food use. I want you to receive your item as soon as possible.',1,80.00),(6,11,'PS5 Hall Effect Stick Controller V3 Magnet Effekt Drift Fix für PlayStation5 Lot','About this item： ⭐Designed for replacing the drifted or damaged joystick of your PS5 controller, effectively eliminates stick drift issues, providing a reliable solution for uninterrupted gaming sessions. ⭐Improved accuracy: Hall sensors provide…',1,392.00),(7,12,'Kenner Star Wars Imperial AT-AT Walker 1997 (opened) Everything Included.','This first edition, battery-powered unit is a sought-after item for fans of the iconic film series, particularly Episode V - The Empire Strikes Back.',1,200.00),(8,12,'Star Wars The Retro Collection Return of the Jedi 3 3/4-Inch Action Figure','And Mon Mothma gets her long-overdue Kenner-style debut. Exclusive collector set. Why Collect This Set.',1,70.00),(9,12,'Vintage 1979 Star Wars Boba Fett Bounty Hunter Original Kenner Action Figure HK','The Vintage 1979 Star Wars Boba Fett Bounty Hunter Original Kenner Action Figure from Hong Kong is a highly sought-after collectible for fans of the Star Wars franchise and collectors of vintage toys. This 3.75\" plastic action figure of the iconic…',1,30.00),(10,13,'Wilson Tennis Pro Overgrip 30 Pack White WRZ4017WH','The Wilson Tennis PRO Overgrip 30 Pack is a high-quality product designed for tennis players looking to enhance their grip on the racket. Made by the reputable brand Wilson, this pack includes 30 Pro Overgrip models, ensuring that players have a…',1,30.00),(11,14,'Werther\'s Original Soft Caramel Candy, 25 oz (2 Count)','Made with real butter and fresh cream, for a one-of-a-kind taste. One 25 Oz. Peanut-Free Shellfish-Free Tree Nut-Free. One 25 oz. Made with real butter and fresh cream, for a smooth taste that is one of a kind.',1,56.00),(12,15,'Vintage Indiana Jones Golden Fertility Idol -The Lost Temple, Raiders of the Ark','The Vintage Indiana Jones Golden Fertility Idol by Kenner is a collectible action figure from the Indiana Jones franchise. This plastic toy, made in the 1980s, features the iconic Golden Fertility Idol from the Raiders of the Lost Ark movie. With…',1,5.00),(13,15,'1981 Topps Raiders of the Lost Ark Card #53 Ark of The Covenant','Each card will be in its own sleeve. Card(s) are placed in a Rigid Envelope. BONUS 1 New BCW Top Loader Card protector per order to protect them. Excellent: Has clearly visible signs of wear, Flaws may include.',1,1.00),(14,15,'Indiana Jones Full Size Chachapoyan Golden Fertility Idol - 1:1 Scale','The Golden Idol, to which it is commonly referred as, is a fictitious artifact that appears in the opening sequence of the 1981 film Raiders of the Lost Ark. It is the first relic that the audience sees Indiana Jones acquire, establishing him as a…',1,133.00),(15,15,'Grand Theft Auto 6 GTA VI Ultimate Edition - PS5 Offline - READ DESCRIPTION','🕹️ About Grand Theft Auto VI. 🌎 Explore the massive open world of Leonida. 💥 Experience thrilling heists and high-speed police chases.',1,33.00),(16,16,'Indiana Jones Urn of Nurhachi prop replica','This is a prop replica of the “Funerary Urn of Nurhachi’s Remains” inspired by the movie, Indiana Jones and the Temple of Doom based on the screen-used prop, using as many reference photos from display exhibitions, source material from the Lucasfilm…',1,1125.00),(17,17,'US American Flag 3x5 Quality Made USA Flag Embroidered United States Flag','★ FLYING THE PRIDE FLAG, EXPRESS YOUR LOVE AND ADMIRATION FOR THIS GREAT COUNTRY! ★ Every component exceeds the standard - beginning with fabric - blended army duck cloth is used for a clean white header - then 210 Denier heavyweight nylon bunting…',1,9.00),(18,18,'KJV HOLY BIBLE King James Version Black Large Print Thumb Index Edition* NEW','KJV HOLY BIBLE. The edition includes the Epistle Dedicatory. Unique Scripture Verse Finder. Gold foil pressed titling and accents and gold gilt-edged pages enhance the simple elegance of the design.',1,30.00),(19,19,'4 DC Comic Batman 3 In 1 Batcave Playset & Exclusive 4\" Batman Action Figure Set','Excellent condition! Make sure to add to your DC collection. Pricing is for each box not the lot.',1,60.00),(20,20,'Cross of Coronado 1:1 Scale Prop Indiana Jones Last Crusade','The Cross of Coronado 1:1 Scale Prop from Indiana Jones Last Crusade is a detailed replica used in the movie. This reproduction piece is perfect for fans of the film looking to add a piece of cinematic history to their collection. The prop adds an…',1,30.00),(21,21,'Cross of Coronado 1:1 Scale Prop Indiana Jones Last Crusade','The Cross of Coronado 1:1 Scale Prop from Indiana Jones Last Crusade is a detailed replica used in the movie. This reproduction piece is perfect for fans of the film looking to add a piece of cinematic history to their collection. The prop adds an…',1,30.00),(22,22,'3D Holy Grail Chalice Indiana Jones And The Last Crusade Cosplay Prop UNPAINTED','3D Printed one-piece strong composite. See last picture for an example of the materials needed to paint this piece. Small, about the size of a wallet so it fits anywhere!',1,1134.00),(23,23,'1981 Topps Raiders of the Lost Ark Card #53 Ark of The Covenant','Each card will be in its own sleeve. Card(s) are placed in a Rigid Envelope. BONUS 1 New BCW Top Loader Card protector per order to protect them. Excellent: Has clearly visible signs of wear, Flaws may include.',1,99.00);
/*!40000 ALTER TABLE `ITEMIZEDORDER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LOGINATTEMPTS`
--

DROP TABLE IF EXISTS `LOGINATTEMPTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LOGINATTEMPTS` (
  `ATTEMPT_ID` int NOT NULL AUTO_INCREMENT,
  `ATTEMPTED_EMAIL` varchar(255) NOT NULL,
  `RESULT` tinyint(1) NOT NULL,
  `DTS` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ATTEMPT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=575 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LOGINATTEMPTS`
--

LOCK TABLES `LOGINATTEMPTS` WRITE;
/*!40000 ALTER TABLE `LOGINATTEMPTS` DISABLE KEYS */;
INSERT INTO `LOGINATTEMPTS` VALUES (1,'chosenone@gmail.com',0,'2026-10-24 14:55:00'),(2,'chosenone@gmail.com',1,'2026-10-24 14:56:20'),(12,'something@gmail.com',0,'2026-10-24 15:03:39'),(13,'something@gmail.com',0,'2026-10-24 15:03:43'),(14,'asdf',0,'2026-10-24 15:04:00'),(15,'skdjfkasdf',0,'2026-10-24 15:04:30'),(16,'chosenone@gmail.com',1,'2026-10-24 15:06:04'),(17,'chosenone@gmail.com',1,'2026-10-24 16:52:54'),(18,'chosenone@gmail.com',1,'2026-10-24 16:56:49'),(19,'chosenone@gmail.com',1,'2026-10-25 14:28:11'),(20,'chosenone@gmail.com',1,'2026-10-25 14:56:45'),(21,'chosenone@gmail.com',1,'2026-10-25 14:57:40'),(22,'bwayne@gmail.com',1,'2026-10-26 00:52:58'),(23,'bwayne@gmail.com',1,'2026-10-26 00:58:25'),(24,'admin@gmail.com',1,'2026-10-26 00:59:23'),(25,'chosenone@gmail.com',1,'2026-10-26 13:13:05'),(26,'chosenone@gmail.com',1,'2026-10-26 13:17:38'),(27,'admin@gmail.com',1,'2026-10-26 13:36:42'),(28,'admin@gmail.com',1,'2026-10-26 13:38:44'),(29,'chosenone@gmail.com',1,'2026-10-26 13:44:11'),(30,'chosenone@gmail.com',1,'2026-10-26 13:45:08'),(31,'admin@gmail.com',1,'2026-10-26 13:46:06'),(32,'admin@gmail.com',1,'2026-10-26 13:57:21'),(33,'admin@gmail.com',1,'2026-10-26 13:59:36'),(34,'admin@gmail.com',1,'2026-10-26 14:02:21'),(35,'chosenone@gmail.com',1,'2026-10-26 14:03:45'),(36,'chosenone@gmail.com',1,'2026-10-26 14:07:01'),(37,'BipBop',1,'2026-10-26 14:55:26'),(38,'Bipbop',1,'2026-10-26 14:59:52'),(39,'Bipbop',0,'2026-10-26 15:09:30'),(40,'BipBop',1,'2026-10-26 15:09:56'),(41,'Bipbop',1,'2026-10-26 15:11:22'),(42,'hansolo@gmail.com',1,'2026-10-26 16:31:35'),(43,'bwayne@gmail.com',1,'2026-10-26 16:34:13'),(44,'Bipbop',1,'2026-10-26 16:35:31'),(45,'bwayne@gmail.com',1,'2026-10-26 16:46:04'),(46,'bwayne@gmail.com',1,'2026-10-26 16:46:29'),(47,'bwayne@gmail.com',1,'2026-10-26 16:49:47'),(48,'bwayne@gmail.com',1,'2026-10-26 16:51:21'),(49,'bwayne@gmail.com',1,'2026-10-26 16:52:52'),(50,'hansolo@gmail.com',1,'2026-10-26 16:55:00'),(51,'bwayne@gmail.com',1,'2026-10-26 17:02:14'),(52,'bwayne@gmail.com',1,'2026-10-26 17:03:05'),(53,'hansolo@gmail.com',1,'2026-10-26 17:34:57'),(54,'hansolo@gmail.com',1,'2026-10-27 00:18:02'),(55,'lukeskywalker@gmail.com',1,'2026-10-27 00:25:13'),(56,'hansolo@gmail.com',1,'2026-10-27 00:29:04'),(57,'hansolo@gmail.com',1,'2026-10-27 00:30:49'),(58,'lukeskywalker@gmail.com',1,'2026-10-27 00:35:02'),(59,'hansolo@gmail.com',1,'2026-10-27 00:39:59'),(60,'lukeskywalker@gmail.com',1,'2026-10-27 00:43:28'),(61,'bobafett@gmail.com',1,'2026-10-27 00:44:38'),(62,'indianajones@gmail.com',1,'2026-10-27 00:45:29'),(63,'lukeskywalker@gmail.com',1,'2026-10-27 00:45:58'),(64,'chosenone@gmail.com',1,'2026-10-27 13:58:50'),(65,'chosenone@gmail.com',1,'2026-10-27 14:28:42'),(66,'lukeskywalker@gmail.com',1,'2026-10-27 15:27:22'),(67,'lukeskywalker@gmail.com',1,'2026-10-27 15:28:27'),(68,'lukeskywalker@gmail.com',1,'2026-10-27 15:39:12'),(69,'chosenone@gmail.com',1,'2026-10-27 15:43:00'),(70,'bwayne@gmail.com',0,'2026-10-27 15:44:04'),(71,'bwayne@gmail.com',1,'2026-10-27 15:44:12'),(72,'chosenone@gmail.com',1,'2026-10-27 15:46:03'),(73,'chosenone@gmail.com',1,'2026-10-27 15:47:04'),(74,'bwayne@gmail.com',1,'2026-10-27 15:49:33'),(75,'bwayne@gmail.com',0,'2026-10-27 15:51:12'),(76,'bwayne@gmail.com',1,'2026-10-27 15:51:21'),(77,'bwayne@gmail.com',1,'2026-10-27 16:04:35'),(78,'bwayne@gmail.com',1,'2026-10-27 16:06:08'),(79,'bwayne@gmail.com',1,'2026-10-27 16:06:49'),(80,'lukeskywalker@gmail.com',1,'2026-10-27 16:09:16'),(81,'bwayne@gmail.com',1,'2026-10-27 16:09:43'),(82,'hansolo@gmail.com',1,'2026-10-27 16:10:48'),(83,'bwayne@gmail.com',0,'2026-10-27 16:12:47'),(84,'bwayne@gmail.com',1,'2026-10-27 16:12:56'),(85,'chosenone@gmail.com',1,'2026-10-27 16:13:19'),(86,'chosenone@gmail.com',1,'2026-10-27 16:18:15'),(87,'chosenone@gmail.com',1,'2026-10-27 16:18:16'),(88,'BipBop',1,'2026-10-27 16:23:29'),(89,'BipBop',1,'2026-10-27 16:31:55'),(90,'bwayne@gmail.com',1,'2026-10-27 16:32:14'),(91,'bwayne@gmail.com',1,'2026-10-27 16:56:40'),(92,'bwayne@gmail.com',1,'2026-10-27 16:58:53'),(93,'lluthor@gmail.com',1,'2026-10-27 16:59:33'),(94,'lluthor@gmail.com',1,'2026-10-27 17:14:19'),(95,'bwayne@gmail.com',0,'2026-10-27 17:15:32'),(96,'bwayne@gmail.com',1,'2026-10-27 17:15:41'),(97,'bwayne@gmail.com',1,'2026-10-27 17:16:36'),(98,'bwayne@gmail.com',1,'2026-10-27 17:19:14'),(99,'lukeskywalker@gmail.com',1,'2026-10-27 18:25:58'),(100,'hansolo@gmail.com',1,'2026-10-27 18:27:00'),(101,'chosenone@gmail.com',1,'2026-10-27 18:31:25'),(102,'bwayne@gmail.com',1,'2026-10-27 18:32:12'),(103,'bwayne@gmail.com',0,'2026-10-27 18:32:34'),(104,'lukeskywalker@gmail.com',1,'2026-10-27 18:32:51'),(105,'lukeskywalker@gmail.com',1,'2026-10-27 18:34:43'),(106,'chosenone@gmail.com',1,'2026-10-27 18:35:07'),(107,'chosenone@gmail.com',1,'2026-10-27 18:50:23'),(108,'chosenone@gmail.com',1,'2026-10-27 18:52:02'),(109,'chosenone@gmail.com',1,'2026-10-27 18:53:48'),(110,'lukeskywalker@gmail.com',1,'2026-10-27 18:56:02'),(111,'chosenone@gmail.com',1,'2026-10-27 18:57:26'),(112,'chosenone@gmail.com',1,'2026-10-28 11:49:53'),(113,'chosenone@gmail.com',1,'2026-10-28 12:26:15'),(114,'chosenone@gmail.com',1,'2026-10-28 14:27:55'),(115,'chosenone@gmail.com',1,'2026-10-28 21:58:51'),(116,'chosenone@gmail.com',1,'2026-10-28 22:26:44'),(117,'lukeskywalker@gmail.com',1,'2026-10-28 23:24:07'),(118,'chosenone@gmail.com',1,'2026-10-28 23:26:30'),(119,'lukeskywalker@gmail.com',1,'2026-10-28 23:35:57'),(120,'chosenone@gmail.com',1,'2026-10-28 23:40:54'),(121,'lukeskywalker@gmail.com',1,'2026-10-28 23:46:39'),(122,'chosenone@gmail.com',1,'2026-10-28 23:57:41'),(123,'chosenone@gmail.com',1,'2026-10-29 00:05:03'),(124,'lukeskywalker@gmail.com',1,'2026-10-29 11:45:54'),(125,'chosenone@gmail.com',1,'2026-10-29 12:11:29'),(126,'lukeskywalker@gmail.com',1,'2026-10-29 15:53:10'),(127,'chosenone@gmail.com',1,'2026-10-29 15:55:12'),(128,'lukeskywalker@gmail.com',1,'2026-10-29 15:56:49'),(129,'lukeskywalker@gmail.com',1,'2026-10-29 16:04:49'),(130,'hansolo@gmail.com',1,'2026-10-29 16:08:03'),(131,'chosenone@gmail.com',1,'2026-10-29 16:15:41'),(132,'lukeskywalker@gmail.com',1,'2026-10-29 16:15:56'),(133,'chosenone@gmail.com',1,'2026-10-29 16:18:55'),(134,'chosenone@gmail.com',1,'2026-10-29 16:19:15'),(135,'chosenone@gmail.com',1,'2026-10-29 16:19:30'),(136,'chosenone@gmail.com',1,'2026-10-29 16:21:02'),(137,'hansolo@gmail.com',1,'2026-10-29 16:23:43'),(138,'hansolo@gmail.com',1,'2026-10-29 16:24:23'),(139,'hansolo@gmail.com',1,'2026-10-29 16:26:26'),(140,'chosenone@gmail.com',1,'2026-10-29 16:27:49'),(141,'chosenone@gmail.com',1,'2026-10-29 16:31:43'),(142,'chosenone@gmail.com',1,'2026-10-29 16:32:37'),(143,'chosenone@gmail.com',1,'2026-10-29 16:34:18'),(144,'hansolo@gmail.com',1,'2026-10-29 16:36:39'),(145,'hansolo@gmail.com',1,'2026-10-29 16:37:58'),(146,'hansolo@gmail.com',1,'2026-10-29 16:38:08'),(147,'chosenone@gmail.com',1,'2026-10-29 16:41:00'),(148,'lukeskywalker@gmail.com',1,'2026-10-29 16:41:33'),(149,'hansolo@gmail.com',1,'2026-10-29 16:42:03'),(150,'hansolo@gmail.com',1,'2026-10-29 16:42:10'),(151,'hansolo@gmail.com',1,'2026-10-29 16:43:25'),(152,'hansolo@gmail.com',1,'2026-10-29 16:43:38'),(153,'hansolo@gmail.com',1,'2026-10-29 16:51:41'),(154,'lukeskywalker@gmail.com',1,'2026-10-29 17:17:29'),(155,'nightwing@gmail.com',0,'2026-10-29 17:43:11'),(156,'nightwing@gmail.com',0,'2026-10-29 17:43:30'),(157,'nightwing@gmail.com',1,'2026-10-29 17:44:04'),(158,'lukeskywalker@gmail.com',1,'2026-10-29 17:46:39'),(159,'chosenone@gmail.com',1,'2026-10-29 17:52:09'),(160,'BipBop',1,'2026-10-29 18:00:59'),(161,'admin@gmail.com',1,'2026-10-29 18:14:34'),(162,'lukeskywalker@gmail.com',1,'2026-10-29 18:15:38'),(163,'bwayne@gmail.com',1,'2026-10-29 18:19:24'),(164,'hansolo@gmail.com',1,'2026-10-29 18:23:18'),(165,'admin@gmail.com',1,'2026-10-29 18:26:04'),(166,'lukeskywalker@gmail.com',1,'2026-10-29 18:26:45'),(167,'hansolo@gmail.com',1,'2026-10-29 18:27:32'),(168,'chosenone@gmail.com',1,'2026-10-29 18:33:33'),(169,'admin@gmail.com',1,'2026-10-29 18:34:46'),(170,'hansolo@gmail.com',1,'2026-10-29 18:35:49'),(171,'lukeskywalker@gmail.com',1,'2026-10-29 18:36:49'),(172,'hansolo@gmail.com',1,'2026-10-29 18:38:14'),(173,'bwayne@gmail.com',1,'2026-10-29 18:39:29'),(174,'lukeskywalker@gmail.com',1,'2026-10-29 18:45:14'),(175,'brucewayne@gmail.com',0,'2026-10-29 18:45:42'),(176,'bwayne@gmail.com',1,'2026-10-29 18:45:56'),(177,'hansolo@gmail.com',1,'2026-10-29 18:46:32'),(178,'hansolo@gmail.com',0,'2026-10-29 19:38:41'),(179,'hansolo@gmail.com',1,'2026-10-29 19:39:03'),(180,'lukeskywalker@gmail.com',1,'2026-10-29 19:39:29'),(181,'babyoda@gmail.com',1,'2026-10-29 19:41:47'),(182,'lukeskywalker@gmail.com',1,'2026-10-29 19:45:20'),(183,'lukeskywalker@gmail.com',1,'2026-10-29 19:47:45'),(184,'chosenone@gmail.com',1,'2026-10-29 20:19:09'),(185,'lukeskywalker@gmail.com',1,'2026-10-29 20:28:26'),(186,'chosenone@gmail.com',1,'2026-10-29 20:30:08'),(187,'lukeskywalker@gmail.com',1,'2026-10-29 20:30:58'),(188,'lukeskywalker@gmail.com',1,'2026-10-29 23:17:49'),(189,'lukeskywalker@gmail.com',1,'2026-10-29 23:32:34'),(190,'lukeskywalker@gmail.com',1,'2026-10-29 23:42:26'),(191,'chosenone@gmail.com',1,'2026-10-29 23:43:31'),(192,'chosenone@gmail.com',1,'2026-10-30 00:09:19'),(193,'chosenone@gmail.com',1,'2026-10-30 00:13:42'),(194,'chosenone@gmail.com',1,'2026-10-30 13:38:25'),(195,'lukeskywalker@gmail.com',1,'2026-10-30 13:40:29'),(196,'chosenone@gmail.com',1,'2026-10-30 20:01:10'),(197,'hansolo@gmail.com',1,'2026-10-30 20:03:09'),(198,'hansolo@gmail.com',1,'2026-10-30 20:03:37'),(199,'admin@gmail.com',1,'2026-10-30 20:06:37'),(200,'bwayne@gmail.com',1,'2026-10-30 20:08:20'),(201,'bwayne@gmail.com',1,'2026-10-30 20:37:06'),(202,'lluther@gmail.com',0,'2026-10-30 21:00:42'),(203,'lluther@gmail.com',0,'2026-10-30 21:01:11'),(204,'bobafett@gmail.com',1,'2026-10-30 21:01:47'),(205,'something',1,'2026-10-30 21:02:46'),(206,'admin@gmail.com',1,'2026-10-30 21:27:25'),(207,'ecart@gmail.com',1,'2026-10-30 21:41:05'),(208,'ecart@gmail.com',1,'2026-10-30 21:42:16'),(209,'bwayne@gmail.com',1,'2026-10-30 21:43:06'),(210,'admin@gmail.com',1,'2026-10-30 21:43:22'),(211,'bwayne@gmail.com',1,'2026-10-31 01:21:23'),(212,'something',1,'2026-10-31 01:44:38'),(213,'something',1,'2026-10-31 02:02:23'),(214,'admin@gmail.com',1,'2026-10-31 02:57:32'),(215,'hansolo@gmail.com',1,'2026-10-31 04:34:31'),(216,'hansolo@gmail.com',1,'2026-10-31 04:37:31'),(217,'bwayne@gmail.com',1,'2026-10-31 04:51:30'),(218,'hansolo@gmail.com',1,'2026-10-31 04:55:47'),(219,'bwayne@gmail.com',1,'2026-10-31 04:56:23'),(220,'lukeskywalker@gmail.com',1,'2026-10-31 05:05:40'),(221,'lukeskywalker@gmail.com',0,'2026-10-31 05:16:19'),(222,'chosenone@gmail.com',1,'2026-10-31 05:16:24'),(223,'admin@gmail.com',1,'2026-10-31 11:13:09'),(224,'bwayne@gmail.com',1,'2026-10-31 11:14:44'),(225,'admin@gmail.com',1,'2026-10-31 11:21:07'),(226,'admin@gmail.com',1,'2026-10-31 11:26:27'),(227,'hansolo@gmail.com',1,'2026-11-02 14:30:52'),(228,'admin@gmail.com',1,'2026-11-02 14:32:05'),(229,'chosenone@gmail.com',1,'2026-11-02 14:34:00'),(230,'admin@gmail.com',1,'2026-11-02 16:47:47'),(231,'admin@gmail.com',1,'2026-11-03 15:14:30'),(232,'admin@gmail.com',1,'2026-11-03 15:16:37'),(233,'admin@gmail.com',1,'2026-11-03 15:18:20'),(234,'bwayne@gmail.com',1,'2026-11-03 15:45:01'),(235,'bwayne@gmail.com',1,'2026-11-03 15:47:22'),(236,'admin@gmail.com',1,'2026-11-03 15:47:57'),(237,'admin@gmail.com',1,'2026-11-03 15:55:52'),(238,'admin@gmail.com',1,'2026-11-03 15:58:51'),(239,'admin@gmail.com',1,'2026-11-03 16:06:30'),(240,'admin@gmail.com',1,'2026-11-03 16:19:54'),(241,'admin@gmail.com',1,'2026-11-03 16:29:35'),(242,'bwayne@gmail.com',1,'2026-11-03 18:37:44'),(243,'admin@gmail.com',1,'2026-11-03 18:38:14'),(244,'bwayne@gmail.com',1,'2026-11-03 18:48:25'),(245,'admin@gmail.com',1,'2026-11-03 19:12:17'),(246,'admin@gmail.com',1,'2026-11-03 19:27:56'),(247,'admin@gmail.com',1,'2026-11-03 19:31:31'),(248,'disney@yahoo.com',1,'2026-11-04 13:42:50'),(249,'admin@gmail.com',1,'2026-11-04 14:06:10'),(250,'superman@gmail.com',1,'2026-11-04 14:07:27'),(251,'frostedflakes@gmail.com',1,'2026-11-04 14:09:08'),(252,'Bipbop',0,'2026-11-04 14:16:05'),(253,'bwayne@gmail.com',1,'2026-11-04 14:17:07'),(254,'frostedflakes@gmail.com',1,'2026-11-05 12:34:44'),(255,'disney@yahoo.com',1,'2026-11-05 12:59:45'),(256,'frostedflakes@gmail.com',1,'2026-11-05 13:18:44'),(257,'chosenone@gmail.com',1,'2026-11-05 13:25:00'),(258,'lukeskywalker@gmail.com',1,'2026-11-05 18:07:18'),(259,'lukeskywalker@gmail.com',1,'2026-11-05 18:09:01'),(260,'lukeskywalker@gmail.com',1,'2026-11-05 18:13:38'),(261,'lukeskywalker@gmail.com',1,'2026-11-05 18:17:43'),(262,'lukeskywalker@gmail.com',1,'2026-11-05 18:27:38'),(263,'frostedflakes@gmail.com',1,'2026-11-05 18:29:25'),(264,'lukeskywalker@gmail.com',1,'2026-11-05 18:29:25'),(265,'frostedflakes@gmail.com',1,'2026-11-05 18:29:51'),(266,'chosenone@gmail.com',1,'2026-11-05 18:30:10'),(267,'chosenone@gmail.com',1,'2026-11-05 18:30:21'),(268,'admin@gmail.com',1,'2026-11-05 18:30:59'),(269,'chosenone@gmail.com',1,'2026-11-05 18:35:42'),(270,'hansolo@gmail.com',0,'2026-11-05 18:35:55'),(271,'hansolo@gmail.com',1,'2026-11-05 18:36:15'),(272,'chosenone@gmail.com',1,'2026-11-05 18:36:33'),(273,'lukeskywalker@gmail.com',1,'2026-11-05 18:37:04'),(274,'babyoda@gmail.com',0,'2026-11-05 18:38:03'),(275,'babyoda@gmail.com',1,'2026-11-05 18:38:36'),(276,'lukeskywalker@gmail.com',1,'2026-11-05 18:39:25'),(277,'chosenone@gmail.com',1,'2026-11-05 18:40:55'),(278,'frostedflakes@gmail.com',1,'2026-11-05 18:41:17'),(279,'lukeskywalker@gmail.com',1,'2026-11-05 18:41:30'),(280,'lukeskywalker@gmail.com',1,'2026-11-05 18:42:52'),(281,'lukeskywalker@gmail.com',1,'2026-11-05 18:43:56'),(282,'chosenone@gmail.com',1,'2026-11-05 18:46:10'),(283,'lukeskywalker@gmail.com',1,'2026-11-05 18:46:17'),(284,'chosenone@gmail.com',1,'2026-11-05 18:47:40'),(285,'hansolo@gmail.com',1,'2026-11-05 18:51:32'),(286,'lukeskywalker@gmail.com',1,'2026-11-05 18:54:28'),(287,'lukeskywalker@gmail.com',1,'2026-11-05 19:09:02'),(288,'lukeskywalker@gmail.com',1,'2026-11-05 19:11:40'),(289,'lukeskywalker@gmail.com',1,'2026-11-05 19:12:14'),(290,'lukeskywalker@gmail.com',1,'2026-11-05 19:24:48'),(291,'lukeskywalker@gmail.com',1,'2026-11-05 19:26:11'),(292,'chosenone@gmail.com',1,'2026-11-05 19:33:38'),(293,'lukeskywalker@gmail.com',1,'2026-11-05 19:34:04'),(294,'lukeskywalker@gmail.com',1,'2026-11-05 19:38:05'),(295,'hansolo@gmail.com',1,'2026-11-05 19:39:35'),(296,'chosenone@gmail.com',1,'2026-11-05 19:43:45'),(297,'hansolo@gmail.com',1,'2026-11-05 21:11:59'),(298,'admin@gmail.com',1,'2026-11-06 16:43:13'),(299,'bwayne@gmail.com',1,'2026-11-06 16:44:36'),(300,'admin@gmail.com',1,'2026-11-06 17:23:49'),(301,'lukeskywalker@gmail.com',1,'2026-11-06 17:38:59'),(302,'admin@gmail.com',1,'2026-11-06 19:15:39'),(303,'bwayne@gmail.com',1,'2026-11-06 19:17:15'),(304,'admin@gmail.com',1,'2026-11-06 19:17:56'),(305,'hw@gmail.com',1,'2026-11-06 19:22:45'),(306,'bwayne@gmail.com',1,'2026-11-06 19:23:44'),(307,'bwayne@gmail.com',1,'2026-11-06 19:43:25'),(308,'hw@gmail.com',0,'2026-11-06 19:46:43'),(309,'hw@gmail.com',0,'2026-11-06 19:47:03'),(310,'hw@gmail.com',0,'2026-11-06 19:47:13'),(311,'hw@gmail.com',0,'2026-11-06 19:47:23'),(312,'hw@gmail.com',0,'2026-11-06 19:47:39'),(313,'hw@gmail.com',1,'2026-11-06 19:48:25'),(314,'bwayne@gmail.com',1,'2026-11-06 20:21:28'),(315,'hansolo@gmail.com',1,'2026-11-06 20:23:48'),(316,'bwayne@gmail.com',1,'2026-11-06 20:26:55'),(317,'indianajones@gmail.com',1,'2026-11-06 20:27:43'),(318,'lukeskywalker@gmail.com',1,'2026-11-06 20:28:43'),(319,'bwayne@gmail.com',1,'2026-11-06 20:28:58'),(320,'indianajones@gmail.com',1,'2026-11-06 20:29:45'),(321,'bwayne@gmail.com',1,'2026-11-06 20:30:24'),(322,'indianajones@gmail.com',1,'2026-11-06 20:30:50'),(323,'bwayne@gmail.com',1,'2026-11-06 20:33:48'),(324,'admin@gmail.com',1,'2026-11-06 20:35:08'),(325,'hw@gmail.com',0,'2026-11-06 20:35:41'),(326,'bwayne@gmail.com',1,'2026-11-06 20:36:01'),(327,'fsmoak@gmail.com',1,'2026-11-06 20:37:52'),(328,'fsmoak@gmail.com',1,'2026-11-06 21:00:41'),(329,'admin@gmail.com',1,'2026-11-06 21:01:09'),(330,'fsmoak@gmail.com',1,'2026-11-06 21:03:54'),(331,'admin@gmail.com',1,'2026-11-06 21:16:25'),(332,'fsmoak@gmail.com',1,'2026-11-06 21:20:28'),(333,'fsmoak@gmail.com',1,'2026-11-07 00:31:28'),(334,'admin@gmail.com',1,'2026-11-07 00:46:40'),(335,'bwayne@gmail.com',1,'2026-11-07 00:47:38'),(336,'indianajones@gmail.com',1,'2026-11-07 20:09:33'),(337,'indianajones@gmail.com',1,'2026-11-09 01:08:40'),(338,'bwayne@gmail.com',1,'2026-11-09 01:09:12'),(339,'indianajones@gmail.com',1,'2026-11-09 01:09:38'),(340,'bwayne@gmail.com',1,'2026-11-09 01:11:19'),(341,'indianajones@gmail.com',1,'2026-11-09 01:14:01'),(342,'bwayne@gmail.com',1,'2026-11-09 01:17:31'),(343,'bwayne@gmail.com',1,'2026-11-09 01:18:28'),(344,'indianajones@gmail.com',1,'2026-11-09 01:20:53'),(345,'bwayne@gmail.com',1,'2026-11-09 01:23:16'),(346,'indianajones@gmail.com',1,'2026-11-09 01:44:18'),(347,'bwayne@gmail.com',1,'2026-11-09 01:48:08'),(348,'indianajones@gmail.com',1,'2026-11-09 01:48:31'),(349,'indianajones@gmail.com',1,'2026-11-09 01:54:31'),(350,'Bipbop',0,'2026-11-09 14:06:38'),(351,'admin@gmail.com',1,'2026-11-09 14:06:53'),(352,'jasonzheng1244@gmail.com',1,'2026-11-09 14:14:12'),(353,'bwayne@gmail.com',0,'2026-11-09 14:15:05'),(354,'bwayne@gmail.com',1,'2026-11-09 14:15:20'),(355,'jasonzheng1244@gmail.com',1,'2026-11-09 14:15:36'),(356,'admin@gmail.com',1,'2026-11-09 14:16:10'),(357,'test@example.com',1,'2026-11-09 14:16:25'),(358,'bwayne@gmail.com',1,'2026-11-09 14:17:11'),(359,'bwayne@gmail.com',1,'2026-11-09 14:18:11'),(360,'admin@gmail.com',1,'2026-11-09 14:19:16'),(361,'Lukeskywalker@gmail.com',0,'2026-11-09 14:19:27'),(362,'Lukeskywalker@gmail.com',1,'2026-11-09 14:20:14'),(363,'admin@gmail.com',1,'2026-11-09 14:20:54'),(364,'kropemma3@gmail.com',1,'2026-11-09 14:22:43'),(365,'lluthor@gmail.com',1,'2026-11-09 14:24:12'),(366,'bwayne@gmail.com',1,'2026-11-09 14:24:18'),(367,'test@example.com',1,'2026-11-09 14:24:38'),(368,'jasonzheng1244@gmail.com',1,'2026-11-09 14:25:16'),(369,'jasonzheng1244@gmail.com',1,'2026-11-09 14:26:03'),(370,'test@example.com',1,'2026-11-09 14:26:14'),(371,'jasonzheng1244@gmail.com',1,'2026-11-09 14:27:04'),(372,'Lukeskywalker@gmail.com',1,'2026-11-09 14:28:59'),(373,'test@example.com',1,'2026-11-09 14:30:40'),(374,'Lukeskywalker@gmail.com',1,'2026-11-09 14:33:21'),(375,'test@example.com',1,'2026-11-09 14:34:02'),(376,'admin@gmail.com',1,'2026-11-09 14:36:03'),(377,'lukeskywalk@gmail.com',0,'2026-11-09 14:36:20'),(378,'chosenone@gmail.com',1,'2026-11-09 14:36:21'),(379,'lukeskywalker@gmail.com',1,'2026-11-09 14:36:50'),(380,'bwayne@gmail.com',1,'2026-11-09 14:38:04'),(381,'admin@gmail.com',1,'2026-11-09 14:38:28'),(382,'jasonzheng1244@gmail.com',1,'2026-11-09 14:41:04'),(383,'chosenone@gmail.com',1,'2026-11-09 14:41:42'),(384,'bwayne@gmail.com',1,'2026-11-09 14:42:10'),(385,'bwayne@gmail.com',1,'2026-11-09 14:42:16'),(386,'Lukeskywalker@gmail.com',1,'2026-11-09 14:42:34'),(387,'bwayne@gmail.com',1,'2026-11-09 14:43:42'),(388,'chosenone@gmail.com',1,'2026-11-09 14:45:53'),(389,'chosenone@gmail.com',1,'2026-11-09 14:58:16'),(390,'chosenone@gmail.com',1,'2026-11-09 14:58:58'),(391,'chosenone@gmail.com',1,'2026-11-09 15:05:04'),(392,'chosenone@gmail.com',1,'2026-11-09 15:09:08'),(393,'Lukeskywalker@gmail.com',1,'2026-11-10 13:25:39'),(394,'chosenone@gmail.com',1,'2026-11-10 13:53:32'),(395,'chosenone@gmail.com',1,'2026-11-10 13:56:08'),(396,'bwayne@gmail.com',1,'2026-11-10 14:34:40'),(397,'bwayne@gmail.com',1,'2026-11-10 14:44:16'),(398,'hansolo@gmail.com',1,'2026-11-10 16:22:55'),(399,'BipBop',1,'2026-11-10 16:23:44'),(400,'BipBop',1,'2026-11-10 16:55:50'),(401,'Bipbop',1,'2026-11-10 17:03:44'),(402,'bwayne@gmail.com',1,'2026-11-10 17:40:24'),(403,'Bipbop',0,'2026-11-10 18:14:52'),(404,'Bipbop',0,'2026-11-10 18:15:01'),(405,'Bipbop',1,'2026-11-10 18:15:20'),(406,'chosenone@gmail.com',1,'2026-11-10 19:17:52'),(407,'bwayne@gmail.com',1,'2026-11-10 19:19:32'),(408,'chosenone@gmail.com',1,'2026-11-10 19:21:14'),(409,'chosenone@gmail.com',1,'2026-11-10 19:25:42'),(410,'frostedflakes@gmail.com',1,'2026-11-10 19:28:04'),(411,'disney@yahoo.com',1,'2026-11-10 19:28:27'),(412,'chosenone@gmail.com',1,'2026-11-10 19:28:43'),(413,'bwayne@gmail.com',1,'2026-11-10 19:29:04'),(414,'chosenone@gmail.com',1,'2026-11-10 19:36:24'),(415,'bwayne@gmail.com',1,'2026-11-11 14:39:01'),(416,'bwayne@gmail.com',1,'2026-11-11 14:39:04'),(417,'chosenone@gmail.com',1,'2026-11-12 19:03:13'),(418,'bwayne@gmail.com',1,'2026-11-12 19:11:12'),(419,'indianajones@gmail.com',1,'2026-11-12 19:13:07'),(420,'admin@gmail.com',1,'2026-11-12 19:16:42'),(421,'bwayne@gmail.com',1,'2026-11-12 19:18:00'),(422,'chosenone@gmail.com',1,'2026-11-12 19:34:23'),(423,'Bipbop',0,'2026-11-12 19:34:57'),(424,'indianajones@gmail.com',1,'2026-11-12 19:36:25'),(425,'bwayne@gmail.com',1,'2026-11-12 19:39:44'),(426,'chosenone@gmail.com',1,'2026-11-12 21:16:08'),(427,'indianajones@gmail.com',1,'2026-11-13 14:49:29'),(428,'bwayne@gmail.com',1,'2026-11-13 14:50:10'),(429,'indianajones@gmail.com',1,'2026-11-13 14:55:16'),(430,'bwayne@gmail.com',1,'2026-11-13 14:55:34'),(431,'chosenone@gmail.com',1,'2026-11-13 14:56:33'),(432,'lukeskywalker@gmail.com',1,'2026-11-13 14:58:33'),(433,'chosenone@gmail.com',1,'2026-11-13 14:59:00'),(434,'indianajones@gmail.com',1,'2026-11-13 15:00:13'),(435,'bwayne@gmail.com',1,'2026-11-13 15:35:57'),(436,'bwayne@gmail.com',1,'2026-11-13 15:37:23'),(437,'ecart@gmail.com',1,'2026-11-13 15:45:24'),(438,'mail_name',1,'2026-11-13 15:46:49'),(439,'chosenone@gmail.com',1,'2026-11-13 15:51:15'),(440,'chosenone@gmail.com',1,'2026-11-13 15:57:21'),(441,'mail_name',1,'2026-11-13 16:03:15'),(442,'chosenone@gmail.com',1,'2026-11-13 16:05:16'),(443,'mail_name',1,'2026-11-13 16:05:48'),(444,'admin@gmail.com',1,'2026-11-13 16:18:52'),(445,'mail_name',1,'2026-11-13 16:44:46'),(446,'admin@gmail.com',1,'2026-11-13 16:53:04'),(447,'mail_name',1,'2026-11-13 16:54:14'),(448,'bwayne@gmail.com',1,'2026-11-13 17:22:26'),(449,'mail_name',1,'2026-11-13 18:22:58'),(450,'bwayne@gmail.com',1,'2026-11-13 18:26:00'),(451,'hansolo@gmail.com',1,'2026-11-13 18:29:03'),(452,'something',1,'2026-11-13 18:29:37'),(453,'bwayne@gmail.com',1,'2026-11-13 18:30:01'),(454,'ecart@gmail.com',1,'2026-11-13 18:30:33'),(455,'mail_name',1,'2026-11-13 18:44:54'),(456,'mail_name',1,'2026-11-13 19:04:25'),(457,'admin@gmail.com',1,'2026-11-13 19:16:16'),(458,'bwayne@gmail.com',1,'2026-11-13 19:16:45'),(459,'mail_name',1,'2026-11-13 19:17:17'),(460,'chosenone@gmail.com',1,'2026-11-15 16:14:57'),(461,'chosenone@gmail.com',1,'2026-11-15 16:16:22'),(462,'indianajones@gmail.com',1,'2026-11-15 16:49:22'),(463,'bwayne@gmail.com',1,'2026-11-15 17:37:49'),(464,'indianajones@gmail.com',1,'2026-11-15 17:46:29'),(465,'bwayne@gmail.com',1,'2026-11-15 17:56:18'),(466,'mail_name',1,'2026-11-15 18:15:32'),(467,'bwayne@gmail.com',1,'2026-11-15 18:15:56'),(468,'mail_name',1,'2026-11-15 18:39:19'),(469,'bwayne@gmail.com',1,'2026-11-15 18:39:48'),(470,'ecart@gmail.com',1,'2026-11-15 18:41:23'),(471,'admin@gmail.com',1,'2026-11-15 18:41:42'),(472,'admin@gmail.com',1,'2026-11-15 18:44:20'),(473,'bwayne@gmail.com',1,'2026-11-15 21:21:18'),(474,'bwayne@gmail.com',1,'2026-11-15 21:28:37'),(475,'indianajones@gmail.com',1,'2026-11-15 21:28:59'),(476,'bwayne@gmail.com',1,'2026-11-15 21:35:01'),(477,'indianajones@gmail.com',1,'2026-11-15 21:35:31'),(478,'bwayne@gmail.com',1,'2026-11-15 21:36:26'),(479,'indianajones@gmail.com',1,'2026-11-15 21:36:58'),(480,'admin@gmail.com',1,'2026-11-16 01:34:32'),(481,'admin@gmail.com',1,'2026-11-16 01:38:21'),(482,'Bipbop',0,'2026-11-16 01:40:27'),(483,'BipBop',0,'2026-11-16 01:41:08'),(484,'BipBop',1,'2026-11-16 01:41:21'),(485,'bwayne@gmail.com',1,'2026-11-16 03:17:54'),(486,'BipBop',1,'2026-11-16 03:24:55'),(487,'disney@yahoo.com',1,'2026-11-16 14:19:50'),(488,'bwayne@gmail.com',1,'2026-11-16 14:50:59'),(489,'bwayne@gmail.com',1,'2026-11-16 14:58:32'),(490,'2phones@gmail',1,'2026-11-16 15:02:33'),(491,'bwayne@gmail.com',1,'2026-11-16 15:03:12'),(492,'lluthor@gmail.com',1,'2026-11-16 15:04:23'),(493,'2phones@gmail',0,'2026-11-16 15:04:52'),(494,'2phones@gmail',0,'2026-11-16 15:05:15'),(495,'2phones@gmail',1,'2026-11-16 15:20:08'),(496,'2phones@gmail',1,'2026-11-16 15:36:24'),(497,'2phones@gmail',1,'2026-11-16 15:45:17'),(498,'bwayne@gmail.com',1,'2026-11-16 15:46:20'),(499,'2phones@gmail',1,'2026-11-16 15:47:36'),(500,'lluthor@gmail.com',1,'2026-11-16 15:48:35'),(501,'2phones@gmail',1,'2026-11-16 15:50:31'),(502,'2phones@gmail',1,'2026-11-16 15:54:19'),(503,'2phones@gmail',1,'2026-11-16 15:59:44'),(504,'bwayne@gmail.com',1,'2026-11-16 16:00:13'),(505,'chosenone@gmail.com',1,'2026-11-16 16:24:25'),(506,'Lukeskywalker@gmail.com',1,'2026-11-16 16:26:23'),(507,'2phones@gmail',1,'2026-11-16 17:15:15'),(508,'BipBop',1,'2026-11-16 17:17:01'),(509,'2phones@gmail',1,'2026-11-16 17:19:32'),(510,'2phones@gmail',1,'2026-11-16 17:22:22'),(511,'2phones@gmail',1,'2026-11-16 17:28:05'),(512,'2phones@gmail',1,'2026-11-16 17:30:03'),(513,'chosenone@gmail.com',1,'2026-11-17 13:48:49'),(514,'chosenone@gmail.com',1,'2026-11-17 13:49:04'),(515,'chosenone@gmail.com',1,'2026-11-17 13:50:26'),(516,'chosenone@gmail.com',1,'2026-11-17 13:50:45'),(517,'chosenone@gmail.com',1,'2026-11-17 13:51:02'),(518,'chosenone@gmai.com',0,'2026-11-17 13:51:23'),(519,'chosenone@gmail.com',1,'2026-11-17 13:51:31'),(520,'chosenone@gmail.com',1,'2026-11-17 13:52:14'),(521,'chosenone@gmail.com',1,'2026-11-17 13:52:47'),(522,'chosenone@gmail.com',1,'2026-11-17 14:02:35'),(523,'chosenone@gmail.com',1,'2026-11-17 14:07:37'),(524,'chosenone@gmail.com',1,'2026-11-17 14:09:21'),(525,'chosenone@gmail.com',1,'2026-11-17 14:53:21'),(526,'lukeskywalker@gmail.com',0,'2026-11-17 14:55:01'),(527,'lukeskywalker@gmail.com',1,'2026-11-17 14:55:09'),(528,'lukeskywalker@gmail.com',0,'2026-11-17 14:55:26'),(529,'lukeskywalker@gmail.com',1,'2026-11-17 14:56:48'),(530,'testdriver@example.com',1,'2026-11-17 14:57:28'),(531,'chosenone@gmail.com',1,'2026-11-17 15:00:05'),(532,'testdriver@example.com',1,'2026-11-17 15:00:21'),(533,'chosenone@gmail.com',1,'2026-11-17 15:01:11'),(534,'bwayne@gmail.com',1,'2026-11-17 15:01:33'),(535,'testdriver@example.com',1,'2026-11-17 15:01:59'),(536,'chosenone@gmail.com',1,'2026-11-17 15:02:34'),(537,'testdriver@example.com',1,'2026-11-17 15:03:01'),(538,'testdriver@example.com',1,'2026-11-17 15:06:00'),(539,'testdriver@example.com',1,'2026-11-17 15:08:15'),(540,'testdriver@example.com',1,'2026-11-17 15:09:05'),(541,'testdriver@example.com',1,'2026-11-17 15:16:58'),(542,'testdriver@example.com',1,'2026-11-17 15:18:36'),(543,'testdriver@example.com',1,'2026-11-17 15:18:43'),(544,'chosenone@gmail.com',1,'2026-11-17 15:18:52'),(545,'indianajones@gmail.com',1,'2026-11-17 15:21:20'),(546,'bwayne@gmail.com',1,'2026-11-17 15:26:32'),(547,'indianajones@gmail.com',1,'2026-11-17 15:29:20'),(548,'chosenone@gmail.com',1,'2026-11-17 16:28:36'),(549,'chosenone@gmail.com',1,'2026-11-17 16:34:00'),(550,'admin@gmail.com',1,'2026-11-17 17:50:21'),(551,'admin@gmail.com',1,'2026-11-17 17:55:07'),(552,'admin@gmail.com',1,'2026-11-17 18:29:22'),(553,'bwayne@gmail.com',1,'2026-11-17 18:32:32'),(554,'admin@gmail.com',1,'2026-11-17 18:35:10'),(555,'bwayne@gmail.com',1,'2026-11-17 19:25:46'),(556,'admin@gmail.com',1,'2026-11-17 19:26:34'),(557,'indianajones@gmail.com',1,'2026-11-17 19:30:01'),(558,'bwayne@gmail.com',1,'2026-11-17 19:32:25'),(559,'mail_name',1,'2026-11-17 20:21:34'),(560,'mail_name',1,'2026-11-17 20:26:51'),(561,'mail_name',1,'2026-11-17 20:44:57'),(562,'bwayne@gmail.com',1,'2026-11-17 22:31:32'),(563,'bwayne@gmail.com',1,'2026-11-17 22:53:27'),(564,'bwayne@gmail.com',1,'2026-11-17 23:03:35'),(565,'bwayne@gmail.com',1,'2026-11-17 23:09:24'),(566,'admin@gmail.com',1,'2026-11-17 23:38:44'),(567,'admin@gmail.com',1,'2026-11-17 23:41:08'),(568,'mail_name',1,'2026-11-17 23:42:29'),(569,'mail_name',1,'2026-11-18 00:09:30'),(570,'admin@gmail.com',1,'2026-11-18 00:09:54'),(571,'chosenone@gmail.com',1,'2026-11-18 14:44:33'),(572,'chosenone@gmail.com',1,'2026-11-18 15:04:12'),(573,'admin@gmail.com',1,'2026-11-19 15:08:55'),(574,'bwayne@gmail.com',1,'2026-11-19 16:22:29');
/*!40000 ALTER TABLE `LOGINATTEMPTS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `NOTIFICATIONS`
--

DROP TABLE IF EXISTS `NOTIFICATIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NOTIFICATIONS` (
  `NOTIFICATION_ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `NOTIFICATION_TYPE` varchar(50) NOT NULL,
  `TITLE` varchar(150) NOT NULL,
  `MESSAGE` varchar(500) NOT NULL,
  `IS_READ` tinyint(1) NOT NULL DEFAULT '0',
  `CREATED_DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `POINTCHANGE_ID` int DEFAULT NULL,
  `APPLICATION_ID` int DEFAULT NULL,
  PRIMARY KEY (`NOTIFICATION_ID`),
  KEY `IDX_NOTIFICATIONS_USER_DATE` (`USER_ID`,`CREATED_DTS`),
  KEY `IDX_NOTIFICATIONS_USER_READ` (`USER_ID`,`IS_READ`),
  KEY `FK_NOTIFICATIONS_POINTCHANGE` (`POINTCHANGE_ID`),
  KEY `FK_NOTIFICATIONS_APPLICATION` (`APPLICATION_ID`),
  CONSTRAINT `FK_NOTIFICATIONS_APPLICATION` FOREIGN KEY (`APPLICATION_ID`) REFERENCES `APPLICATIONS` (`APPLICATION_ID`) ON DELETE SET NULL,
  CONSTRAINT `FK_NOTIFICATIONS_POINTCHANGE` FOREIGN KEY (`POINTCHANGE_ID`) REFERENCES `POINTCHANGES` (`POINTCHANGE_ID`) ON DELETE SET NULL,
  CONSTRAINT `FK_NOTIFICATIONS_USER` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=272 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `NOTIFICATIONS`
--

LOCK TABLES `NOTIFICATIONS` WRITE;
/*!40000 ALTER TABLE `NOTIFICATIONS` DISABLE KEYS */;
INSERT INTO `NOTIFICATIONS` VALUES (1,5,'POINTS_GAINED','You earned points!','You received 10 points from The Comp. Reason: please notifications!. Your new balance is 29406 points.',0,'2026-10-30 20:19:42',61,NULL),(2,2,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: please notifications!. New balance: 29406 points.',1,'2026-10-30 20:19:43',61,NULL),(3,6,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: please notifications!. New balance: 29406 points.',1,'2026-10-30 20:19:43',61,NULL),(4,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: please notifications!. New balance: 29406 points.',0,'2026-10-30 20:19:43',61,NULL),(5,1,'POINTS_GAINED','You earned points!','You received 10 points from The Comp. Reason: notification test. Your new balance is 378478 points.',0,'2026-10-30 20:24:20',62,NULL),(6,2,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 378478 points.',1,'2026-10-30 20:24:20',62,NULL),(7,6,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 378478 points.',1,'2026-10-30 20:24:21',62,NULL),(8,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 378478 points.',0,'2026-10-30 20:24:21',62,NULL),(9,3,'POINTS_GAINED','You earned points!','You received 10 points from The Comp. Reason: notification test. Your new balance is 1955 points.',0,'2026-10-30 20:24:21',63,NULL),(10,2,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 1955 points.',0,'2026-10-30 20:24:21',63,NULL),(11,6,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 1955 points.',1,'2026-10-30 20:24:21',63,NULL),(12,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 1955 points.',0,'2026-10-30 20:24:21',63,NULL),(13,4,'POINTS_GAINED','You earned points!','You received 10 points from The Comp. Reason: notification test. Your new balance is 109 points.',0,'2026-10-30 20:24:21',64,NULL),(14,2,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 109 points.',0,'2026-10-30 20:24:21',64,NULL),(15,6,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 109 points.',1,'2026-10-30 20:24:21',64,NULL),(16,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 109 points.',0,'2026-10-30 20:24:21',64,NULL),(17,5,'POINTS_GAINED','You earned points!','You received 10 points from The Comp. Reason: notification test. Your new balance is 29416 points.',0,'2026-10-30 20:24:21',65,NULL),(18,2,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 29416 points.',0,'2026-10-30 20:24:21',65,NULL),(19,6,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 29416 points.',1,'2026-10-30 20:24:21',65,NULL),(20,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 29416 points.',0,'2026-10-30 20:24:22',65,NULL),(21,12,'POINTS_GAINED','You earned points!','You received 10 points from The Comp. Reason: notification test. Your new balance is 108 points.',0,'2026-10-30 20:24:22',66,NULL),(22,2,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 108 points.',0,'2026-10-30 20:24:22',66,NULL),(23,6,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 108 points.',1,'2026-10-30 20:24:22',66,NULL),(24,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 108 points.',0,'2026-10-30 20:24:22',66,NULL),(25,13,'POINTS_GAINED','You earned points!','You received 10 points from The Comp. Reason: notification test. Your new balance is 2059 points.',0,'2026-10-30 20:24:22',67,NULL),(26,2,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 2059 points.',0,'2026-10-30 20:24:22',67,NULL),(27,6,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 2059 points.',1,'2026-10-30 20:24:22',67,NULL),(28,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at The Comp. Reason: notification test. New balance: 2059 points.',0,'2026-10-30 20:24:22',67,NULL),(29,12,'APPLICATION_ACCEPTED','Application accepted!','Your application to join The Comp has been accepted.',0,'2026-10-30 20:38:26',NULL,7),(30,12,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with The Comp. You can begin earning points through this company.',0,'2026-10-30 20:38:26',NULL,7),(31,2,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join The Comp was accepted. The driver is now connected with your company.',0,'2026-10-30 20:38:26',NULL,7),(32,5,'POINTS_GAINED','You earned points!','You received 1 points from The Comp. Reason: test. Your new balance is 29417 points.',0,'2026-10-30 21:28:01',68,NULL),(33,2,'SPONSOR_POINT_CHANGE','Driver points Updated','1 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 29417 points.',0,'2026-10-30 21:28:01',68,NULL),(34,6,'ADMIN_POINT_CHANGE','Driver points Updated','1 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 29417 points.',1,'2026-10-30 21:28:01',68,NULL),(35,9,'ADMIN_POINT_CHANGE','Driver points Updated','1 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 29417 points.',0,'2026-10-30 21:28:01',68,NULL),(36,2,'SPONSOR_NEW_APPLICATION','New driver application','eric cartman has applied to join The Comp.',0,'2026-10-30 21:40:52',NULL,16),(37,6,'ADMIN_NEW_APPLICATION','New driver application','eric cartman has applied to join The Comp.',1,'2026-10-30 21:40:52',NULL,16),(38,9,'ADMIN_NEW_APPLICATION','New driver application','eric cartman has applied to join The Comp.',0,'2026-10-30 21:40:52',NULL,16),(39,5,'POINTS_GAINED','You earned points!','You received 1 points from The Comp. Reason: notif preference test. Your new balance is 29423 points.',0,'2026-10-31 11:20:08',82,NULL),(40,2,'SPONSOR_POINT_CHANGE','Driver points Updated','1 points were added to a driver\'s balance at The Comp. Reason: notif preference test. New balance: 29423 points.',0,'2026-10-31 11:20:08',82,NULL),(41,9,'ADMIN_POINT_CHANGE','Driver points Updated','1 points were added to a driver\'s balance at The Comp. Reason: notif preference test. New balance: 29423 points.',0,'2026-10-31 11:20:08',82,NULL),(43,7,'SPONSOR_POINT_CHANGE','Driver points Updated','19 points were added to a driver\'s balance at LexCorps. Reason: test if gets points. New balance: 19 points.',0,'2026-11-03 15:25:59',NULL,NULL),(44,10,'SPONSOR_POINT_CHANGE','Driver points Updated','19 points were added to a driver\'s balance at LexCorps. Reason: test if gets points. New balance: 19 points.',0,'2026-11-03 15:25:59',NULL,NULL),(45,11,'SPONSOR_POINT_CHANGE','Driver points Updated','19 points were added to a driver\'s balance at LexCorps. Reason: test if gets points. New balance: 19 points.',0,'2026-11-03 15:25:59',NULL,NULL),(46,9,'ADMIN_POINT_CHANGE','Driver points Updated','19 points were added to a driver\'s balance at LexCorps. Reason: test if gets points. New balance: 19 points.',0,'2026-11-03 15:25:59',NULL,NULL),(47,7,'SPONSOR_NEW_APPLICATION','New driver application','Mike Tiger has applied to join LexCorps.',0,'2026-11-04 14:09:00',NULL,17),(48,10,'SPONSOR_NEW_APPLICATION','New driver application','Mike Tiger has applied to join LexCorps.',0,'2026-11-04 14:09:00',NULL,17),(49,11,'SPONSOR_NEW_APPLICATION','New driver application','Mike Tiger has applied to join LexCorps.',0,'2026-11-04 14:09:00',NULL,17),(50,9,'ADMIN_NEW_APPLICATION','New driver application','Mike Tiger has applied to join LexCorps.',0,'2026-11-04 14:09:00',NULL,17),(51,2,'SPONSOR_NEW_APPLICATION','New driver application','Mike Tiger has applied to join The Comp.',0,'2026-11-05 12:55:38',NULL,19),(52,9,'ADMIN_NEW_APPLICATION','New driver application','Mike Tiger has applied to join The Comp.',0,'2026-11-05 12:55:38',NULL,19),(53,21,'DRIVER_SPONSOR_REMOVED','Sponsor connection ended','You are no longer connected with LexCorps.',0,'2026-11-06 19:17:00',NULL,NULL),(54,7,'SPONSOR_DRIVER_REMOVED','Driver removed','Gro Gu was removed from LexCorps.',0,'2026-11-06 19:17:00',NULL,NULL),(55,10,'SPONSOR_DRIVER_REMOVED','Driver removed','Gro Gu was removed from LexCorps.',0,'2026-11-06 19:17:00',NULL,NULL),(56,11,'SPONSOR_DRIVER_REMOVED','Driver removed','Gro Gu was removed from LexCorps.',0,'2026-11-06 19:17:00',NULL,NULL),(57,6,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','Gro Gu was removed from LexCorps.',1,'2026-11-06 19:17:01',NULL,NULL),(58,9,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','Gro Gu was removed from LexCorps.',0,'2026-11-06 19:17:01',NULL,NULL),(59,12,'DRIVER_SPONSOR_REMOVED','Sponsor connection ended','You are no longer connected with The Comp.',0,'2026-11-06 19:17:23',NULL,NULL),(60,2,'SPONSOR_DRIVER_REMOVED','Driver removed','Han Solo was removed from The Comp.',0,'2026-11-06 19:17:23',NULL,NULL),(61,6,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','Han Solo was removed from The Comp.',0,'2026-11-06 19:17:23',NULL,NULL),(62,9,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','Han Solo was removed from The Comp.',0,'2026-11-06 19:17:23',NULL,NULL),(63,7,'SPONSOR_NEW_APPLICATION','New driver application','hello world has applied to join LexCorps.',0,'2026-11-06 19:22:26',NULL,20),(64,10,'SPONSOR_NEW_APPLICATION','New driver application','hello world has applied to join LexCorps.',0,'2026-11-06 19:22:26',NULL,20),(65,11,'SPONSOR_NEW_APPLICATION','New driver application','hello world has applied to join LexCorps.',0,'2026-11-06 19:22:26',NULL,20),(66,9,'ADMIN_NEW_APPLICATION','New driver application','hello world has applied to join LexCorps.',0,'2026-11-06 19:22:26',NULL,20),(67,2,'SPONSOR_NEW_APPLICATION','New driver application','hello world has applied to join The Comp.',0,'2026-11-06 19:23:17',NULL,21),(68,9,'ADMIN_NEW_APPLICATION','New driver application','hello world has applied to join The Comp.',0,'2026-11-06 19:23:17',NULL,21),(69,34,'APPLICATION_ACCEPTED','Application accepted!','Your application to join The Comp has been accepted.',0,'2026-11-06 19:24:03',NULL,21),(70,34,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with The Comp. You can begin earning points through this company.',0,'2026-11-06 19:24:03',NULL,21),(71,2,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join The Comp was accepted. The driver is now connected with your company.',0,'2026-11-06 19:24:03',NULL,21),(72,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','hello world was accepted by The Comp. The driver is now connected with this sponsor.',0,'2026-11-06 19:24:03',NULL,21),(73,34,'DRIVER_SPONSOR_REMOVED','Sponsor connection ended','You are no longer connected with The Comp.',1,'2026-11-06 19:24:36',NULL,NULL),(74,2,'SPONSOR_DRIVER_REMOVED','Driver removed','hello world was removed from The Comp.',0,'2026-11-06 19:24:36',NULL,NULL),(75,6,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','hello world was removed from The Comp.',0,'2026-11-06 19:24:36',NULL,NULL),(76,9,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','hello world was removed from The Comp.',0,'2026-11-06 19:24:36',NULL,NULL),(77,13,'POINTS_GAINED','You earned points!','You received 3000 points from The Comp. Reason: Headpiece to the Staff of Ra. Your new balance is 4984 points.',0,'2026-11-09 01:13:50',88,NULL),(78,2,'SPONSOR_POINT_CHANGE','Driver points Updated','3000 points were added to a driver\'s balance at The Comp. Reason: Headpiece to the Staff of Ra. New balance: 4984 points.',0,'2026-11-09 01:13:50',88,NULL),(79,9,'ADMIN_POINT_CHANGE','Driver points Updated','3000 points were added to a driver\'s balance at The Comp. Reason: Headpiece to the Staff of Ra. New balance: 4984 points.',0,'2026-11-09 01:13:50',88,NULL),(80,2,'SPONSOR_NEW_APPLICATION','New driver application','Jason Zheng has applied to join The Comp.',0,'2026-11-09 14:14:08',NULL,22),(81,9,'ADMIN_NEW_APPLICATION','New driver application','Jason Zheng has applied to join The Comp.',0,'2026-11-09 14:14:08',NULL,22),(82,7,'SPONSOR_NEW_APPLICATION','New driver application','John Smith has applied to join LexCorps.',0,'2026-11-09 14:16:09',NULL,23),(83,10,'SPONSOR_NEW_APPLICATION','New driver application','John Smith has applied to join LexCorps.',0,'2026-11-09 14:16:09',NULL,23),(84,11,'SPONSOR_NEW_APPLICATION','New driver application','John Smith has applied to join LexCorps.',0,'2026-11-09 14:16:09',NULL,23),(85,9,'ADMIN_NEW_APPLICATION','New driver application','John Smith has applied to join LexCorps.',0,'2026-11-09 14:16:09',NULL,23),(86,7,'SPONSOR_NEW_APPLICATION','New driver application','admin adminson has applied to join LexCorps.',0,'2026-11-09 14:16:43',NULL,24),(87,10,'SPONSOR_NEW_APPLICATION','New driver application','admin adminson has applied to join LexCorps.',0,'2026-11-09 14:16:43',NULL,24),(88,11,'SPONSOR_NEW_APPLICATION','New driver application','admin adminson has applied to join LexCorps.',0,'2026-11-09 14:16:43',NULL,24),(89,9,'ADMIN_NEW_APPLICATION','New driver application','admin adminson has applied to join LexCorps.',0,'2026-11-09 14:16:43',NULL,24),(90,35,'APPLICATION_ACCEPTED','Application accepted!','Your application to join The Comp has been accepted.',0,'2026-11-09 14:17:27',NULL,22),(91,35,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with The Comp. You can begin earning points through this company.',0,'2026-11-09 14:17:27',NULL,22),(92,2,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join The Comp was accepted. The driver is now connected with your company.',1,'2026-11-09 14:17:27',NULL,22),(93,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','Jason Zhengg was accepted by The Comp. The driver is now connected with this sponsor.',0,'2026-11-09 14:17:27',NULL,22),(94,35,'POINTS_GAINED','You earned points!','You received 100 points from The Comp. Reason: Test. Your new balance is 100 points.',1,'2026-11-09 14:17:51',90,NULL),(95,2,'SPONSOR_POINT_CHANGE','Driver points Updated','100 points were added to a driver\'s balance at The Comp. Reason: Test. New balance: 100 points.',1,'2026-11-09 14:17:51',90,NULL),(96,9,'ADMIN_POINT_CHANGE','Driver points Updated','100 points were added to a driver\'s balance at The Comp. Reason: Test. New balance: 100 points.',0,'2026-11-09 14:17:51',90,NULL),(97,7,'SPONSOR_NEW_APPLICATION','New driver application','Emma Kropf has applied to join LexCorps.',0,'2026-11-09 14:19:47',NULL,25),(98,10,'SPONSOR_NEW_APPLICATION','New driver application','Emma Kropf has applied to join LexCorps.',0,'2026-11-09 14:19:47',NULL,25),(99,11,'SPONSOR_NEW_APPLICATION','New driver application','Emma Kropf has applied to join LexCorps.',0,'2026-11-09 14:19:47',NULL,25),(100,9,'ADMIN_NEW_APPLICATION','New driver application','Emma Kropf has applied to join LexCorps.',0,'2026-11-09 14:19:47',NULL,25),(101,36,'APPLICATION_ACCEPTED','Application accepted!','Your application to join LexCorps has been accepted.',0,'2026-11-09 14:21:57',NULL,23),(102,36,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with LexCorps. You can begin earning points through this company.',0,'2026-11-09 14:21:57',NULL,23),(103,7,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-09 14:21:57',NULL,23),(104,10,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-09 14:21:57',NULL,23),(105,11,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-09 14:21:57',NULL,23),(106,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','John Smith was accepted by LexCorps. The driver is now connected with this sponsor.',0,'2026-11-09 14:21:57',NULL,23),(107,36,'POINTS_GAINED','You earned points!','You received 100 points from LexCorps. Reason: test. Your new balance is 100 points.',0,'2026-11-09 14:22:24',91,NULL),(108,7,'SPONSOR_POINT_CHANGE','Driver points Updated','100 points were added to a driver\'s balance at LexCorps. Reason: test. New balance: 100 points.',0,'2026-11-09 14:22:24',91,NULL),(109,10,'SPONSOR_POINT_CHANGE','Driver points Updated','100 points were added to a driver\'s balance at LexCorps. Reason: test. New balance: 100 points.',0,'2026-11-09 14:22:24',91,NULL),(110,11,'SPONSOR_POINT_CHANGE','Driver points Updated','100 points were added to a driver\'s balance at LexCorps. Reason: test. New balance: 100 points.',0,'2026-11-09 14:22:24',91,NULL),(111,9,'ADMIN_POINT_CHANGE','Driver points Updated','100 points were added to a driver\'s balance at LexCorps. Reason: test. New balance: 100 points.',0,'2026-11-09 14:22:24',91,NULL),(112,37,'APPLICATION_ACCEPTED','Application accepted!','Your application to join LexCorps has been accepted.',0,'2026-11-09 14:24:42',NULL,25),(113,37,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with LexCorps. You can begin earning points through this company.',0,'2026-11-09 14:24:42',NULL,25),(114,7,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-09 14:24:42',NULL,25),(115,10,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-09 14:24:42',NULL,25),(116,11,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-09 14:24:42',NULL,25),(117,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','Emma Kropf was accepted by LexCorps. The driver is now connected with this sponsor.',0,'2026-11-09 14:24:42',NULL,25),(118,33,'APPLICATION_REJECTED','Application update','Your application to join LexCorps was not accepted.',0,'2026-11-09 14:39:43',NULL,17),(119,37,'POINTS_GAINED','You earned points!','You received 1000000000000000000000000000000000000 points from LexCorps. Reason: Because shes great. Your new balance is 1e+36 points.',0,'2026-11-09 14:44:44',94,NULL),(120,7,'SPONSOR_POINT_CHANGE','Driver points Updated','1000000000000000000000000000000000000 points were added to a driver\'s balance at LexCorps. Reason: Because shes great. New balance: 1e+36 points.',0,'2026-11-09 14:44:44',94,NULL),(121,10,'SPONSOR_POINT_CHANGE','Driver points Updated','1000000000000000000000000000000000000 points were added to a driver\'s balance at LexCorps. Reason: Because shes great. New balance: 1e+36 points.',0,'2026-11-09 14:44:44',94,NULL),(122,11,'SPONSOR_POINT_CHANGE','Driver points Updated','1000000000000000000000000000000000000 points were added to a driver\'s balance at LexCorps. Reason: Because shes great. New balance: 1e+36 points.',0,'2026-11-09 14:44:44',94,NULL),(123,9,'ADMIN_POINT_CHANGE','Driver points Updated','1000000000000000000000000000000000000 points were added to a driver\'s balance at LexCorps. Reason: Because shes great. New balance: 1e+36 points.',0,'2026-11-09 14:44:44',94,NULL),(124,1,'POINTS_GAINED','You earned points!','You received 2341 points from The Comp. Reason: for being a good test sub. Your new balance is 380076 points.',0,'2026-11-10 19:21:01',100,NULL),(125,2,'SPONSOR_POINT_CHANGE','Driver points Updated','2341 points were added to a driver\'s balance at The Comp. Reason: for being a good test sub. New balance: 380076 points.',1,'2026-11-10 19:21:02',100,NULL),(126,9,'ADMIN_POINT_CHANGE','Driver points Updated','2341 points were added to a driver\'s balance at The Comp. Reason: for being a good test sub. New balance: 380076 points.',0,'2026-11-10 19:21:02',100,NULL),(127,5,'DRIVER_SPONSOR_REMOVED','Sponsor connection ended','You are no longer connected with The Comp.',0,'2026-11-12 19:40:46',NULL,NULL),(128,2,'SPONSOR_DRIVER_REMOVED','Driver removed','Maria Egg was removed from The Comp.',0,'2026-11-12 19:40:46',NULL,NULL),(129,6,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','Maria Egg was removed from The Comp.',0,'2026-11-12 19:40:46',NULL,NULL),(130,9,'ADMIN_DRIVER_REMOVED','Driver removed from sponsor company','Maria Egg was removed from The Comp.',0,'2026-11-12 19:40:46',NULL,NULL),(131,13,'POINTS_GAINED','You earned points!','You received 17000 points from The Comp. Reason: Those guys must really be desperate. Your new balance is 20831 points.',0,'2026-11-13 14:53:23',104,NULL),(132,2,'SPONSOR_POINT_CHANGE','Driver points Updated','17000 points were added to a driver\'s balance at The Comp. Reason: Those guys must really be desperate. New balance: 20831 points.',0,'2026-11-13 14:53:24',104,NULL),(133,9,'ADMIN_POINT_CHANGE','Driver points Updated','17000 points were added to a driver\'s balance at The Comp. Reason: Those guys must really be desperate. New balance: 20831 points.',0,'2026-11-13 14:53:24',104,NULL),(134,3,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-13 16:44:57',NULL,NULL),(135,3,'PROFILE_UPDATED','Profile Updated','Your last name has been updated.',0,'2026-11-13 16:45:30',NULL,NULL),(136,3,'PROFILE_UPDATED','Profile Updated','Your password has been updated.',0,'2026-11-13 16:45:47',NULL,NULL),(137,2,'SPONSOR_ITEM_ADDED','Item added to catalog','You added \'dinosaur\' to your company catalog.',0,'2026-11-13 17:28:47',NULL,NULL),(138,2,'SPONSOR_ITEM_REMOVED','Item removed from catalog','You removed \'dinosaur\' from your company catalog.',0,'2026-11-13 17:29:29',NULL,NULL),(139,2,'SPONSOR_ITEM_ADDED','Item added to catalog','You added \'dinosaur\' to your company catalog.',0,'2026-11-13 18:26:08',NULL,NULL),(140,2,'SPONSOR_ITEM_REMOVED','Item removed from catalog','You removed \'dinosaur\' from your company catalog.',0,'2026-11-13 18:26:14',NULL,NULL),(141,27,'APPLICATION_ACCEPTED','Application accepted!','Your application to join The Comp has been accepted.',0,'2026-11-13 18:30:14',NULL,16),(142,27,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with The Comp. You can begin earning points through this company.',0,'2026-11-13 18:30:14',NULL,16),(143,2,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join The Comp was accepted. The driver is now connected with your company.',0,'2026-11-13 18:30:14',NULL,16),(144,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','eric cartman was accepted by The Comp. The driver is now connected with this sponsor.',0,'2026-11-13 18:30:14',NULL,16),(145,3,'DRIVER_CART_ADDED','Item added to cart','You added an item to your cart.',0,'2026-11-13 18:47:04',NULL,NULL),(146,3,'DRIVER_CART_REMOVED','Item removed from cart','You removed an item from your cart.',0,'2026-11-13 18:47:27',NULL,NULL),(147,3,'DRIVER_CART_ADDED','Item added to cart','You added an item to your cart.',0,'2026-11-13 19:10:00',NULL,NULL),(148,2,'DRIVER_ORDER_PLACED','Order placed','Your order #18 was successfully placed.',0,'2026-11-13 19:10:16',NULL,NULL),(149,2,'SPONSOR_ORDER_PLACED','New driver order','A new order #18 was placed by a driver.',0,'2026-11-13 19:10:16',NULL,NULL),(150,6,'ADMIN_ORDER_PLACED','New driver order','A new order #18 was placed by a driver.',0,'2026-11-13 19:10:16',NULL,NULL),(151,9,'ADMIN_ORDER_PLACED','New driver order','A new order #18 was placed by a driver.',0,'2026-11-13 19:10:16',NULL,NULL),(152,3,'DRIVER_ORDER_CANCELED','Order canceled','Your order #18 was successfully canceled.',0,'2026-11-13 19:10:43',NULL,NULL),(153,2,'SPONSOR_ORDER_CANCELED','Driver canceled order','A driver canceled order #18.',0,'2026-11-13 19:10:43',NULL,NULL),(154,6,'ADMIN_ORDER_CANCELED','Driver canceled order','A driver canceled order #18.',0,'2026-11-13 19:10:43',NULL,NULL),(155,9,'ADMIN_ORDER_CANCELED','Driver canceled order','A driver canceled order #18.',0,'2026-11-13 19:10:43',NULL,NULL),(156,3,'DRIVER_CART_ADDED','Item added to cart','You added an item to your cart.',0,'2026-11-13 19:21:21',NULL,NULL),(157,3,'DRIVER_ORDER_PLACED','Order placed','Your order #19 was successfully placed.',0,'2026-11-13 19:21:29',NULL,NULL),(158,2,'SPONSOR_ORDER_PLACED','New driver order','A new order #19 was placed by a driver.',0,'2026-11-13 19:21:29',NULL,NULL),(159,6,'ADMIN_ORDER_PLACED','New driver order','A new order #19 was placed by a driver.',0,'2026-11-13 19:21:29',NULL,NULL),(160,9,'ADMIN_ORDER_PLACED','New driver order','A new order #19 was placed by a driver.',0,'2026-11-13 19:21:29',NULL,NULL),(161,9,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 16:15:34',NULL,NULL),(162,9,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 16:15:39',NULL,NULL),(163,13,'DRIVER_CART_ADDED','Item added to cart','You added an item to your cart.',0,'2026-11-15 17:01:01',NULL,NULL),(164,13,'DRIVER_ORDER_PLACED','Order placed','Your order #20 was successfully placed.',0,'2026-11-15 17:01:21',NULL,NULL),(165,2,'SPONSOR_ORDER_PLACED','New driver order','A new order #20 was placed by a driver.',0,'2026-11-15 17:01:21',NULL,NULL),(166,6,'ADMIN_ORDER_PLACED','New driver order','A new order #20 was placed by a driver.',0,'2026-11-15 17:01:21',NULL,NULL),(167,9,'ADMIN_ORDER_PLACED','New driver order','A new order #20 was placed by a driver.',0,'2026-11-15 17:01:21',NULL,NULL),(168,13,'DRIVER_ORDER_CANCELED','Order canceled','Your order #20 was successfully canceled.',0,'2026-11-15 17:01:43',NULL,NULL),(169,2,'SPONSOR_ORDER_CANCELED','Driver canceled order','A driver canceled order #20.',0,'2026-11-15 17:01:43',NULL,NULL),(170,6,'ADMIN_ORDER_CANCELED','Driver canceled order','A driver canceled order #20.',0,'2026-11-15 17:01:43',NULL,NULL),(171,9,'ADMIN_ORDER_CANCELED','Driver canceled order','A driver canceled order #20.',0,'2026-11-15 17:01:44',NULL,NULL),(172,13,'DRIVER_CART_ADDED','Item added to cart','You added an item to your cart.',0,'2026-11-15 17:03:06',NULL,NULL),(173,13,'DRIVER_ORDER_PLACED','Order placed','Your order #21 was successfully placed.',0,'2026-11-15 17:03:26',NULL,NULL),(174,2,'SPONSOR_ORDER_PLACED','New driver order','A new order #21 was placed by a driver.',0,'2026-11-15 17:03:26',NULL,NULL),(175,6,'ADMIN_ORDER_PLACED','New driver order','A new order #21 was placed by a driver.',0,'2026-11-15 17:03:26',NULL,NULL),(176,9,'ADMIN_ORDER_PLACED','New driver order','A new order #21 was placed by a driver.',0,'2026-11-15 17:03:26',NULL,NULL),(177,13,'DRIVER_ORDER_CANCELED','Order canceled','Your order #21 was successfully canceled.',0,'2026-11-15 17:03:50',NULL,NULL),(178,2,'SPONSOR_ORDER_CANCELED','Driver canceled order','A driver canceled order #21.',0,'2026-11-15 17:03:50',NULL,NULL),(179,6,'ADMIN_ORDER_CANCELED','Driver canceled order','A driver canceled order #21.',0,'2026-11-15 17:03:50',NULL,NULL),(180,9,'ADMIN_ORDER_CANCELED','Driver canceled order','A driver canceled order #21.',0,'2026-11-15 17:03:50',NULL,NULL),(181,3,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:15:39',NULL,NULL),(182,3,'PROFILE_UPDATED','Profile Updated','Your last name has been updated.',0,'2026-11-15 18:15:42',NULL,NULL),(183,3,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:39:26',NULL,NULL),(184,3,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:39:30',NULL,NULL),(185,2,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:39:57',NULL,NULL),(186,2,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:40:01',NULL,NULL),(187,27,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:40:20',NULL,NULL),(188,11,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:41:54',NULL,NULL),(189,11,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:41:59',NULL,NULL),(190,27,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-15 18:42:10',NULL,NULL),(191,5,'PROFILE_UPDATED','Profile Updated','Your last name has been updated.',0,'2026-11-15 18:44:28',NULL,NULL),(192,5,'PROFILE_UPDATED','Profile Updated','Your last name has been updated.',0,'2026-11-15 18:44:31',NULL,NULL),(193,2,'SPONSOR_NEW_APPLICATION','New driver application','2_Job James has applied to join The Comp.',0,'2026-11-16 15:02:15',NULL,26),(194,9,'ADMIN_NEW_APPLICATION','New driver application','2_Job James has applied to join The Comp.',0,'2026-11-16 15:02:15',NULL,26),(195,7,'SPONSOR_NEW_APPLICATION','New driver application','2_Job James has applied to join LexCorps.',0,'2026-11-16 15:02:40',NULL,27),(196,10,'SPONSOR_NEW_APPLICATION','New driver application','2_Job James has applied to join LexCorps.',0,'2026-11-16 15:02:40',NULL,27),(197,11,'SPONSOR_NEW_APPLICATION','New driver application','2_Job James has applied to join LexCorps.',0,'2026-11-16 15:02:40',NULL,27),(198,9,'ADMIN_NEW_APPLICATION','New driver application','2_Job James has applied to join LexCorps.',0,'2026-11-16 15:02:40',NULL,27),(199,38,'APPLICATION_ACCEPTED','Application accepted!','Your application to join The Comp has been accepted.',0,'2026-11-16 15:03:21',NULL,26),(200,38,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with The Comp. You can begin earning points through this company.',0,'2026-11-16 15:03:21',NULL,26),(201,2,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join The Comp was accepted. The driver is now connected with your company.',0,'2026-11-16 15:03:21',NULL,26),(202,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','2_Job James was accepted by The Comp. The driver is now connected with this sponsor.',0,'2026-11-16 15:03:21',NULL,26),(203,38,'APPLICATION_ACCEPTED','Application accepted!','Your application to join LexCorps has been accepted.',0,'2026-11-16 15:04:31',NULL,27),(204,38,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with LexCorps. You can begin earning points through this company.',0,'2026-11-16 15:04:31',NULL,27),(205,7,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-16 15:04:31',NULL,27),(206,10,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-16 15:04:32',NULL,27),(207,11,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-16 15:04:32',NULL,27),(208,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','2_Job James was accepted by LexCorps. The driver is now connected with this sponsor.',0,'2026-11-16 15:04:32',NULL,27),(209,38,'POINTS_GAINED','You earned points!','You received 200 points from The Comp. Reason: test. Your new balance is 200 points.',0,'2026-11-16 15:46:49',116,NULL),(210,2,'SPONSOR_POINT_CHANGE','Driver points Updated','200 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 200 points.',0,'2026-11-16 15:46:49',116,NULL),(211,9,'ADMIN_POINT_CHANGE','Driver points Updated','200 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 200 points.',0,'2026-11-16 15:46:49',116,NULL),(212,38,'POINTS_GAINED','You earned points!','You received 589 points from LexCorps. Reason: poor boy get his point. Your new balance is 589 points.',0,'2026-11-16 15:50:08',117,NULL),(213,7,'SPONSOR_POINT_CHANGE','Driver points Updated','589 points were added to a driver\'s balance at LexCorps. Reason: poor boy get his point. New balance: 589 points.',0,'2026-11-16 15:50:08',117,NULL),(214,10,'SPONSOR_POINT_CHANGE','Driver points Updated','589 points were added to a driver\'s balance at LexCorps. Reason: poor boy get his point. New balance: 589 points.',0,'2026-11-16 15:50:08',117,NULL),(215,11,'SPONSOR_POINT_CHANGE','Driver points Updated','589 points were added to a driver\'s balance at LexCorps. Reason: poor boy get his point. New balance: 589 points.',0,'2026-11-16 15:50:08',117,NULL),(216,9,'ADMIN_POINT_CHANGE','Driver points Updated','589 points were added to a driver\'s balance at LexCorps. Reason: poor boy get his point. New balance: 589 points.',0,'2026-11-16 15:50:08',117,NULL),(217,38,'DRIVER_CART_ADDED','Item added to cart','You added an item to your cart.',0,'2026-11-16 17:15:42',NULL,NULL),(218,38,'DRIVER_ORDER_PLACED','Order placed','Your order #23 was successfully placed.',0,'2026-11-16 17:15:59',NULL,NULL),(219,7,'SPONSOR_ORDER_PLACED','New driver order','A new order #23 was placed by a driver.',0,'2026-11-16 17:16:00',NULL,NULL),(220,10,'SPONSOR_ORDER_PLACED','New driver order','A new order #23 was placed by a driver.',0,'2026-11-16 17:16:00',NULL,NULL),(221,11,'SPONSOR_ORDER_PLACED','New driver order','A new order #23 was placed by a driver.',0,'2026-11-16 17:16:00',NULL,NULL),(222,6,'ADMIN_ORDER_PLACED','New driver order','A new order #23 was placed by a driver.',0,'2026-11-16 17:16:00',NULL,NULL),(223,9,'ADMIN_ORDER_PLACED','New driver order','A new order #23 was placed by a driver.',0,'2026-11-16 17:16:00',NULL,NULL),(224,9,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-17 13:50:28',NULL,NULL),(225,9,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-17 13:50:29',NULL,NULL),(226,9,'PROFILE_UPDATED','Profile Updated','Your first name has been updated.',0,'2026-11-17 13:51:49',NULL,NULL),(227,1,'POINTS_GAINED','You earned points!','You received 5 points from The Comp. Reason: Automated Selenium test add 5 points 99e3055628ac4d4e9747eef6b3e9ef0a. Your new balance is 380081 points.',0,'2026-11-17 14:07:40',119,NULL),(228,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: Automated Selenium test add 5 points 99e3055628ac4d4e9747eef6b3e9ef0a. New balance: 380081 points.',0,'2026-11-17 14:07:40',119,NULL),(229,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: Automated Selenium test add 5 points 99e3055628ac4d4e9747eef6b3e9ef0a. New balance: 380081 points.',0,'2026-11-17 14:07:40',119,NULL),(230,1,'POINTS_LOST','Your points changed','5 points were deducted by The Comp. Reason: Automated Selenium test subtract 5 points 99e3055628ac4d4e9747eef6b3e9ef0a. Your new balance is 380076 points.',0,'2026-11-17 14:07:42',120,NULL),(231,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: Automated Selenium test subtract 5 points 99e3055628ac4d4e9747eef6b3e9ef0a. New balance: 380076 points.',0,'2026-11-17 14:07:42',120,NULL),(232,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: Automated Selenium test subtract 5 points 99e3055628ac4d4e9747eef6b3e9ef0a. New balance: 380076 points.',0,'2026-11-17 14:07:42',120,NULL),(233,1,'POINTS_GAINED','You earned points!','You received 5 points from The Comp. Reason: test. Your new balance is 380081 points.',0,'2026-11-17 14:09:24',121,NULL),(234,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 380081 points.',0,'2026-11-17 14:09:24',121,NULL),(235,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 380081 points.',0,'2026-11-17 14:09:24',121,NULL),(236,1,'POINTS_LOST','Your points changed','5 points were deducted by The Comp. Reason: test. Your new balance is 380076 points.',0,'2026-11-17 14:09:26',122,NULL),(237,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: test. New balance: 380076 points.',0,'2026-11-17 14:09:26',122,NULL),(238,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: test. New balance: 380076 points.',0,'2026-11-17 14:09:27',122,NULL),(239,7,'SPONSOR_NEW_APPLICATION','New driver application','John Driver has applied to join LexCorps.',0,'2026-11-17 14:56:36',NULL,28),(240,10,'SPONSOR_NEW_APPLICATION','New driver application','John Driver has applied to join LexCorps.',0,'2026-11-17 14:56:36',NULL,28),(241,11,'SPONSOR_NEW_APPLICATION','New driver application','John Driver has applied to join LexCorps.',0,'2026-11-17 14:56:36',NULL,28),(242,9,'ADMIN_NEW_APPLICATION','New driver application','John Driver has applied to join LexCorps.',0,'2026-11-17 14:56:36',NULL,28),(243,39,'APPLICATION_ACCEPTED','Application accepted!','Your application to join LexCorps has been accepted.',0,'2026-11-17 14:56:58',NULL,28),(244,39,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with LexCorps. You can begin earning points through this company.',0,'2026-11-17 14:56:58',NULL,28),(245,7,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-17 14:56:58',NULL,28),(246,10,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-17 14:56:58',NULL,28),(247,11,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join LexCorps was accepted. The driver is now connected with your company.',0,'2026-11-17 14:56:58',NULL,28),(248,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','John Driver was accepted by LexCorps. The driver is now connected with this sponsor.',0,'2026-11-17 14:56:58',NULL,28),(249,1,'POINTS_GAINED','You earned points!','You received 5 points from The Comp. Reason: test. Your new balance is 380081 points.',0,'2026-11-17 15:00:09',123,NULL),(250,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 380081 points.',0,'2026-11-17 15:00:09',123,NULL),(251,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 380081 points.',0,'2026-11-17 15:00:09',123,NULL),(252,1,'POINTS_LOST','Your points changed','5 points were deducted by The Comp. Reason: test. Your new balance is 380076 points.',0,'2026-11-17 15:00:11',124,NULL),(253,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: test. New balance: 380076 points.',0,'2026-11-17 15:00:11',124,NULL),(254,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: test. New balance: 380076 points.',0,'2026-11-17 15:00:11',124,NULL),(255,2,'SPONSOR_NEW_APPLICATION','New driver application','John Driver has applied to join The Comp.',0,'2026-11-17 15:00:47',NULL,29),(256,9,'ADMIN_NEW_APPLICATION','New driver application','John Driver has applied to join The Comp.',0,'2026-11-17 15:00:47',NULL,29),(257,39,'APPLICATION_ACCEPTED','Application accepted!','Your application to join The Comp has been accepted.',0,'2026-11-17 15:01:45',NULL,29),(258,39,'DRIVER_SPONSOR_ADDED','Sponsor added','You are now connected with The Comp. You can begin earning points through this company.',0,'2026-11-17 15:01:45',NULL,29),(259,2,'SPONSOR_DRIVER_ADDED','Driver added','A driver\'s application to join The Comp was accepted. The driver is now connected with your company.',0,'2026-11-17 15:01:45',NULL,29),(260,9,'ADMIN_APPLICATION_ACCEPTED','Driver application accepted','John Driver was accepted by The Comp. The driver is now connected with this sponsor.',0,'2026-11-17 15:01:45',NULL,29),(261,39,'POINTS_GAINED','You earned points!','You received 10 points from LexCorps. Reason: Test. Your new balance is 10 points.',0,'2026-11-17 15:02:53',125,NULL),(262,7,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at LexCorps. Reason: Test. New balance: 10 points.',0,'2026-11-17 15:02:53',125,NULL),(263,10,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at LexCorps. Reason: Test. New balance: 10 points.',0,'2026-11-17 15:02:53',125,NULL),(264,11,'SPONSOR_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at LexCorps. Reason: Test. New balance: 10 points.',0,'2026-11-17 15:02:53',125,NULL),(265,9,'ADMIN_POINT_CHANGE','Driver points Updated','10 points were added to a driver\'s balance at LexCorps. Reason: Test. New balance: 10 points.',0,'2026-11-17 15:02:53',125,NULL),(266,1,'POINTS_GAINED','You earned points!','You received 5 points from The Comp. Reason: test. Your new balance is 380081 points.',0,'2026-11-17 15:18:56',126,NULL),(267,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 380081 points.',0,'2026-11-17 15:18:56',126,NULL),(268,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were added to a driver\'s balance at The Comp. Reason: test. New balance: 380081 points.',0,'2026-11-17 15:18:56',126,NULL),(269,1,'POINTS_LOST','Your points changed','5 points were deducted by The Comp. Reason: test. Your new balance is 380076 points.',0,'2026-11-17 15:18:58',127,NULL),(270,2,'SPONSOR_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: test. New balance: 380076 points.',0,'2026-11-17 15:18:58',127,NULL),(271,9,'ADMIN_POINT_CHANGE','Driver points Updated','5 points were deducted from a driver\'s balance at The Comp. Reason: test. New balance: 380076 points.',0,'2026-11-17 15:18:58',127,NULL);
/*!40000 ALTER TABLE `NOTIFICATIONS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `NOTIFICATIONSETTINGS`
--

DROP TABLE IF EXISTS `NOTIFICATIONSETTINGS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NOTIFICATIONSETTINGS` (
  `SETTING_ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `NOTIFICATION_TYPE` varchar(50) NOT NULL,
  `IS_ENABLED` tinyint(1) NOT NULL DEFAULT '1',
  `CREATED_DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`SETTING_ID`),
  UNIQUE KEY `UQ_NOTIFICATIONSETTINGS_USER_TYPE` (`USER_ID`,`NOTIFICATION_TYPE`),
  CONSTRAINT `FK_NOTIFICATIONSETTINGS_USER` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `NOTIFICATIONSETTINGS`
--

LOCK TABLES `NOTIFICATIONSETTINGS` WRITE;
/*!40000 ALTER TABLE `NOTIFICATIONSETTINGS` DISABLE KEYS */;
INSERT INTO `NOTIFICATIONSETTINGS` VALUES (1,6,'POINTS_GAINED',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(2,6,'POINTS_LOST',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(3,6,'SPONSOR_POINT_CHANGE',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(4,6,'ADMIN_POINT_CHANGE',0,'2026-10-31 11:13:53','2026-11-17 18:39:48'),(5,6,'DRIVER_SPONSOR_ADDED',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(6,6,'DRIVER_SPONSOR_REMOVED',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(7,6,'SPONSOR_DRIVER_ADDED',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(8,6,'SPONSOR_DRIVER_REMOVED',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(9,6,'SPONSOR_NEW_APPLICATION',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(10,6,'ADMIN_NEW_APPLICATION',0,'2026-10-31 11:13:53','2026-11-17 18:39:48'),(11,6,'APPLICATION_ACCEPTED',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(12,6,'APPLICATION_REJECTED',0,'2026-10-31 11:13:53','2026-10-31 11:13:53'),(13,6,'ADMIN_APPLICATION_ACCEPTED',0,'2026-10-31 11:13:53','2026-11-17 18:39:48'),(14,36,'POINTS_GAINED',1,'2026-11-09 14:31:40','2026-11-09 14:31:40'),(15,36,'POINTS_LOST',0,'2026-11-09 14:31:40','2026-11-09 14:31:40'),(16,36,'DRIVER_SPONSOR_ADDED',1,'2026-11-09 14:31:40','2026-11-09 14:31:40'),(17,36,'DRIVER_SPONSOR_REMOVED',1,'2026-11-09 14:31:40','2026-11-09 14:31:40'),(18,36,'APPLICATION_ACCEPTED',1,'2026-11-09 14:31:40','2026-11-09 14:31:40'),(19,36,'APPLICATION_REJECTED',1,'2026-11-09 14:31:40','2026-11-09 14:31:40'),(23,6,'ADMIN_DRIVER_REMOVED',0,'2026-11-17 18:39:48','2026-11-17 18:39:48'),(24,6,'PROFILE_UPDATED',0,'2026-11-17 18:39:48','2026-11-17 18:39:48'),(25,6,'ADMIN_ORDER_PLACED',0,'2026-11-17 18:39:48','2026-11-17 18:39:48'),(26,6,'ADMIN_ORDER_CANCELED',0,'2026-11-17 18:39:48','2026-11-17 18:39:48'),(27,3,'POINTS_GAINED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(28,3,'POINTS_LOST',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(29,3,'DRIVER_SPONSOR_ADDED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(30,3,'DRIVER_SPONSOR_REMOVED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(31,3,'APPLICATION_ACCEPTED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(32,3,'APPLICATION_REJECTED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(33,3,'PROFILE_UPDATED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(34,3,'DRIVER_CART_ADDED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(35,3,'DRIVER_CART_REMOVED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(36,3,'DRIVER_ORDER_PLACED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04'),(37,3,'DRIVER_ORDER_CANCELED',1,'2026-11-17 20:27:02','2026-11-17 20:45:04');
/*!40000 ALTER TABLE `NOTIFICATIONSETTINGS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ORDERS`
--

DROP TABLE IF EXISTS `ORDERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ORDERS` (
  `ORDER_ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int DEFAULT NULL,
  `DRIVER_ID` int DEFAULT NULL,
  `ORDER_DTS` datetime DEFAULT NULL,
  `POINT_TOTAL` int DEFAULT NULL,
  `ORDER_STATUS` varchar(10) DEFAULT NULL,
  `SPONSORCOMP_ID` int DEFAULT NULL,
  PRIMARY KEY (`ORDER_ID`),
  KEY `ORDERS_USER_ID` (`USER_ID`),
  KEY `ORDERS_DRIVER_ID` (`DRIVER_ID`),
  CONSTRAINT `ORDERS_DRIVER_ID` FOREIGN KEY (`DRIVER_ID`) REFERENCES `DRIVER` (`DRIVER_ID`),
  CONSTRAINT `ORDERS_USER_ID` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ORDERS`
--

LOCK TABLES `ORDERS` WRITE;
/*!40000 ALTER TABLE `ORDERS` DISABLE KEYS */;
INSERT INTO `ORDERS` VALUES (2,NULL,NULL,'0000-00-00 00:00:00',1000,'Done',NULL),(3,NULL,NULL,'2026-09-14 13:15:00',1231,'Done',NULL),(4,NULL,NULL,'2025-05-22 01:10:22',572,'Cancelled',NULL),(5,1,1,'2026-09-22 14:34:10',1201,'Done',NULL),(6,1,1,'2026-10-26 13:56:50',10,'done',NULL),(7,13,7,'2026-11-09 01:10:01',80,'Done',1),(8,13,7,'2026-11-09 01:21:38',28,'Done',1),(9,36,19,'2026-11-09 14:27:02',100,'Done',2),(10,35,18,'2026-11-09 14:29:11',80,'Done',1),(11,1,1,'2026-11-10 16:25:48',392,'Done',1),(12,1,1,'2026-11-10 16:57:35',300,'Done',1),(13,1,1,'2026-11-10 18:16:23',30,'Cancelled',1),(14,1,1,'2026-11-10 18:18:00',56,'Done',1),(15,13,7,'2026-11-12 19:37:32',172,'Cancelled',1),(16,13,7,'2026-11-13 14:51:28',1125,'Done',1),(17,3,2,'2026-11-13 16:55:38',9,'Cancelled',1),(18,3,2,'2026-11-13 19:10:16',30,'Cancelled',1),(19,3,2,'2026-11-13 19:21:29',60,'Done',1),(20,13,7,'2026-11-15 17:01:21',30,'Cancelled',1),(21,13,7,'2026-11-15 17:03:26',30,'Cancelled',1),(22,13,7,'2026-11-15 21:37:20',1134,'Cancelled',1),(23,38,22,'2026-11-16 17:15:59',99,'Done',2);
/*!40000 ALTER TABLE `ORDERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PASSWORDCHANGES`
--

DROP TABLE IF EXISTS `PASSWORDCHANGES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PASSWORDCHANGES` (
  `PASSWORDCHANGE_ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `PASSWORDCHANGE_REASON` varchar(255) NOT NULL,
  `OLD_PASSWORD` varchar(255) NOT NULL,
  `NEW_PASSWORD` varchar(255) NOT NULL,
  `DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`PASSWORDCHANGE_ID`),
  KEY `USER_ID` (`USER_ID`),
  CONSTRAINT `PASSWORDCHANGES_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PASSWORDCHANGES`
--

LOCK TABLES `PASSWORDCHANGES` WRITE;
/*!40000 ALTER TABLE `PASSWORDCHANGES` DISABLE KEYS */;
INSERT INTO `PASSWORDCHANGES` VALUES (1,1,'User requested password change','old_hash','no_reason','2026-09-19 14:00:03'),(2,2,'User requested password change','password12345','HeartselinaKyle','2026-09-19 14:44:08'),(3,2,'User requested password change','HeartselinaKyle','ILoveFamily','2026-09-19 14:45:58'),(4,1,'User requested password change','noReason','scrypt:32768:8:1$a8WDfLzVzkmZlMPf$ed51397dce3b250a4d49de1b41c2f3131a71ddc6743b5427aa7fe59013077d763de5fe34269090128214e330b68ae8a756ff475e03dfe1923f09e84da10a8daa','2026-10-02 18:40:08'),(5,1,'User requested password change','scrypt:32768:8:1$a8WDfLzVzkmZlMPf$ed51397dce3b250a4d49de1b41c2f3131a71ddc6743b5427aa7fe59013077d763de5fe34269090128214e330b68ae8a756ff475e03dfe1923f09e84da10a8daa','scrypt:32768:8:1$VvOrtiynZA1QOj6l$05abf4f70b0fbf84a762aaa9255f09c3b3f5401e25436ff44003330c97c93e14d2cfc9050e89130a843e1e2c4f2830d26849d63b379410ee163fee3d77fd64f4','2026-10-02 18:41:35'),(6,1,'User requested password change','scrypt:32768:8:1$VvOrtiynZA1QOj6l$05abf4f70b0fbf84a762aaa9255f09c3b3f5401e25436ff44003330c97c93e14d2cfc9050e89130a843e1e2c4f2830d26849d63b379410ee163fee3d77fd64f4','scrypt:32768:8:1$V4HCSfGdMbe77FKr$c53139bf87c26983511f2ce8cbf3252389a96327c881f4e26e2934b00efed888420ae1a0cfcd9b5a1a8345b6a7488a41a9994ca42b16027ce0dfba495b35f552','2026-10-02 18:42:08'),(7,10,'User requested password change','scrypt:32768:8:1$WU8P4ZfbVQL8M7mM$61c30e1319b6d234737b8322d0f726b3962655048e3305b7211b935919c896910dd6231a6c0a233ee1f260bcf00c7fb76e9d966d32246ae26cc015e37a02aad7','scrypt:32768:8:1$qIwTitF6oZBzsOfU$eae348d078e37a34fedceeb6c7be04f83d7278246be253a93c594dfcf704a19db39a453d365a673b3822fd16bc02e2ce1c4f6f0178bc4959d18e88ecdc470515','2026-10-02 18:44:33'),(8,10,'User requested password change','scrypt:32768:8:1$qIwTitF6oZBzsOfU$eae348d078e37a34fedceeb6c7be04f83d7278246be253a93c594dfcf704a19db39a453d365a673b3822fd16bc02e2ce1c4f6f0178bc4959d18e88ecdc470515','scrypt:32768:8:1$23dUzXOkTzJZhaXf$6cb20e5b32c0bb383b04fbb51faa2d41f08fb8682bdc55f8ac418b3b8ea122c2ece42cc25a2b04da70af4102e8e9e9a177f6a98ca1362faaba9c49453261e4b7','2026-10-02 18:45:04'),(9,11,'User requested password change','scrypt:32768:8:1$HuLWBOh5z0hPIzph$b1428b1fac087ff7d2c1137949593bc114dfe78777d1dab41cac13b47a7e4f239aa4a7de4aa35210c4454014256d658d4afb2c095da9868e5ce89c31fa033193','scrypt:32768:8:1$UAzPzEhrE9VywHNy$d237af44d3d920c8776ea04cb2ec391b1d14cdbe6089382d1375251d14be5d7b32728c1fb86d5d384b475e85ec8845d3bb52ba43790561d5d18249776887f9b4','2026-10-02 18:54:43'),(10,10,'User requested password change','scrypt:32768:8:1$23dUzXOkTzJZhaXf$6cb20e5b32c0bb383b04fbb51faa2d41f08fb8682bdc55f8ac418b3b8ea122c2ece42cc25a2b04da70af4102e8e9e9a177f6a98ca1362faaba9c49453261e4b7','scrypt:32768:8:1$H9iA87gPtsXiOtDg$00da0f7379922f84c73209457454e8d88994371d1d303ecae57a6cbbf7b5b914400343f7a8e2344162ae663ec4137058d72a6b1ac01d25f33904175aaf1681ea','2026-10-08 18:07:30'),(11,10,'User requested password change','scrypt:32768:8:1$H9iA87gPtsXiOtDg$00da0f7379922f84c73209457454e8d88994371d1d303ecae57a6cbbf7b5b914400343f7a8e2344162ae663ec4137058d72a6b1ac01d25f33904175aaf1681ea','scrypt:32768:8:1$O81HJlJW7r3RJar8$20bbdbca762921d094db0b7699548ea0d3c2c4d60a7a12d99d9744dd69ca0c86891256c87c1d5acd9ef9bd0fe4cb26a268bfef82ad4600b42f89a51a488b6acf','2026-10-08 18:07:40'),(12,3,'User requested password change','supTechNerds','scrypt:32768:8:1$cO701GASyZ69FqpC$cbacf388ead859c8953cb1570385eb18df0ae388aa534e71f953ea772bfce56a0d2f78e460d0420e99b6f14056d6a7589a682344f54813931798817e71e007ea','2026-11-13 16:05:09'),(13,3,'User requested password change','scrypt:32768:8:1$cO701GASyZ69FqpC$cbacf388ead859c8953cb1570385eb18df0ae388aa534e71f953ea772bfce56a0d2f78e460d0420e99b6f14056d6a7589a682344f54813931798817e71e007ea','scrypt:32768:8:1$ipcUtWALu2MZ6OfA$67da602ee5321089d76a60766bc24ac26754bca1070b0c81bcaa998e7b44a8673bbccec1eeb485f6e8e359d66360db1694a0a02ea4f6d133a181dae29bdc4e1a','2026-11-13 16:45:47');
/*!40000 ALTER TABLE `PASSWORDCHANGES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `POINTCHANGES`
--

DROP TABLE IF EXISTS `POINTCHANGES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `POINTCHANGES` (
  `POINTCHANGE_ID` int NOT NULL AUTO_INCREMENT,
  `DRIVER_ID` int NOT NULL,
  `POINTCHANGE_AMOUNT` int NOT NULL,
  `POINTCHANGE_REASON` varchar(255) NOT NULL,
  `DTS` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `USER_ID` int NOT NULL,
  `BALANCE_ID` int DEFAULT NULL,
  PRIMARY KEY (`POINTCHANGE_ID`),
  KEY `DRIVER_ID` (`DRIVER_ID`),
  KEY `FK_POINTCHANGES_USER` (`USER_ID`),
  KEY `FK_POINTCHANGES_BALANCE` (`BALANCE_ID`),
  CONSTRAINT `FK_POINTCHANGES_BALANCE` FOREIGN KEY (`BALANCE_ID`) REFERENCES `BALANCE` (`BALANCE_ID`),
  CONSTRAINT `FK_POINTCHANGES_USER` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`),
  CONSTRAINT `POINTCHANGES_ibfk_1` FOREIGN KEY (`DRIVER_ID`) REFERENCES `DRIVER` (`DRIVER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `POINTCHANGES`
--

LOCK TABLES `POINTCHANGES` WRITE;
/*!40000 ALTER TABLE `POINTCHANGES` DISABLE KEYS */;
INSERT INTO `POINTCHANGES` VALUES (1,1,200,'test','2026-09-19 16:32:32',1,1),(2,1,-1201,'neg test','2026-09-19 17:46:08',1,1),(5,3,192,'test reason','2026-09-26 14:44:52',4,3),(6,2,-45,'guess','2026-09-26 14:44:52',3,2),(7,2,-872,'drunk driving','2026-09-26 14:44:52',3,2),(8,4,167,'Helpped my kid','2026-09-26 14:44:53',5,4),(10,6,10,'test','2026-10-14 22:10:35',2,6),(11,6,-10,'now subtract','2026-10-14 22:10:54',2,6),(13,1,-5,'test','2026-10-15 20:35:12',2,1),(14,2,-5,'test','2026-10-15 20:35:12',2,2),(15,3,-5,'test','2026-10-15 20:35:12',2,3),(16,4,-5,'test','2026-10-15 20:35:12',2,4),(17,6,-5,'test','2026-10-15 20:35:12',2,6),(18,7,-5,'test','2026-10-15 20:35:12',2,7),(20,1,5,'test','2026-10-15 21:00:53',2,1),(21,2,5,'test','2026-10-15 21:00:53',2,2),(22,3,5,'test','2026-10-15 21:00:53',2,3),(23,4,5,'test','2026-10-15 21:00:53',2,4),(24,6,5,'test','2026-10-15 21:00:53',2,6),(25,7,5,'test','2026-10-15 21:00:53',2,7),(26,4,9,'test','2026-10-18 17:40:50',2,4),(27,6,18,'test','2026-10-18 17:49:29',2,6),(28,6,-18,'test','2026-10-18 17:49:40',2,6),(29,6,18,'k','2026-10-18 17:51:38',2,6),(30,4,10,'test2','2026-10-20 09:19:12',9,4),(31,3,2,'ok','2026-10-27 16:13:12',2,3),(32,1,5,'because','2026-10-27 16:13:56',2,1),(33,2,5,'because','2026-10-27 16:13:56',2,2),(34,3,5,'because','2026-10-27 16:13:56',2,3),(35,4,5,'because','2026-10-27 16:13:56',2,4),(36,6,5,'because','2026-10-27 16:13:56',2,6),(37,7,5,'because','2026-10-27 16:13:56',2,7),(38,1,5,'Testing!','2026-10-28 23:26:53',9,NULL),(39,2,5,'Testing!','2026-10-28 23:26:53',9,NULL),(40,3,5,'Testing!','2026-10-28 23:26:53',9,NULL),(41,4,5,'Testing!','2026-10-28 23:26:53',9,NULL),(42,5,5,'Testing!','2026-10-28 23:26:53',9,NULL),(43,6,5,'Testing!','2026-10-28 23:26:53',9,NULL),(44,7,5,'Testing!','2026-10-28 23:26:53',9,NULL),(45,5,5,'Testing again','2026-10-28 23:27:06',9,NULL),(46,5,1,'Bulk add all companies - admin','2026-10-28 23:34:32',9,5),(47,1,2,'This is bulk add all','2026-10-28 23:35:22',9,1),(48,2,2,'This is bulk add all','2026-10-28 23:35:22',9,2),(49,3,2,'This is bulk add all','2026-10-28 23:35:22',9,3),(50,4,2,'This is bulk add all','2026-10-28 23:35:22',9,4),(51,5,2,'This is bulk add all','2026-10-28 23:35:22',9,5),(52,6,2,'This is bulk add all','2026-10-28 23:35:22',9,6),(53,7,2,'This is bulk add all','2026-10-28 23:35:22',9,7),(54,1,56,'bulk add as Luke Skywalker','2026-10-28 23:36:18',10,1),(55,2,56,'bulk add as Luke Skywalker','2026-10-28 23:36:18',10,2),(56,3,56,'bulk add as Luke Skywalker','2026-10-28 23:36:18',10,3),(57,4,56,'bulk add as Luke Skywalker','2026-10-28 23:36:18',10,4),(58,6,56,'bulk add as Luke Skywalker','2026-10-28 23:36:18',10,6),(59,7,56,'bulk add as Luke Skywalker','2026-10-28 23:36:18',10,7),(61,4,10,'please notifications!','2026-10-30 20:19:42',2,4),(62,1,10,'notification test','2026-10-30 20:24:20',2,1),(63,2,10,'notification test','2026-10-30 20:24:21',2,2),(64,3,10,'notification test','2026-10-30 20:24:21',2,3),(65,4,10,'notification test','2026-10-30 20:24:21',2,4),(66,6,10,'notification test','2026-10-30 20:24:22',2,6),(67,7,10,'notification test','2026-10-30 20:24:22',2,7),(68,4,1,'test','2026-10-30 21:28:01',6,4),(69,9,10,'For fun','2026-10-31 05:12:44',10,9),(70,9,-10,'No fun anymore','2026-10-31 05:12:55',10,9),(71,1,5,'Happy Halloween!','2026-10-31 05:16:46',9,1),(72,2,5,'Happy Halloween!','2026-10-31 05:16:46',9,2),(73,3,5,'Happy Halloween!','2026-10-31 05:16:46',9,3),(74,4,5,'Happy Halloween!','2026-10-31 05:16:46',9,4),(75,5,5,'Happy Halloween!','2026-10-31 05:16:46',9,5),(76,6,5,'Happy Halloween!','2026-10-31 05:16:46',9,6),(77,7,5,'Happy Halloween!','2026-10-31 05:16:46',9,7),(78,8,5,'Happy Halloween!','2026-10-31 05:16:46',9,8),(79,9,5,'Happy Halloween!','2026-10-31 05:16:46',9,9),(80,10,5,'Happy Halloween!','2026-10-31 05:16:46',9,10),(81,11,5,'Happy Halloween!','2026-10-31 05:16:46',9,11),(82,4,1,'notif preference test','2026-10-31 11:20:08',2,4),(87,7,-80,'Purchase (order #7)','2026-11-09 01:10:01',13,7),(88,7,3000,'Headpiece to the Staff of Ra','2026-11-09 01:13:49',2,7),(89,7,-28,'Purchase (order #8)','2026-11-09 01:21:38',13,7),(90,18,100,'Test','2026-11-09 14:17:51',2,18),(91,19,100,'test','2026-11-09 14:22:24',10,19),(92,19,-100,'Purchase (order #9)','2026-11-09 14:27:02',36,19),(93,18,-80,'Purchase (order #10)','2026-11-09 14:29:11',35,18),(94,20,2147483647,'Because shes great','2026-11-09 14:44:44',10,20),(95,1,-392,'Purchase (order #11)','2026-11-10 16:25:48',1,1),(96,1,-300,'Purchase (order #12)','2026-11-10 16:57:35',1,1),(97,1,-30,'Purchase (order #13)','2026-11-10 18:16:23',1,1),(98,1,30,'Refund for cancelled order #13','2026-11-10 18:16:48',1,1),(99,1,-56,'Purchase (order #14)','2026-11-10 18:18:00',1,1),(100,1,2341,'for being a good test sub','2026-11-10 19:21:01',2,1),(101,7,-172,'Purchase (order #15)','2026-11-12 19:37:32',13,7),(102,7,172,'Refund for cancelled order #15','2026-11-12 19:38:01',13,7),(103,7,-1125,'Purchase (order #16) placed by sponsor','2026-11-13 14:51:28',2,7),(104,7,17000,'Those guys must really be desperate','2026-11-13 14:53:23',2,7),(105,2,-9,'Purchase (order #17)','2026-11-13 16:55:38',3,2),(106,2,9,'Refund for cancelled order #17','2026-11-13 16:55:59',3,2),(107,2,-30,'Purchase (order #18)','2026-11-13 19:10:16',3,2),(108,2,30,'Refund for cancelled order #18','2026-11-13 19:10:43',3,2),(109,2,-60,'Purchase (order #19)','2026-11-13 19:21:29',3,2),(110,7,-30,'Purchase (order #20)','2026-11-15 17:01:21',13,7),(111,7,30,'Refund for cancelled order #20','2026-11-15 17:01:43',13,7),(112,7,-30,'Purchase (order #21)','2026-11-15 17:03:26',13,7),(113,7,30,'Refund for cancelled order #21','2026-11-15 17:03:50',13,7),(114,7,-1134,'Purchase (order #22)','2026-11-15 21:37:20',13,7),(115,7,1134,'Refund for cancelled order #22','2026-11-15 21:37:43',13,7),(116,22,200,'test','2026-11-16 15:46:49',2,22),(117,22,589,'poor boy get his point','2026-11-16 15:50:08',7,23),(118,22,-99,'Purchase (order #23)','2026-11-16 17:15:59',38,23),(119,1,5,'Automated Selenium test add 5 points 99e3055628ac4d4e9747eef6b3e9ef0a','2026-11-17 14:07:40',9,1),(120,1,-5,'Automated Selenium test subtract 5 points 99e3055628ac4d4e9747eef6b3e9ef0a','2026-11-17 14:07:42',9,1),(121,1,5,'test','2026-11-17 14:09:24',9,1),(122,1,-5,'test','2026-11-17 14:09:26',9,1),(123,1,5,'test','2026-11-17 15:00:09',9,1),(124,1,-5,'test','2026-11-17 15:00:11',9,1),(125,23,10,'Test','2026-11-17 15:02:53',9,24),(126,1,5,'test','2026-11-17 15:18:56',9,1),(127,1,-5,'test','2026-11-17 15:18:58',9,1);
/*!40000 ALTER TABLE `POINTCHANGES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SPONSOR`
--

DROP TABLE IF EXISTS `SPONSOR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SPONSOR` (
  `SPONSOR_ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `SPONSORCOMP_ID` int NOT NULL,
  PRIMARY KEY (`SPONSOR_ID`),
  KEY `USER_ID` (`USER_ID`),
  KEY `SPONSORCOMP_ID` (`SPONSORCOMP_ID`),
  CONSTRAINT `SPONSOR_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`USER_ID`),
  CONSTRAINT `SPONSOR_ibfk_2` FOREIGN KEY (`SPONSORCOMP_ID`) REFERENCES `SPONSORCOMP` (`SPONSORCOMP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SPONSOR`
--

LOCK TABLES `SPONSOR` WRITE;
/*!40000 ALTER TABLE `SPONSOR` DISABLE KEYS */;
INSERT INTO `SPONSOR` VALUES (1,2,1),(2,7,2),(3,10,2),(4,11,2);
/*!40000 ALTER TABLE `SPONSOR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SPONSORCOMP`
--

DROP TABLE IF EXISTS `SPONSORCOMP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SPONSORCOMP` (
  `SPONSORCOMP_ID` int NOT NULL AUTO_INCREMENT,
  `SPONSORCOMP_NAME` varchar(100) NOT NULL,
  `SPONSORCOMP_DOLLAR` double NOT NULL,
  `SPONSORCOMP_POINT` double NOT NULL,
  `CATALOG_MODE` varchar(10) NOT NULL DEFAULT 'query',
  PRIMARY KEY (`SPONSORCOMP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SPONSORCOMP`
--

LOCK TABLES `SPONSORCOMP` WRITE;
/*!40000 ALTER TABLE `SPONSORCOMP` DISABLE KEYS */;
INSERT INTO `SPONSORCOMP` VALUES (1,'The Comp',0.01,1,'selection'),(2,'LexCorps',1,100,'query');
/*!40000 ALTER TABLE `SPONSORCOMP` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SPONSORORDERS`
--

DROP TABLE IF EXISTS `SPONSORORDERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SPONSORORDERS` (
  `QUERY_ID` int NOT NULL AUTO_INCREMENT,
  `QUERY` varchar(100) NOT NULL,
  `SPONSORCOMP_ID` int NOT NULL,
  `USER_ID` int NOT NULL,
  `SPONSOR_ID` int NOT NULL,
  PRIMARY KEY (`QUERY_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SPONSORORDERS`
--

LOCK TABLES `SPONSORORDERS` WRITE;
/*!40000 ALTER TABLE `SPONSORORDERS` DISABLE KEYS */;
INSERT INTO `SPONSORORDERS` VALUES (1,'kenner star wars',1,10,3),(2,'playstation 5',1,10,3),(3,'lego millennium falcon',1,10,3),(5,'bryce young jersey',1,10,3),(6,'american flag',1,10,3),(7,'crucifix',1,10,3),(9,'rosary',1,10,3),(10,'holy hand grenade',1,10,3),(11,'brown scapular',1,10,3),(12,'bible',1,10,3),(13,'summa theologica',1,10,3),(14,'usa boxing approved headgear',1,10,3),(15,'headpiece to the staff of ra',1,10,3),(16,'ark of the covenant',1,10,3),(17,'fertility idol',1,10,3),(19,'sankara stones',1,10,3),(20,'urn of nurhachi',1,10,3),(21,'cross of coronado',1,10,3),(22,'candy',1,10,3),(23,'ark of the covenant',2,10,3),(24,'batcave',1,2,1),(25,'holy grail prop',1,2,1),(26,'ee3 prop',1,2,1),(27,'seismic charge prop',1,2,1),(28,'han solo in carbonite',1,2,1),(29,'baseball',2,10,3),(30,'tennis',1,2,1);
/*!40000 ALTER TABLE `SPONSORORDERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SPONSOR_APPROVED_ITEM`
--

DROP TABLE IF EXISTS `SPONSOR_APPROVED_ITEM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SPONSOR_APPROVED_ITEM` (
  `APPROVED_ID` int NOT NULL AUTO_INCREMENT,
  `SPONSORCOMP_ID` int NOT NULL,
  `ITEM_ID` varchar(100) NOT NULL,
  `USER_ID` int NOT NULL,
  `SPONSOR_ID` int NOT NULL,
  `ADDED_AT` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`APPROVED_ID`),
  UNIQUE KEY `uq_comp_item` (`SPONSORCOMP_ID`,`ITEM_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SPONSOR_APPROVED_ITEM`
--

LOCK TABLES `SPONSOR_APPROVED_ITEM` WRITE;
/*!40000 ALTER TABLE `SPONSOR_APPROVED_ITEM` DISABLE KEYS */;
INSERT INTO `SPONSOR_APPROVED_ITEM` VALUES (1,1,'v1|257833144943|0',2,1,'2026-11-15 21:22:45'),(2,1,'v1|304472532115|0',2,1,'2026-11-15 21:23:20'),(3,1,'v1|267838518029|0',2,1,'2026-11-15 21:24:06'),(4,1,'v1|287503101432|0',2,1,'2026-11-15 21:24:57'),(5,1,'v1|385742498821|0',2,1,'2026-11-15 21:25:22'),(6,1,'v1|128196520968|0',2,1,'2026-11-15 21:25:51'),(7,1,'v1|115846701921|0',2,1,'2026-11-15 21:26:29'),(8,1,'v1|256703210371|0',2,1,'2026-11-15 21:27:03'),(9,1,'v1|227375490976|0',2,1,'2026-11-15 21:27:58'),(10,1,'v1|206692553155|0',2,1,'2026-11-17 19:29:29');
/*!40000 ALTER TABLE `SPONSOR_APPROVED_ITEM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USER` (
  `USER_ID` int NOT NULL AUTO_INCREMENT,
  `USER_FNAME` varchar(50) NOT NULL,
  `USER_LNAME` varchar(50) NOT NULL,
  `ROLE` varchar(20) NOT NULL,
  `EMAIL` varchar(50) NOT NULL,
  `PASSWORD` varchar(255) NOT NULL,
  PRIMARY KEY (`USER_ID`),
  UNIQUE KEY `USERNAME` (`EMAIL`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES (1,'Annie','Smith','Driver','BipBop','scrypt:32768:8:1$V4HCSfGdMbe77FKr$c53139bf87c26983511f2ce8cbf3252389a96327c881f4e26e2934b00efed888420ae1a0cfcd9b5a1a8345b6a7488a41a9994ca42b16027ce0dfba495b35f552'),(2,'Bruce','Wayne','Sponsor','bwayne@gmail.com','ILoveFamily'),(3,'JohnnyB','Good','Driver','mail_name','scrypt:32768:8:1$ipcUtWALu2MZ6OfA$67da602ee5321089d76a60766bc24ac26754bca1070b0c81bcaa998e7b44a8673bbccec1eeb485f6e8e359d66360db1694a0a02ea4f6d133a181dae29bdc4e1a'),(4,'Josuke','Higashikata','Driver','theOnlyemail','Its1999'),(5,'Maria','Egg','Driver','something','dafljksd'),(6,'admin','adminson','Admin','admin@gmail.com','admin'),(7,'Lex','Luthor','Sponsor','lluthor@gmail.com','IHATESUPERMAN'),(8,'Felicity','Smoak','Driver','fsmoak@gmail.com','psw'),(9,'Anakin','Skywalker','Admin','chosenone@gmail.com','scrypt:32768:8:1$crKR2rnCfcGGX1Sk$5fda414fdcb9348757f3e8f6749c355c5e212cd8fd2440cb618ce8ff0b4492561e06ffbf0e48c818a4207028ab5f641c2fa3b5b5756649f95ecd248c2493c015'),(10,'Luke','Skywalker','Sponsor','lukeskywalker@gmail.com','scrypt:32768:8:1$O81HJlJW7r3RJar8$20bbdbca762921d094db0b7699548ea0d3c2c4d60a7a12d99d9744dd69ca0c86891256c87c1d5acd9ef9bd0fe4cb26a268bfef82ad4600b42f89a51a488b6acf'),(11,'Boba','Fett','Sponsor','bobafett@gmail.com','scrypt:32768:8:1$UAzPzEhrE9VywHNy$d237af44d3d920c8776ea04cb2ec391b1d14cdbe6089382d1375251d14be5d7b32728c1fb86d5d384b475e85ec8845d3bb52ba43790561d5d18249776887f9b4'),(12,'Han','Solo','Driver','hansolo@gmail.com','scrypt:32768:8:1$x1e1UOlFxjyOHKtP$7cd4762518ca50777eee08ce07dafbead402a9b26eecfedfec32e07ce6ebfc8b00958d36fc1461ca3ee828ca18808c1f24d2d8cac4394b3ab6d89a444de25cc0'),(13,'Henry','Jones','Driver','indianajones@gmail.com','scrypt:32768:8:1$EBcmbm4RzVCdZdMs$f88a4335d99e5b60ac3b0e3d77daca305a1cb624728fda2995ccecda6d17c88e80852def4bfeafc7100a95cedc7f4a9a13d73157069d90af574eb636530164b4'),(16,'Jango','Fett','Driver','originalfett@gmail.com','scrypt:32768:8:1$th3atHSewezcT3Mu$e342608b9f364f75b32d24a1188d2d2a7bcac15c7968d07961f3d75f031ed247bf7139220cd9729f0501929906b1a8ab223b79fddfb9774fcaff3f73607f3a2b'),(17,'Roger','Van Scoy','Driver','vanscoy@clemson.edu','scrypt:32768:8:1$LuQPvGAlpMt1LY1L$6a586be105eaa247c5ed6f9c6e343de791084c612d72cdfc57f8b14f2f485d32a87e0b34f8143a60d8954b6ebce3bfe2b366da9bdfcf2e56d08144680137b868'),(18,'Dick','Grayson','Driver','nightwing@gmail.com','scrypt:32768:8:1$8EhUrWPyYsrx3Nvv$4b9f1f464f91f1d57a3ee2c8f506b4e7a0d6f0921066a5daa3393f1aaf0bd15113870f93135dd669f87de893217a80206e5c60b9c9b8c4bfc46cf802adea2f3a'),(20,'Damian','Wayne','Driver','robin@gmail.com','scrypt:32768:8:1$dnqJGQElJI5jfiju$3ff56c412c04bf71aa5b15410c70858097c9b6421192654f93be5da9ef76f3cff793b6a0a111bc4527f19606e7e8979a5daa2efc1cb0da9a2fde8bd77c1a01b8'),(21,'Gro','Gu','Driver','babyoda@gmail.com','scrypt:32768:8:1$QUPcmogf3WU5Jz2c$a94269878ced7db4ea74e8351388b707865511214bd80051bdb0294aabf42077fd829900a34e2c7a6b2f1bc5c6b50643d34bb92be4c31b59c0f707f3c5b89f65'),(22,'Sponge','Bob','Driver','squarepants@gmail.com','scrypt:32768:8:1$UyxlpaYQMG8SyKZB$fddb0d0d74943bea8cb4a95ce18c8127099ffc0d3179bf7992927c17bab742fffcd552848c88dce40c9c2c423dcee4a0f9ee8e284935b60ea06e8ece7f48487c'),(23,'Mickey','Mouse','Driver','disney@yahoo.com','scrypt:32768:8:1$p2SQsVEvKJC8QQzB$396f93e5d91c8313c415695ddd0ec6290613daf22b0ea459e346d8ad5e7222e5f6be460536cc24f284c3f98f4475e9b3af086cf5a0658333f093ff9a0fdbaccb'),(24,'spider','man','Driver','spideysense@gmail.com','scrypt:32768:8:1$o1W1YhnokwtP9VMn$39ff0d4e2e9c65e232e971cc8246822fead0533a130a5ec805c7d073262711a1c1d91f840f21f2076f6c184205e59fc6d86296390d080457980f1a878aa9d1f8'),(25,'Clark','Kent','Driver','superman@gmail.com','scrypt:32768:8:1$idcFy1ITH4m2Nf6N$0c55000a0a26bad06e6c4c3da09ab81a0c7468d318ad83da6bba610565495f1c90b91c28395c01421320d48fcc31ac3333c83a17d28eb2ab528fbc19a34aedc3'),(26,'annoying','orange','Driver','sunnyd@gmail.com','scrypt:32768:8:1$Z9EVbywlcKA8pS0o$11b8f8df88ffa9f3e4018dda2de60afa13aa0e47cfdfcd944def9a255722cd64adbd48b04285430aa3380d1b83f9a387bae774a15105beb54d35c3104b3fc292'),(27,'eric','cartman','Driver','ecart@gmail.com','scrypt:32768:8:1$2OVfok73n5uKoYqO$dca4b1f31df7b586a86fe8c2e82d50976f26569e70f234fdee6abce5c5cf1744c08dede8d97e3a5112fd35b6f29b64e707a8a8f9f30299f1b386d39cd6f1a5ee'),(33,'Mike','Tiger','Driver','frostedflakes@gmail.com','scrypt:32768:8:1$P8kOsFQf9xp57Mdj$1637ad05cc8fdbd0142ce8a58eae9530502cc712de1702f4ad415c6542446ec6dd454409237d7932d40155d1d71676cd1fae5b98ba8b2d07db9142902b243b56'),(34,'hello','world','Driver','hw@gmail.com','scrypt:32768:8:1$p0Qgpuvgioep0aBi$9928127f25ff8b64c100070be790de22b3e76859484d3b2541b4ee74221efbece882c22176bff9fbf0d3a3b61ce4115cef765489da70e991ae753b6b2f0b44b0'),(35,'Jasonn','Zhengg','Driver','jasonzheng1244@gmail.com','scrypt:32768:8:1$qBbe93Nb9fwLEBbf$2af9547fc7774617c4f97581e6ca5fef2e5c4d59c2725b215899d508add2e8f9fbffd629511559ce9fdfbcbae4110a021ff8e241809032a14734cae19ee9a39c'),(36,'Jane','Smoth','Driver','test@example.com','scrypt:32768:8:1$M1RG1ynjVZfkUQgt$1364c92aba8e2a5bbd8e77ee4991ca9fab6f0e73e7381b7a72575b66c058273aa13169abf6daf8c53e0736f70440287f829faae1907f9afd1635587764373362'),(37,'Emma','Hall','Driver','kropemma3@gmail.com','scrypt:32768:8:1$mGxUXRVhEdpKdFNY$62425f7a0957081cdc61c1638f6c92e8ea084e47c08ea557a1f141295f9b99fe349a3c62c7eeb62513b402ec73a52c6744287eefb0a3b012f4d9fdd4bee5af64'),(38,'2_Job','James','Driver','2phones@gmail','scrypt:32768:8:1$w1QueyRgtQCX4F7X$921fe43e6a341c812685fc16b13fb8ef5a944e1eb463c136c55238aa11a7d514a6b32ca5fff014984c3c914e7ef30f75216da352328caa8607ef2247d2633967'),(39,'John','Driver','Driver','testdriver@example.com','scrypt:32768:8:1$8tfli5ERuP8kIQWO$14bc2c0837e4685e02bfcc2b40f37f90895bcf108e9085f095a0f328d33370dad5b538df11fc96ffc228ba2dc8e8254b47599cf3a6f911b9fbb475c24518f18f');
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'Team01_DB'
--
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
/*!50106 DROP EVENT IF EXISTS `complete_expired_orders` */;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'UTC' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`Team01`@`%`*/ /*!50106 EVENT `complete_expired_orders` ON SCHEDULE EVERY 1 MINUTE STARTS '2026-11-10 18:13:31' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE ORDERS
    SET ORDER_STATUS = 'Done'
    WHERE ORDER_STATUS = 'Active'
      AND ORDER_DTS <= NOW() - INTERVAL 5 MINUTE */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;

--
-- Dumping routines for database 'Team01_DB'
--
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `ADMIN_GET_DRIVERS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `ADMIN_GET_DRIVERS`()
BEGIN
    SELECT
        D.DRIVER_ID,
        U.USER_ID,
        U.USER_FNAME,
        U.USER_LNAME,
        U.EMAIL,

        COALESCE(
            GROUP_CONCAT(
                DISTINCT CONCAT(
                    SC.SPONSORCOMP_NAME,
                    ': ',
                    B.BALANCE,
                    ' points'
                )
                ORDER BY SC.SPONSORCOMP_NAME
                SEPARATOR '; '
            ),
            'None'
        ) AS SPONSOR_BALANCES,

        COALESCE(PC.POINTS_AWARDED, 0) AS POINTS_AWARDED,

        GROUP_CONCAT(
            DISTINCT B.SPONSORCOMP_ID
            SEPARATOR ','
        ) AS SPONSOR_IDS

    FROM DRIVER D

    INNER JOIN `USER` U
        ON D.USER_ID = U.USER_ID

    LEFT JOIN `BALANCE` B
        ON D.DRIVER_ID = B.DRIVER_ID

    LEFT JOIN SPONSORCOMP SC
        ON B.SPONSORCOMP_ID = SC.SPONSORCOMP_ID

    LEFT JOIN (
        SELECT
            USER_ID,
            SUM(
                CASE
                    WHEN POINTCHANGE_AMOUNT > 0
                    THEN POINTCHANGE_AMOUNT
                    ELSE 0
                END
            ) AS POINTS_AWARDED
        FROM POINTCHANGES
        GROUP BY USER_ID
    ) PC
        ON PC.USER_ID = U.USER_ID

    GROUP BY
        D.DRIVER_ID,
        U.USER_ID,
        U.USER_FNAME,
        U.USER_LNAME,
        U.EMAIL,
        PC.POINTS_AWARDED

    ORDER BY
        U.USER_LNAME,
        U.USER_FNAME;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `ADMIN_GET_SPONSORS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `ADMIN_GET_SPONSORS`()
BEGIN
    SELECT
        S.SPONSOR_ID,
        U.USER_ID,
        U.USER_FNAME,
        U.USER_LNAME,
        U.EMAIL,
        U.ROLE,
        SC.SPONSORCOMP_ID,
        SC.SPONSORCOMP_NAME,
        COALESCE(PC.POINTS_AWARDED, 0) AS POINTS_AWARDED

    FROM SPONSOR S

    INNER JOIN `USER` U
        ON S.USER_ID = U.USER_ID

    INNER JOIN SPONSORCOMP SC
        ON S.SPONSORCOMP_ID = SC.SPONSORCOMP_ID

    LEFT JOIN (
        SELECT
            USER_ID,
            SUM(
                CASE
                    WHEN POINTCHANGE_AMOUNT > 0
                    THEN POINTCHANGE_AMOUNT
                    ELSE 0
                END
            ) AS POINTS_AWARDED
        FROM POINTCHANGES
        GROUP BY USER_ID
    ) PC
        ON PC.USER_ID = U.USER_ID

    ORDER BY
        U.USER_LNAME,
        U.USER_FNAME;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_DRIVER_APPLICATIONS_AUDIT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `GET_DRIVER_APPLICATIONS_AUDIT`(
    IN p_sponsorcomp_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT
        A.SPONSORCOMP_ID,
        SC.SPONSORCOMP_NAME,
        U.EMAIL AS DRIVER_EMAIL,
        SU.EMAIL AS SPONSOR_EMAIL,
        A.STATUS,
        A.REASON,
        A.CREATED_DTS,
        A.UPDATED_DTS
    FROM APPLICATIONS AS A
    LEFT JOIN SPONSORCOMP AS SC
        ON A.SPONSORCOMP_ID = SC.SPONSORCOMP_ID
    LEFT JOIN `USER` AS U
        ON A.USER_ID = U.USER_ID
    LEFT JOIN SPONSOR AS S
        ON A.SPONSOR_ID = S.SPONSOR_ID
    LEFT JOIN `USER` AS SU
        ON S.USER_ID = SU.USER_ID
    WHERE
        (p_sponsorcomp_id IS NULL
            OR A.SPONSORCOMP_ID = p_sponsorcomp_id)
        AND
        (p_start_date IS NULL
            OR A.CREATED_DTS >= p_start_date)
        AND
        (p_end_date IS NULL
            OR A.CREATED_DTS < DATE_ADD(p_end_date, INTERVAL 1 DAY))
    ORDER BY A.CREATED_DTS DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_LOGIN_ATTEMPTS_AUDIT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `GET_LOGIN_ATTEMPTS_AUDIT`(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT
        ATTEMPTED_EMAIL,
        RESULT,
        DTS
    FROM LOGINATTEMPTS
    WHERE
        (p_start_date IS NULL
            OR DTS >= p_start_date)
        AND
        (p_end_date IS NULL
            OR DTS < DATE_ADD(p_end_date, INTERVAL 1 DAY))
    ORDER BY DTS DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_ORDER_DETAILED` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `GET_ORDER_DETAILED`(
    IN p_sponsorcomp_id INT,
    IN p_user_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_role VARCHAR(20)
)
BEGIN
    SELECT
        o.ORDER_ID,

        o.USER_ID AS ORDERED_BY_USER_ID,

        CONCAT_WS(' ',
            u.USER_FNAME,
            u.USER_LNAME
        ) AS ORDERED_BY_NAME,

        u.ROLE AS ORDERED_BY_ROLE,

        o.DRIVER_ID,

        CONCAT_WS(' ',
            driver_user.USER_FNAME,
            driver_user.USER_LNAME
        ) AS DRIVER_NAME,

        sc.SPONSORCOMP_ID,
        sc.SPONSORCOMP_NAME,

        o.ORDER_DTS,

        io.ITEMIZED_ID,
        io.ITEM_NAME,
        io.ITEM_AMOUNT,
        io.ITEM_PRICE,

        (io.ITEM_AMOUNT * io.ITEM_PRICE)
            AS LINE_TOTAL,

        CASE
            WHEN ROW_NUMBER() OVER (
                PARTITION BY o.ORDER_ID
                ORDER BY io.ITEMIZED_ID
            ) = 1
            THEN o.POINT_TOTAL
            ELSE NULL
        END AS POINTS_USED

    FROM ORDERS AS o

    -- User who placed the order
    JOIN `USER` AS u
        ON u.USER_ID = o.USER_ID

    -- Driver intended to receive the order
    LEFT JOIN DRIVER AS d
        ON d.DRIVER_ID = o.DRIVER_ID

    LEFT JOIN `USER` AS driver_user
        ON driver_user.USER_ID = d.USER_ID

    JOIN SPONSORCOMP AS sc
        ON sc.SPONSORCOMP_ID = o.SPONSORCOMP_ID

    JOIN ITEMIZEDORDER AS io
        ON io.ORDER_ID = o.ORDER_ID

    WHERE LOWER(o.ORDER_STATUS) = 'done'

        AND u.ROLE = p_role

        AND (
            p_sponsorcomp_id IS NULL
            OR o.SPONSORCOMP_ID = p_sponsorcomp_id
        )

        AND (
            p_user_id IS NULL
            OR o.USER_ID = p_user_id
        )

        AND (
            p_start_date IS NULL
            OR o.ORDER_DTS >= p_start_date
        )

        AND (
            p_end_date IS NULL
            OR o.ORDER_DTS <
                DATE_ADD(p_end_date, INTERVAL 1 DAY)
        )

    ORDER BY
        o.ORDER_DTS DESC,
        o.ORDER_ID DESC,
        io.ITEMIZED_ID;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_ORDER_SUMMARY` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `GET_ORDER_SUMMARY`(
    IN p_sponsorcomp_id INT,
    IN p_user_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_role VARCHAR(20)
)
BEGIN
    SELECT
        u.USER_ID AS ORDERED_BY_USER_ID,

        CONCAT_WS(' ',
            u.USER_FNAME,
            u.USER_LNAME
        ) AS ORDERED_BY_NAME,

        u.ROLE AS ORDERED_BY_ROLE,

        sc.SPONSORCOMP_ID,
        sc.SPONSORCOMP_NAME,

        COUNT(*) AS PURCHASE_COUNT,

        COALESCE(
            SUM(o.POINT_TOTAL), 0
        ) AS TOTAL_POINTS_USED,

        COALESCE(
            SUM(items.ORDER_SALES), 0
        ) AS TOTAL_SALES

    FROM ORDERS AS o

    JOIN `USER` AS u
        ON u.USER_ID = o.USER_ID

    JOIN SPONSORCOMP AS sc
        ON sc.SPONSORCOMP_ID = o.SPONSORCOMP_ID

    JOIN (
        SELECT
            ORDER_ID,
            SUM(
                ITEM_AMOUNT * ITEM_PRICE
            ) AS ORDER_SALES
        FROM ITEMIZEDORDER
        GROUP BY ORDER_ID
    ) AS items
        ON items.ORDER_ID = o.ORDER_ID

    WHERE LOWER(o.ORDER_STATUS) = 'done'

        AND u.ROLE = p_role

        AND (
            p_sponsorcomp_id IS NULL
            OR o.SPONSORCOMP_ID = p_sponsorcomp_id
        )

        AND (
            p_user_id IS NULL
            OR o.USER_ID = p_user_id
        )

        AND (
            p_start_date IS NULL
            OR o.ORDER_DTS >= p_start_date
        )

        AND (
            p_end_date IS NULL
            OR o.ORDER_DTS <
                DATE_ADD(p_end_date, INTERVAL 1 DAY)
        )

    GROUP BY
        u.USER_ID,
        u.USER_FNAME,
        u.USER_LNAME,
        u.ROLE,
        sc.SPONSORCOMP_ID,
        sc.SPONSORCOMP_NAME

    ORDER BY
        sc.SPONSORCOMP_NAME,
        ORDERED_BY_NAME;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_PASSWORD_CHANGES_AUDIT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `GET_PASSWORD_CHANGES_AUDIT`(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT
        U.EMAIL,
        PC.PASSWORDCHANGE_REASON AS REASON,
        PC.DTS
    FROM PASSWORDCHANGES AS PC
    JOIN `USER` AS U
        ON PC.USER_ID = U.USER_ID
    WHERE
        (p_start_date IS NULL
            OR PC.DTS >= p_start_date)
        AND
        (p_end_date IS NULL
            OR PC.DTS < DATE_ADD(p_end_date, INTERVAL 1 DAY))
    ORDER BY PC.DTS DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_POINT_CHANGES_AUDIT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `GET_POINT_CHANGES_AUDIT`(
    IN p_sponsorcomp_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_driver_id INT
)
BEGIN
    SELECT
        PC.DRIVER_ID,
        DU.EMAIL AS DRIVER_EMAIL,
        PC.USER_ID,
        CU.EMAIL AS CHANGED_BY_EMAIL,
        PC.POINTCHANGE_AMOUNT,
        PC.POINTCHANGE_REASON,
        PC.DTS,
        PC.BALANCE_ID,
        B.SPONSORCOMP_ID,
        SC.SPONSORCOMP_NAME
    FROM POINTCHANGES AS PC
    LEFT JOIN DRIVER AS D
        ON PC.DRIVER_ID = D.DRIVER_ID
    LEFT JOIN `USER` AS DU
        ON D.USER_ID = DU.USER_ID
    LEFT JOIN `USER` AS CU
        ON PC.USER_ID = CU.USER_ID
    LEFT JOIN BALANCE AS B
        ON PC.BALANCE_ID = B.BALANCE_ID
    LEFT JOIN SPONSORCOMP AS SC
        ON B.SPONSORCOMP_ID = SC.SPONSORCOMP_ID
    WHERE
        (
            p_sponsorcomp_id IS NULL
            OR B.SPONSORCOMP_ID = p_sponsorcomp_id
        )
        AND (
            p_start_date IS NULL
            OR PC.DTS >= p_start_date
        )
        AND (
            p_end_date IS NULL
            OR PC.DTS < DATE_ADD(p_end_date, INTERVAL 1 DAY)
        )
        AND (
            p_driver_id IS NULL 
            OR PC.DRIVER_ID = p_driver_id
        )
    ORDER BY PC.DTS DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `GET_REPORT_USERS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `GET_REPORT_USERS`()
BEGIN
    SELECT
        u.USER_ID,
        u.ROLE,

        CONCAT_WS(
            ' ',
            u.USER_FNAME,
            u.USER_LNAME
        ) AS USER_NAME,

        CASE
            WHEN u.ROLE = 'Driver' THEN (
                SELECT GROUP_CONCAT(
                    DISTINCT b.SPONSORCOMP_ID
                    ORDER BY b.SPONSORCOMP_ID
                )
                FROM DRIVER AS d
                JOIN BALANCE AS b
                    ON b.DRIVER_ID = d.DRIVER_ID
                WHERE d.USER_ID = u.USER_ID
            )

            WHEN u.ROLE = 'Sponsor' THEN (
                SELECT GROUP_CONCAT(
                    DISTINCT s.SPONSORCOMP_ID
                    ORDER BY s.SPONSORCOMP_ID
                )
                FROM SPONSOR AS s
                WHERE s.USER_ID = u.USER_ID
            )

        END AS SPONSOR_IDS

    FROM `USER` AS u

    WHERE u.ROLE IN ('Driver', 'Sponsor')

    ORDER BY
        u.ROLE,
        u.USER_FNAME,
        u.USER_LNAME;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.4.9.
--
/*!50003 DROP PROCEDURE IF EXISTS `RELATE_SPONSOR` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Team01`@`%` PROCEDURE `RELATE_SPONSOR`()
BEGIN
    INSERT INTO `Team01_DB`.`SPONSOR` (
        USER_ID,
        SPONSORCOMP_ID
    )
    SELECT
        u.USER_ID,
        CASE
            WHEN MOD(u.USER_ID, 2) = 0 THEN 1
            ELSE 2
        END AS SPONSORCOMP_ID
    FROM `Team01_DB`.`USER` AS u
    WHERE u.ROLE = 'Sponsor'
      AND NOT EXISTS (
          SELECT 1
          FROM `Team01_DB`.`SPONSOR` AS s
          WHERE s.USER_ID = u.USER_ID
      );
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-19 11:25:52
