CREATE TABLE `domains` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `customer` varchar(255) default NULL,
  `responsible` varchar(255) default 'ii-tech',
  `price_plan` varchar(255) default 'special',
  `registry` varchar(255) default 'Providerdomain',
  `state` varchar(255) default 'OK',
  `since` date default '1970-01-01',
  `last_payment` date default '1970-01-01',
  `payment_until` date default '1970-01-01',
  `comments` text,
  `dkim_private_key` text,
  `is_mx` tinyint(1) NOT NULL default '1',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `mailboxes` (
  `id` int(11) NOT NULL auto_increment,
  `domain_id` int(11) NOT NULL,
  `local_part` varchar(50) NOT NULL,
  `dotted_address` varchar(255) default NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `forward` varchar(255) default NULL,
  `has_mailbox` tinyint(1) NOT NULL default '0',
  `has_vacation` tinyint(1) NOT NULL default '0',
  `has_spamfilter` tinyint(1) NOT NULL default '0',
  `vacation_subject` varchar(255) default NULL,
  `vacation_body` text,
  `action` varchar(255) NOT NULL,
  `mailbox_path` varchar(255) NOT NULL,
  `uid` int(11) NOT NULL default '{{component.exim_user["uid"]}}',
  `gid` int(11) NOT NULL default '{{component.exim_user["gid"]}}',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `schema_info` (
  `version` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `id` int(11) NOT NULL auto_increment,
  `login` varchar(40) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL default 'mail',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO schema_info (version) VALUES (4);
INSERT INTO users (login, password, role) VALUES ('root', '{{component.thyrida_root_password}}', 'root');
