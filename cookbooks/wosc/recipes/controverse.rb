directory "/home/controverse" do
  owner "wosc"
  group "wosc"
end

include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/controverse.wosc.de" do
  source "controverse.wosc.de.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/controverse.wosc.de" do
  to "/etc/nginx/sites-available/controverse.wosc.de"
  notifies :reload, "service[nginx]", :delayed
end


file "/etc/exim4/domains/controverse.wosc.de" do
  content 'mail: "|/usr/bin/mlmmj-recieve -L /var/spool/mlmmj/controverse/"'
end
