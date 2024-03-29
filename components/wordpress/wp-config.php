<?php
/**
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, and ABSPATH. You can find more information by visiting
 * {@link https://codex.wordpress.org/Editing_wp-config.php Editing wp-config.php}
 * Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'grshop');

/** MySQL database username */
define('DB_USER', 'grshop');

/** MySQL database password */
define('DB_PASSWORD', '{{component.db_password}}');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '{{component.auth_key}}');
define('SECURE_AUTH_KEY',  '{{component.secure_auth_key}}');
define('LOGGED_IN_KEY',    '{{component.logged_in_key}}');
define('NONCE_KEY',        '{{component.nonce_key}}');
define('AUTH_SALT',        '{{component.auth_salt}}');
define('SECURE_AUTH_SALT', '{{component.secure_auth_salt}}');
define('LOGGED_IN_SALT',   '{{component.logged_in_salt}}');
define('NONCE_SALT',       '{{component.nonce_salt}}');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
        define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');


/** wosc: bypass strange FTP business */
define('FS_METHOD','direct');

/** wosc: https://codex.wordpress.org/Function_Reference/is_ssl#Notes */
$_SERVER['HTTPS'] = 'on';

/** wosc: we run wp-cron via the system cron, not on every page load */
define('DISABLE_WP_CRON', true);
