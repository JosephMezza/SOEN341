--
-- Table structure for table `image`
--
DROP TABLE IF EXISTS `image`;
CREATE TABLE `image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` mediumblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=latin1;

--
-- Table structure for table `user`
--
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

--
-- Table structure for table `post`
--
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `image_id` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `caption` varchar(200) NOT NULL,
  `likes` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `image_id` (`image_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`image_id`) REFERENCES `image` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8;

--
-- Table structure for table `user_like`
--
DROP TABLE IF EXISTS `user_like`;
CREATE TABLE `user_like` (
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `user_like_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_like_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `comment`
--
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `content` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;

--
-- Table structure for table `follower`
--
DROP TABLE IF EXISTS `follower`;
CREATE TABLE `follower` (
  `user_id` int(11) NOT NULL,
  `following_id` int(11) NOT NULL,
  KEY `user_id` (`user_id`),
  KEY `following_id` (`following_id`),
  CONSTRAINT `follower_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `follower_ibfk_2` FOREIGN KEY (`following_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Ablion73','JohnJStahl@superrito.com','John','Stahl','$2b$12$gmaTLM3z/ff102SSIarNeuxS/25GjyWbrzxhbmePQyiGtXNsc6e/6'),(2,'Winglersen1989','VernonAYoung@superrito.com','Vernon','Young','$2b$12$5d2XuRrV/QfAELEjVKw9V.4CnDx8X.iZvWFfjVQyFR5BrLFlKVxaC'),(3,'Thithe','GeneCRodriguez@dayrep.com','Gene','Rodriguez','$2b$12$TtGou.MWZbzVaZMZPFE74eXcmcEKlPQMYS5cvBgJyCiOj3F5ey.4S'),(4,'Wrove1935','WilliamCDupre@armyspy.com','William','Dupre','$2b$12$/jqqOMehxHU80PRmEjQhZ.Fv5poESoq8FG8XkM3Uozzn5n5UYEke.'),(5,'Kning1982','WalterVHerndon@cuvox.de','Walter','Herndon','$2b$12$8SlzVMswX6AsSUDgYSRZveEHhmumNwp0GPGcYMWAaWPQ5eP8ovmC2'),(6,'Whimseeplis','JodiCWorrell@fleckens.hu','Jodi','Worrell','$2b$12$4ENpGE7MXTaN/hhHQX04VOuoBkYi7xo7Egy3wrOYxyylsntWaE.SW'),(7,'Locies','SuzanneGMcClellan@fleckens.hu','Suzanne','McClellan','$2b$12$hwL6KWLazQrzzYSTrifAj.u9Krk7Gf7zn5iQyekEWmCmjS1Hq5fuK'),(8,'Somprood','BelindaBMatos@superrito.com','Belinda','Matos','$2b$12$ARuVwGTwfEXtYoeDbzUI.uvTmOiSjWskJGgVe0j2QS6ctxZxcQfaS'),(9,'Giarturner','KathyRMatthews@gustr.com','Kathy','Matthews','$2b$12$pHB7S4aOxVysWyCcIPF/mOqhoUqEo3Gk74KOK/wBr9JknxbkykmdC'),(10,'Drand1943','DaraRHawkins@armyspy.com','Dara','Hawkins','$2b$12$kknifIErjGRg6iQcPkVo5OaCNN08dcSvXhFWHmpPNjMHkGy4cSWL2'),(11,'Theyear','ShayNWurster@dayrep.com','Shay','Wurster','$2b$12$OcKDFKMbVdmhaIb1gBePiO82R98YSOfUntfmq1uE5tbCkR36ppGCG'),(12,'Witive','FloraCGriffin@rhyta.com','Flora','Griffin','$2b$12$14c/zC.bBwtKenXkKf/mGeI3R6G2GN4rtKj12AVJ6gngw6dCjyUJW'),(13,'Ristraid','BettyJDuarte@superrito.com','Betty','Duarte','$2b$12$ZrLpQehiHnq0LctEz6oEJ.QtqYTc5wyXcwLdaBpOGTe5fY1TEpWry'),(14,'Dideas85','ZeldaWStark@cuvox.de','Zelda','Stark','$2b$12$J9aTwtkdiDBNjkY1quYbXOwtC4zvzJ2qNhwu/uh61oxOwmSPT.hDS'),(15,'Milloon','LeroyDRios@rhyta.com','Leroy','Rios','$2b$12$fzN./w9CML0FVCLbh4OavuY.L29w0usTqswP8fY33CmrpAjKbt3.6'),(16,'Calasts53','RudolphSSmith@cuvox.de','Rudolph','Smith','$2b$12$k6UgJ0xvSb/5p/DgUxp.TeKDXwy.QRI8gxWELeFf4.REotdIg/xYC'),(17,'Usithed66','SeleneDLund@einrot.com','Selene','Lund','$2b$12$cAP9uu09yH6fnQhJkPMO6uVfRt4zBPKW0u5DsKsT7g0/HZTp490Z.'),(18,'Marknow','GeorgeNSchreiber@cuvox.de','George','Schreiber','$2b$12$eVCiGHetHeYcfLzoqFmuPelUaQbkXIX6rdqlJh8YvJGmFjcyWyhCK'),(19,'Feck1968','DylanSFrazier@fleckens.hu','Dylan','Frazier','$2b$12$eQlPLtlN3v1SFyBwlfMr8OpwdtpzPxY5EjAuEfphCoRgHEt5IVnyu'),(20,'Suchown','CarolTMadigan@cuvox.de','Carol','Madigan','$2b$12$Ao8QT9pZ2IWlyTOntVvKqOGbf6v/uP2jX6vwK/r4G6HmXNKT88Rva'),(21,'Thensted','MaryBWeiss@superrito.com','Mary','Weiss','$2b$12$B8hVZWk69yIHThHo3HElpeGaviiHYqswyEb2HWzIaU4dfHPkyN9Qa'),(22,'Crinsonast1984','VirginiaGBaker@gustr.com','Virginia','Baker','$2b$12$EPcCzD3enFFnN2tO5zltMeS6jL4wDoZbRoSha8pKYpH4m90zuNx.i'),(23,'Weaught','MariaAPace@dayrep.com','Maria','Pace','$2b$12$ic6Y7DcM2xE0z/laI6dTHuXwY5uRvuoOZxyrL6sFHwK0E38mB/6n2'),(24,'Weververnly','PatriciaWWhittaker@rhyta.com','Patricia','Whittaker','$2b$12$DOa7OB82PY5jKjgEy4xNKuuA39BVisq7CtVT9Ya7uagVuxqV3aoB.'),(25,'Trumsess1943','EdwardKKirkland@cuvox.de','Edward','Kirkland','$2b$12$Yzv9epl8kS5Q7pzvtVrwbOmJaQjtYH2tCRS7q.5/gK82gzbzW.L2a'),(26,'Bods1940','KathleenJTaylor@gustr.com','Kathleen','Taylor','$2b$12$DFWc3d.aRqPaMLFkCGgO.OzgQW23k4LlEkSWONhAF4dMhE5kvat9u'),(27,'Facepow','JohnGRose@rhyta.com','John','Rose','$2b$12$VYPCr47iCS1IIbMkmVl45ufR.Nyj3fC.n34iWdXM/DKwI15hZ3glG'),(28,'Gaveressake','MaryRMabry@rhyta.com','Mary','Mabry','$2b$12$8kZxOxMEBQxz5heWWgFK/edj5NVGAYbX4UYrRFNC1OazEy5B5CWPe'),(29,'Careekeres','RebeccaGBallweg@superrito.com','Rebecca','Ballweg','$2b$12$Qwv0FHY/smVkFFNGIWwSYep0slnoLglBGSYHrMhXoc33Yb4pXpgVe'),(30,'Togand','HaroldMFloyd@jourrapide.com','Harold','Floyd','$2b$12$bfXV53KkFiWwJ1lwbn2WnOEwDPYsFWwWjNOaW8zGY9WLiw.AKvdrG'),(31,'Hadet1965','EdwardARobinson@gustr.com','Edward','Robinson','$2b$12$LKcCVxdiSatYmLO3xVJtgOKug/CGRWGwQp9UElDrlQpCRE6tv65ZO'),(32,'Carther1949','ChadEHolmes@fleckens.hu','Chad','Holmes','$2b$12$ibRu03Y91XwfGKP3PUtJwu4dTOrdETAp0GrmPXU6AXHVDogRDjFwm'),(33,'Hiserus','EdwardCSisler@rhyta.com','Edward','Sisler','$2b$12$fh.Jdfmda5sC/OJLGMPhJ.fkW7CWhfaMcmE8W2O4lSmJObAiBxKBa'),(34,'Swentorme1935','SaraFNusbaum@teleworm.us','Sara','Nusbaum','$2b$12$kup47hA7zExRsAZzkkdh9.kQzGm9Zl/q44dwzd4hSjOc7oBZZCM3G'),(35,'Cathery','ThelmaBColes@teleworm.us','Thelma','Coles','$2b$12$quBp2YtoK4w4.UU0pXt84OkJikrU4eeg14UeKCwtwztyfKPYC4mWC'),(36,'Sups1944','ViolaDAkins@gustr.com','Viola','Akins','$2b$12$d01.Yo1eBu8RAoHm6ljm8.xb05IPKeJdj8Ldq5DdKm8ICBzXoSIdK'),(37,'Wilegire1937','ChristopherSDavidson@teleworm.us','Christopher','Davidson','$2b$12$TW2OHiG9JhTgyJzeqiil5eg.OLRi3K1OSVdM.IUMCZo9WX7bOmoiS'),(38,'Thetting','BettyGHawkins@cuvox.de','Betty','Hawkins','$2b$12$W/ugqKzrQeaKuAt09q46Hu0W9zqJ8lCel9HJrXHgS5Ztv3zIQDdk6'),(39,'Hurs1997','BonnieHBeaulieu@superrito.com','Bonnie','Beaulieu','$2b$12$ndy1LZri923wAqMy1DwBNOymsu8givXPE/z9nK5ObKckuSRkTxRPG'),(40,'Goiderearsur','MarthaMSchultz@jourrapide.com','Martha','Schultz','$2b$12$2wBjdfFx4Cy/tzkOOPRZrecXdzXVcJaCpbmfjCud4bAYwgUH9PDSS'),(41,'Thdow1971','StacyCRichards@gustr.com','Stacy','Richards','$2b$12$PiBHh6ya5bK7sDEQxQD.gO47eSYjfoizVl/qXoFrye.HYq7iJdpwq'),(42,'Horgy1990','TheresaCHargrave@teleworm.us','Theresa','Hargrave','$2b$12$/hzO1OemmyNxM7khQePwV.o.mh.Fbuc39GtGqoPNlrVcITmMGp6cS'),(43,'Sequith','JamesJHoughton@jourrapide.com','James','Houghton','$2b$12$mYWssOb66X0.zxZ59gFDZeyg.krK8aAJJWvFTlwhKZ0g4uyZLMeki'),(44,'Myseat','SusanRSanders@einrot.com','Susan','Sanders','$2b$12$AXEy4lHl6t5NUfpAluxbwu3KtxJmDq45tgzCjN2.C1i7z6cBhxoAe'),(45,'Slogummid','DianeDGiles@dayrep.com','Diane','Giles','$2b$12$gERA2XMLb10etqtyV.5p1.cmWHvgQAKTCbX409Ev4uRFsyYJ.UqYO'),(46,'Sone1983','RoyKWilson@fleckens.hu','Roy','Wilson','$2b$12$FofdgJ1EYNOU3KWzmwea6ugAlSiFIHeY6ro3rwzrjN9WNlljFD47u'),(47,'Whatithas','DonellaJPratt@jourrapide.com','Donella','Pratt','$2b$12$s6/XK1RC5pfI6b0LTH1X7.uAtAjUVJN0TDF8/oPD9q/e.h2Mzgjea'),(48,'Arman1992','GabrielleCRichardson@superrito.com','Gabrielle','Richardson','$2b$12$/X725Ep5ue9r/XnY1dWrge/fF9qo7DXI8y4evGBUBpfbG32Bj7LGm'),(49,'alexabarra','alexandrubara2000@gmail.com','ALEXANDRU','BARA','$2b$12$5UGIM9FvfKYjZxMgHJFM4OwxHx2YAKSfUcoXeUA9Q/04m3Vo9oG8K'),(50,'Jonathan','jonathanjong@gmail.com','Jonathan','Jong','$2b$12$5HYgg//BHsWSKSLSFFb6RuQ4gFtLC05yBpMd.SPh5QKo1LxE6rZPy'),(53,'MatteoGisondi','matteo.gisondi@gmail.com','Matteo','Gisondi','$2b$12$MYuUD1VHWzMVn6x6JJt/y.Qugt9NLVqwXX17MFiZoRsVFLS2s.c5q'),(54,'Prempeh','david.kor@prempeh.com','David','Koranteng','$2b$12$uc52i37x0IFcDmeG15r.CeSe3hm/J5VFxV.TLfdUM6XiP2DXscYgi'),(55,'kylejen','kylejen@gmail.com','kyle','jen','$2b$12$viMCnZb0w.Fj1o0gvh5d5..gwGxd6e7f.y00BePYyDoBeK1jvF5Cy'),(56,'CItester','tester@gmail.com','tester','bester','$2b$12$lPwKATkwnDE1JEWg2gpZfOVefY7cSAyhRiYqjk7iG2.P51fyN1Ac2');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `follower` WRITE;
/*!40000 ALTER TABLE `follower` DISABLE KEYS */;
INSERT INTO `follower` VALUES (1,19),(1,44),(1,16),(1,48),(1,12),(1,20),(1,7),(1,12),(1,31),(1,49),(2,20),(2,17),(2,35),(2,5),(2,41),(2,16),(2,27),(2,25),(2,27),(2,18),(3,48),(3,15),(3,34),(3,6),(3,42),(3,23),(3,42),(3,43),(3,7),(3,32),(4,46),(4,26),(4,43),(4,24),(4,47),(4,29),(4,20),(4,47),(4,22),(4,38),(5,19),(5,13),(5,2),(5,16),(5,14),(5,16),(5,47),(5,40),(5,12),(5,40),(6,31),(6,24),(6,26),(6,29),(6,22),(6,29),(6,6),(6,25),(6,38),(6,34),(7,1),(7,16),(7,20),(7,5),(7,40),(7,23),(7,20),(7,24),(7,37),(7,8),(8,1),(8,5),(8,44),(8,46),(8,2),(8,27),(8,24),(8,6),(8,15),(8,33),(9,10),(9,10),(9,5),(9,1),(9,17),(9,38),(9,44),(9,23),(9,10),(9,11),(10,38),(10,13),(10,11),(10,45),(10,49),(10,26),(10,49),(10,19),(10,31),(10,15),(11,19),(11,32),(11,35),(11,22),(11,42),(11,39),(11,36),(11,3),(11,33),(11,34),(12,20),(12,20),(12,37),(12,23),(12,12),(12,13),(12,38),(12,14),(12,22),(12,4),(13,23),(13,8),(13,4),(13,20),(13,29),(13,21),(13,38),(13,6),(13,38),(13,17),(14,31),(14,24),(14,26),(14,4),(14,2),(14,34),(14,4),(14,24),(14,44),(14,46),(15,14),(15,44),(15,35),(15,21),(15,31),(15,1),(15,8),(15,47),(15,37),(15,22),(16,34),(16,24),(16,31),(16,39),(16,13),(16,39),(16,38),(16,24),(16,7),(16,17),(17,48),(17,33),(17,33),(17,27),(17,47),(17,35),(17,8),(17,17),(17,36),(17,26),(18,32),(18,25),(18,3),(18,49),(18,45),(18,13),(18,15),(18,22),(18,22),(18,49),(19,35),(19,37),(19,18),(19,27),(19,36),(19,6),(19,9),(19,7),(19,10),(19,46),(20,48),(20,8),(20,10),(20,21),(20,21),(20,27),(20,41),(20,35),(20,37),(20,36),(21,42),(21,10),(21,7),(21,15),(21,15),(21,35),(21,47),(21,23),(21,36),(21,7),(22,22),(22,41),(22,13),(22,32),(22,18),(22,42),(22,49),(22,22),(22,31),(22,32),(23,48),(23,15),(23,44),(23,30),(23,28),(23,34),(23,21),(23,39),(23,2),(23,38),(24,5),(24,22),(24,21),(24,2),(24,47),(24,26),(24,31),(24,30),(24,5),(24,12),(25,36),(25,23),(25,39),(25,43),(25,21),(25,24),(25,22),(25,4),(25,33),(25,42),(26,31),(26,8),(26,40),(26,37),(26,2),(26,2),(26,40),(26,35),(26,8),(26,43),(27,10),(27,47),(27,47),(27,3),(27,30),(27,29),(27,24),(27,41),(27,41),(27,9),(28,22),(28,18),(28,40),(28,43),(28,26),(28,34),(28,47),(28,46),(28,5),(28,29),(29,15),(29,41),(29,21),(29,14),(29,23),(29,6),(29,7),(29,26),(29,23),(29,13),(30,8),(30,23),(30,29),(30,41),(30,24),(30,17),(30,22),(30,33),(30,21),(30,35),(31,2),(31,3),(31,4),(31,10),(31,35),(31,26),(31,4),(31,3),(31,45),(31,28),(32,23),(32,19),(32,6),(32,1),(32,22),(32,15),(32,36),(32,12),(32,49),(32,20),(33,32),(33,27),(33,32),(33,21),(33,43),(33,2),(33,3),(33,46),(33,35),(33,17),(34,43),(34,46),(34,48),(34,35),(34,2),(34,9),(34,17),(34,14),(34,45),(34,36),(35,46),(35,17),(35,36),(35,43),(35,14),(35,9),(35,11),(35,24),(35,3),(35,16),(36,32),(36,3),(36,7),(36,24),(36,30),(36,5),(36,44),(36,30),(36,33),(36,6),(37,14),(37,48),(37,42),(37,17),(37,13),(37,20),(37,47),(37,8),(37,47),(37,35),(38,1),(38,45),(38,13),(38,30),(38,33),(38,2),(38,11),(38,8),(38,30),(38,46),(39,25),(39,28),(39,21),(39,16),(39,36),(39,34),(39,8),(39,16),(39,12),(39,34),(40,18),(40,20),(40,15),(40,13),(40,48),(40,17),(40,35),(40,22),(40,37),(40,21),(41,8),(41,31),(41,31),(41,30),(41,2),(41,47),(41,4),(41,39),(41,4),(41,38),(42,12),(42,20),(42,1),(42,22),(42,16),(42,41),(42,2),(42,20),(42,36),(42,1),(43,19),(43,41),(43,31),(43,21),(43,39),(43,35),(43,18),(43,9),(43,20),(43,9),(44,28),(44,43),(44,29),(44,34),(44,9),(44,35),(44,31),(44,5),(44,20),(45,30),(45,3),(45,41),(45,24),(45,29),(45,46),(45,25),(45,5),(45,1),(45,31),(46,3),(46,31),(46,11),(46,33),(46,44),(46,32),(46,47),(46,44),(46,18),(46,48),(47,30),(47,18),(47,30),(47,8),(47,8),(47,29),(47,11),(47,20),(47,29),(47,24),(48,35),(48,31),(48,4),(48,41),(48,38),(48,5),(48,23),(48,10),(48,27),(48,39),(49,15),(49,48),(49,12),(49,31),(49,38),(49,18),(50,49),(50,1),(53,4),(53,5),(53,17),(53,3),(53,2),(53,1),(16,1),(54,53),(54,3),(55,26),(55,29),(55,27),(55,32),(55,14),(55,7),(55,28),(49,4),(56,49),(56,16),(56,55),(56,50),(56,53),(49,53),(49,44),(49,43);
/*!40000 ALTER TABLE `follower` ENABLE KEYS */;
UNLOCK TABLES;