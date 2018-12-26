python_runtime "ddns" do
  version "3.6"
  provider :system
end

python_virtualenv "/srv/cgiserv/ddns" do
  user "cgiserv"
  group "cgiserv"
  python "ddns"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
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

template "/srv/cgiserv/nginx.d/ddns.conf" do
  source "ddns/nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
