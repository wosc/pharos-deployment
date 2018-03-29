wosc_service_user "prometheus" do
  shell "/bin/bash"
end

[
  "bin",
  "data",
  "node",
].each do |dir|
    directory "/srv/prometheus/#{dir}" do
      owner "prometheus"
      group "prometheus"
    end
end

ark "prometheus" do
  url "https://github.com/prometheus/prometheus/releases/download/v2.2.1/prometheus-2.2.1.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*/prometheus'"
  path "/srv/prometheus/bin"
end
ark "node_exporter" do
  url "https://github.com/prometheus/node_exporter/releases/download/v0.15.2/node_exporter-0.15.2.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*node_exporter'"
  path "/srv/prometheus/bin"
end
ark "pushgateway" do
  url "https://github.com/prometheus/pushgateway/releases/download/v0.4.0/pushgateway-0.4.0.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*/pushgateway'"
  path "/srv/prometheus/bin"
end

template "/srv/prometheus/server.yml" do
  source "server.yml"
  owner "prometheus"
  group "prometheus"
  notifies :run, "execute[supervisorctl restart prometheus]", :delayed
end

include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/prometheus.conf" do
  source "supervisor/prometheus.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end
template "/etc/supervisor/conf.d/prometheus-node.conf" do
  source "supervisor/node_exporter.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end
# template "/etc/supervisor/conf.d/prometheus-push.conf" do
#   source "supervisor/pushgateway.conf"
#   notifies :run, "execute[reload_supervisor]", :delayed
# end

execute "supervisorctl restart prometheus" do
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/prometheus/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
