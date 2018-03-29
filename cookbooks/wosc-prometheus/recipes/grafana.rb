wosc_mysql_database "grafana"
wosc_mysql_user "grafana" do
  password node["prometheus"]["db_pass"]
end
wosc_mysql_grant "grafana" do
  user "grafana"
end


package "apt-transport-https"
apt_repository "grafana" do
  uri "https://packagecloud.io/grafana/stable/debian/"
  distribution "jessie"
  components ["main"]
  key "https://packagecloud.io/gpg.key"
end

package "grafana"
service "grafana-server"

template "/etc/grafana/grafana.ini" do
  source "grafana.ini"
  notifies :restart, "service[grafana-server]", :delayed
end

include_recipe "wosc-fastcgi::nginx"
template "/srv/prometheus/grafana-nginx.conf" do
  source "grafana-nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end

# Manually add Prometheus data source:
# http://localhost:9090/, proxy through grafana

