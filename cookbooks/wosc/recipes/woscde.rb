package "git"
package "libssl-dev"
ark "git-crypt" do
  url "https://www.agwa.name/projects/git-crypt/downloads/git-crypt-0.6.0.tar.gz"
  action :install_with_make
end

include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/wosc.de" do
  source "wosc.de.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/wosc.de" do
  to "/etc/nginx/sites-available/wosc.de"
  notifies :reload, "service[nginx]", :delayed
end
