ark "mysqld_exporter" do
  url "https://github.com/prometheus/mysqld_exporter/releases/download/v0.10.0/mysqld_exporter-0.10.0.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*/mysqld_exporter'"
  path "/srv/prometheus/bin"
end

wosc_mysql_user "prometheus" do
  password node["prometheus"]["db_pass"]
end
execute "prometheus_grant" do
  command "echo \"GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'prometheus'@'localhost';\" | mysql -Bs -uroot mysql"
end

template "/etc/supervisor/conf.d/prometheus-mysql.conf" do
  source "supervisor/mysqld_exporter.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end
