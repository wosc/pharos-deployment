include_recipe "wosc-fastcgi::php"
package "php7.0-curl"
package "php7.0-gd"
package "php7.0-gettext"


wosc_service_user "shaarli"

VERSION = '0.9.3'

directory "/srv/shaarli/public" do
  owner "shaarli"
end

ark "shaarli" do
  url ("https://github.com/shaarli/Shaarli/releases/download/" +
       "v#{VERSION}/shaarli-v#{VERSION}-full.zip")
  action :put
  path "/srv/shaarli"
  # ark insists on appending the name to the target path, sigh.
  name "public"
  owner "shaarli"
  group "shaarli"
end

ark "shaarli-material" do
  url "https://github.com/kalvn/Shaarli-Material/archive/v0.9.3.tar.gz"
  action :cherry_pick
  creates "Shaarli-Material-0.9.3/material"
  path "/srv/shaarli/public/tpl"
  owner "shaarli"
  group "shaarli"
end

# XXX Shaarli has no cli installer or usable config file, so you'll be prompted
# through the web to set a user/password. Then log in, go to "Tools / Configure
# your shaarli" and set theme to `material`.

include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/shaarli.conf" do
  source "supervisor.conf"
  # XXX Too agressive since it restarts *all* services
  # notifies :reload, "service[supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/bookmarks.wosc.de" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/bookmarks.wosc.de" do
  to "/etc/nginx/sites-available/bookmarks.wosc.de"
  notifies :reload, "service[nginx]", :delayed
end
