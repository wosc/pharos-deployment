package "nginx"
service "nginx" do
  supports :status => true, :restart => true, :reload => true
end

link "/etc/nginx/sites-enabled/default" do
  action :delete
  notifies :reload, "service[nginx]", :delayed
end

template "/etc/nginx/snippets/ssl.conf" do
  source "ssl.conf"
end
