VERSION = '1.0.0'

wosc_service_user "robometeor" do
  shell "/bin/bash"
end

package "mongodb"

# meteor build dist
# scp dist/robometeor.tar.gz wosc.de:/srv/robometeor
# tar xf /srv/robometeor/robometeor.tar.gz
# cd programs/server && npm install

# replace in programs/web.browser/12345.js:
# `Router.route("/` with `Router.router("/roborally/`
# prefix with `/roborally`:
# `/robots/`, `/tiles/`, `/finish.png`, `/start.png`, `/damage-token.png`, `/Power_Off.png`


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/robometeor.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

execute "supervisorctl restart robometeor" do
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/robometeor/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
