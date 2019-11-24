<?php
$config = array();

$config['db_dsnw'] = 'mysql://roundcube:<%=node["roundcube"]["db_pass"]%>@localhost/roundcube';

$config['default_host'] = 'localhost';
$config['default_port'] = 1143;
$config['smtp_server'] = 'localhost';
$config['smtp_port'] = 25;
$config['smtp_user'] = '';
$config['smtp_pass'] = '';

$config['product_name'] = 'Roundcube Webmail';
$config['support_url'] = '';

// this key is used to encrypt the users imap password which is stored
// in the session record (and the client cookie if remember password is enabled).
// please provide a string of exactly 24 chars.
$config['des_key'] = '<%=node["roundcube"]["store_pass_key"]%>';

// List of active plugins (in plugins/ directory)
$config['plugins'] = array(
    'archive',
    'zipdownload',
);

// skin name: folder from skins/
$config['skin'] = 'elastic';
