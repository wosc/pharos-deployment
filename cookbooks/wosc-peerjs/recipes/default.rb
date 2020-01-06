include_recipe "nodejs"

wosc_service_user "peerjs" do
  shell "/bin/bash"
end

VERSION = "31d7acd1bc9424fb22fd8ff6daadddeb2235f3cf"

ark "peerjs" do
  url "https://github.com/peers/peerjs-server/archive/#{VERSION}.zip"
  action :put
  path "/srv"
  owner "peerjs"
  group "peerjs"
end

template "/srv/peerjs/ws-3.0.patch" do
  source "ws-3.0.patch"
end
execute "patch -p0 < /srv/peerjs/ws-3.0.patch" do
  not_if "grep -q 'wosc patched' /srv/peerjs/lib/server.js"
end


template "/srv/peerjs/package-lock.json" do
  source "package-lock.json"
  owner "peerjs"
  group "peerjs"
  notifies :run, "execute[install_peerjs]", :delayed
end
execute "install_peerjs" do
  command "npm install"
  cwd "/srv/peerjs"
  user "peerjs"
  environment({"HOME" => "/srv/peerjs"})
  action :nothing
end

template "/srv/peerjs/serve.js" do
  source "serve.js"
  owner "peerjs"
  group "peerjs"
  notifies :run, "execute[supervisorctl restart peerjs]", :delayed
end
execute "supervisorctl restart peerjs" do
  action :nothing
end

include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/peerjs.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/peerjs/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
