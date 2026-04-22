-- Database Schema for One-Page Website Builder

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Default user: admin / admin123
INSERT INTO `users` (`username`, `password`) VALUES ('admin', '$2y$10$LGQEnYRf8BOPOEcXoKYtbuWlZ8q9gYdRAuRN6Wje2s0xDBRpupXgK');

-- ----------------------------
-- Table structure for settings
-- ----------------------------
CREATE TABLE IF NOT EXISTS `settings` (
  `key` varchar(50) NOT NULL,
  `value` longtext,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Default Settings
INSERT INTO `settings` (`key`, `value`) VALUES
('site_title', 'My Premium Website'),
('primary_color', '#0d6efd'),
('secondary_color', '#6c757d'),
('bg_color', '#ffffff'),
('text_color', '#212529'),
('font_family', 'Inter'),
('header_height', '80'),
('logo_url', ''),
('logo_width', '150'),
('sticky_header', '1'),
('formspree_url', ''),
('whatsapp_number', ''),
('whatsapp_message', 'Hello, I have an inquiry.'),
('custom_css', ''),
('analytics_code', ''),
('cookie_notice', '1'),
('footer_text', '© 2024 My Premium Website. All rights reserved.');

-- ----------------------------
-- Table structure for sections
-- ----------------------------
CREATE TABLE IF NOT EXISTS `sections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `type` varchar(50) NOT NULL,
  `content` longtext,
  `settings` longtext,
  `sort_order` int(11) DEFAULT '0',
  `is_visible` tinyint(1) DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Demo Content
INSERT INTO `sections` (`title`, `slug`, `type`, `content`, `settings`, `sort_order`, `is_visible`) VALUES
('Hero', 'hero', 'hero', '{"heading":"Elevate Your Brand","subheading":"Modern, fast, and professional websites built for your success.","button_text":"Get Started","button_link":"#contact","image":""}', '{"bg_type":"color","bg_color":"#f8f9fa","text_align":"center","padding_top":"100","padding_bottom":"100","overlay_opacity":"0"}', 1, 1),
('About Us', 'about', 'about', '{"heading":"Who We Are","text":"We are a team of passionate designers and developers dedicated to creating high-quality web experiences.","image":""}', '{"bg_type":"color","bg_color":"#ffffff","text_align":"left","padding_top":"80","padding_bottom":"80","overlay_opacity":"0"}', 2, 1);

SET FOREIGN_KEY_CHECKS = 1;
