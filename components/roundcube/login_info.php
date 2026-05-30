<?php

// Inspired by (defunct) https://github.com/marneu/login_info
class login_info extends rcube_plugin
{
    public $task = 'login';
    public $noajax = true;
    public $noframe = true;

    function init() {
        $this->add_hook('template_object_loginform', array($this, 'add_login_info'));
    }

    public function add_login_info($arg) {
        $password = '<div style="position: relative; top: 20vh;"><a href="/config/password">Change password</a></div>';

        $html = '<script type="text/javascript">';
        $html .= '$(document).ready(function() {
      $("#login-form").after(\''.$password.'\');});';
        $html .= '</script>';

        $rcmail = rcube::get_instance();
        $rcmail->output->add_footer($html);
        return $arg;
    }
}

?>
