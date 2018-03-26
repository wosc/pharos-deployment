package "git"
package "libssl-dev"
ark "git-crypt" do
  url "https://www.agwa.name/projects/git-crypt/downloads/git-crypt-0.6.0.tar.gz"
  action :install_with_make
end

package "dailystrips"
template "/usr/local/src/dailystrips-altpattern.patch" do
  source "dailystrips-altpattern.patch"
end
execute "patch -p0 < /usr/local/src/dailystrips-altpattern.patch" do
  not_if "grep -q altpattern /usr/bin/dailystrips"
end
template "/home/wosc/bin/dailycomics.sh" do
  source "dailycomics.sh"
  mode "0755"
end
cron "dailystrips" do
  command "/home/wosc/bin/dailycomics.sh"
  minute "15"
  hour "5"
  user "wosc"
  mailto "wosc@wosc.de"
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
