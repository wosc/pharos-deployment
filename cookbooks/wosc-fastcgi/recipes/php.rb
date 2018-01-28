package "php7.0"
package "php7.0-cgi"

service "php7.0-fpm" do
  action [:stop, :disable]
end

execute "send php errors to nginx log" do
  command "sed -i -e 's+;error_log = php_errors.log+error_log = /dev/stderr+' /etc/php/7.0/cgi/php.ini"
  not_if "grep 'error_log = /dev/stderr' /etc/php/7.0/cgi/php.ini"
end
