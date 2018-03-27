user "grmusik" do
  comment "Gregor Renka"
  home "/home/grmusik"
  shell "/usr/lib/openssh/sftp-server"
end

include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/grmusik.de" do
  source "grmusik.de.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/grmusik.de" do
  to "/etc/nginx/sites-available/grmusik.de"
  notifies :reload, "service[nginx]", :delayed
end
