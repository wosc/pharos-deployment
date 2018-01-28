# Work around systemd-hostnamed not running due to unknown reasons.
ohai.disabled_plugins = [ :Hostnamectl ]
