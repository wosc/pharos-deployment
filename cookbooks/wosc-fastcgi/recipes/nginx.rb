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

file "/etc/nginx/conf.d/gzip.conf" do
  content "gzip_types text/plain text/css text/javascript text/xml application/json application/javascript application/xml application/xml+rss;"
  notifies :reload, "service[nginx]", :delayed
end
