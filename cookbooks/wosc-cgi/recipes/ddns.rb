python_runtime "ddns" do
  version "3.5"
  provider :system
end

python_virtualenv "/srv/cgiserv/ddns" do
  user "cgiserv"
  group "cgiserv"
  python "ddns"
  setuptools_version "38.4.1"
  pip_version "9.0.1"
  wheel_version "0.30.0"
end

template "/srv/cgiserv/ddns/requirements.txt" do
  source "ddns/requirements.txt"
end

pip_requirements "/srv/cgiserv/ddns/requirements.txt" do
  virtualenv "/srv/cgiserv/ddns"
  options "--no-deps"
end

template "/srv/cgiserv/ddns/config" do
  source "ddns/ddns.conf"
  owner "cgiserv"
  group "cgiserv"
  mode "0640"
end

template "/srv/cgiserv/apache.d/ddns.conf" do
  source "ddns/apache.conf"
  notifies :run, "execute[supervisorctl restart cgiserv]", :delayed
end

file "/srv/cgiserv/nginx.d/ddns.conf" do
  content "location /dns-update { proxy_pass http://cgi; }\n"
  notifies :reload, "service[nginx]", :delayed
end
