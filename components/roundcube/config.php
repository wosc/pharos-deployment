<?php
$config = array();

$config['db_dsnw'] = 'mysql://roundcube:{{component.db_password}}@localhost/roundcube';

$config['imap_host'] = 'localhost:1143';
$config['smtp_host'] = 'localhost:25';
$config['smtp_user'] = '';
$config['smtp_pass'] = '';

$config['product_name'] = 'Roundcube Webmail';
$config['support_url'] = '';

// this key is used to encrypt the users imap password which is stored
// in the session record (and the client cookie if remember password is enabled).
// please provide a string of exactly 24 chars.
$config['des_key'] = '{{component.store_pass_key}}';

// List of active plugins (in plugins/ directory)
$config['plugins'] = array(
    'archive',
    'login_info',
    'subscriptions_option',
    'zipdownload',
);

// skin name: folder from skins/
$config['skin'] = 'elastic';

$config['custom_login_info_localization'] = false;
$config['custom_login_info_after'] = '<div style="position: relative; top: 20vh;"><a href="/config/password">Change password</a></div>';
