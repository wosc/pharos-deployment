include_recipe "wosc-fastcgi::php"
package "php7.0-mysql"

wosc_service_user "grshop" do
  shell "/bin/bash"
end

directory "/srv/grshop/tmp" do
  owner "grshop"
  group "grshop"
end

VERSION = '4.9.8'

if node["grmusik"]["install_wordpress"]
  ark "grshop" do
    url "https://wordpress.org/wordpress-#{VERSION}.tar.gz"
    action :put
    path "/srv/grshop"
    # ark insists on appending the name to the target path, sigh.
    name "lib"
    owner "grshop"
    group "grshop"
  end

  template "/srv/grshop/lib/wp-config.php" do
    source "wp-config.php"
    owner "grshop"
    group "grshop"
    mode "0640"
  end

  cookbook_file "/srv/grshop/lib/wp-content/plugins/wc-free-checkout-fields/wc-free-checkout-fields.php" do
    source "wc-free-checkout-fields.php"
    owner "grshop"
    group "grshop"
    mode "0640"
  end
end

wosc_mysql_database "grshop"
wosc_mysql_user "grshop" do
  password node["grmusik"]["db_pass"]
end
wosc_mysql_grant "grshop" do
  user "grshop"
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/grshop.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/grshop/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end


if node["grmusik"]["install_wordpress"]
  execute "wordpress_admin_user" do
    # https://peteris.rocks/blog/unattended-installation-of-wordpress-on-ubuntu-server/
    command "curl -s -k -H 'Host: grmusik.de' https://localhost/shop/wp-admin/install.php?step=2 -d weblog_title=GRShop -d user_name=root -d admin_email=gregor@grmusik.de -d admin_password=#{node['grmusik']['root_pass']} -d admin_password2=#{node['grmusik']['root_pass']} -d pw_weak=1"
    not_if "echo 'select user_login from wp_users' | mysql grshop | grep -q root"
  end
end
