VERSION = "1.2.0"

# group "adm" do  # to read accesslogs; already declared in wosc-prometheus::exim
#   action :manage
#   append true
#   members "prometheus"
# end

remote_file "/srv/prometheus/bin/nginx_exporter" do
  source "https://github.com/martin-helmich/prometheus-nginxlog-exporter/releases/download/v#{VERSION}/prometheus-nginxlog-exporter"
  mode "0755"
end

template "/srv/prometheus/nginx.yml" do
  source "nginx.yml"
  variables(:logs => ::Dir.glob('/var/log/nginx/*-access.log'))
  notifies :run, "execute[supervisorctl restart prometheus-nginx]", :delayed
end

template "/etc/supervisor/conf.d/prometheus-nginx.conf" do
  source "supervisor/nginx_exporter.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

execute "supervisorctl restart prometheus-nginx" do
  action :nothing
end
