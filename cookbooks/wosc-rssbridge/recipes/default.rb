include_recipe "wosc-fastcgi::php"
package "php7.2-curl"
package "php7.2-json"
package "php7.2-mbstring"
package "php7.2-xml"


wosc_service_user "rssbridge"

VERSION = '2019-09-12'

directory "/srv/rssbridge/public" do
  owner "rssbridge"
end

ark "rssbridge" do
  url "https://github.com/RSS-Bridge/rss-bridge/archive/#{VERSION}.tar.gz"
  action :put
  path "/srv/rssbridge"
  name "public"
  owner "rssbridge"
  group "rssbridge"
end

file "/srv/rssbridge/public/whitelist.txt" do
  content "*"
end

template "/usr/local/src/rssbridge-ipv4.patch" do
  source "ipv4.patch"
end
execute "patch -p0 < /usr/local/src/rssbridge-ipv4.patch" do
  not_if "grep -q IPRESOLVE_V4 /srv/rssbridge/public/lib/contents.php"
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/rssbridge.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

include_recipe "wosc-fastcgi::nginx"
template "/srv/rssbridge/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
