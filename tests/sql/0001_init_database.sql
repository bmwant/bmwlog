-- drop tables
SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `role`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `photo`;
DROP TABLE IF EXISTS `post`;
DROP TABLE IF EXISTS `quote`;
DROP TABLE IF EXISTS `session`;
DROP TABLE IF EXISTS `site_joke`;
DROP TABLE IF EXISTS `static_page`;
DROP TABLE IF EXISTS `tag`;
DROP TABLE IF EXISTS `stream_message`;
DROP TABLE IF EXISTS `tag_to_post`;
DROP TABLE IF EXISTS `banner`;
SET foreign_key_checks = 1;

-- create tables
CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(100) NOT NULL,
  `level` int(11) NOT NULL DEFAULT '40',
  PRIMARY KEY (`role_id`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `mail` varchar(100) NOT NULL,
  `nickname` varchar(100) NOT NULL,
  `user_password` varchar(500) NOT NULL,
  `picture` varchar(500) DEFAULT NULL,
  `role_id` int(11) NOT NULL,
  `date_registered` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `mail` (`mail`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`category_id`),
  KEY `category_id` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `photo` (
  `photo_id` int(11) NOT NULL AUTO_INCREMENT,
  `photo` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `desc` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `date_added` datetime NOT NULL,
  PRIMARY KEY (`photo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11),
  `post_text` varchar(10000) NOT NULL,
  `title` varchar(1000) NOT NULL,
  `user_id` int(11),
  `date_posted` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  `likes` int(11) NOT NULL DEFAULT '0',
  `views` int(11) NOT NULL DEFAULT '0',
  `draft` tinyint(1) NOT NULL DEFAULT '1',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `language` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `show_on_index` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`post_id`),
  KEY `post_id` (`post_id`),
  KEY `category_id` (`category_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`category_id`)
  REFERENCES `category` (`category_id`) ON DELETE SET NULL,
  CONSTRAINT `post_ibfk_3` FOREIGN KEY (`user_id`)
  REFERENCES `user` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `quote` (
  `quote_id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(1000) NOT NULL,
  `author` varchar(500) NOT NULL,
  PRIMARY KEY (`quote_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `session` (
  `session_id` int(11) NOT NULL AUTO_INCREMENT,
  `mail` varchar(255) NOT NULL,
  `expires` int(11) NOT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `login_date` datetime NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `site_joke` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `static_page` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `date` datetime NOT NULL,
  `title` varchar(255) NOT NULL,
  `text` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `static_page_url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `stream_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `message` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `tag` (
  `tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(20) NOT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `text` (`text`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `tag_to_post` (
  `tag_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `tag_id` (`tag_id`,`post_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `tag_to_post_ibfk_3` FOREIGN KEY (`post_id`)
  REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tag_to_post_ibfk_4` FOREIGN KEY (`tag_id`)
  REFERENCES `tag` (`tag_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `banner` (
  `banner_id` int(11) NOT NULL AUTO_INCREMENT,
  `desc` varchar(200) NOT NULL,
  `link` varchar(200) NOT NULL,
  `img` varchar(500) NOT NULL,
  `disabled` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`banner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
