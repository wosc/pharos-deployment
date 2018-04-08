<?php

$app['db.options'] = [
        'dbname' => 'agendav',
        'user' => 'agendav',
        'password' => '<%=node["agendav"]["db_pass"]%>',
        'host' => 'localhost',
        'driver' => 'pdo_mysql'
];

$app['caldav.baseurl'] = 'http://localhost:7076/cal/';
$app['caldav.publicurls'] = false;
// $app['caldav.baseurl.public'] = 'https://caldav.server.com';

$app['site.title'] = 'Calendar';
$app['csrf.secret'] = '<%=node["agendav"]["csrf_secret"]%>';
$app['proxies'] = ['127.0.0.1'];
$app['defaults.timezone'] = 'Europe/Berlin';
$app['defaults.show_week_nb'] = true;

$app['log.level'] = 'INFO';
