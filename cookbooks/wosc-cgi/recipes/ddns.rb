python_runtime "ddns" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/srv/cgiserv/ddns" do
  user "cgiserv"
  group "cgiserv"
  python "ddns"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
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


# How to set up a Synology SRM Router to use this service as client:
# - Enable default "admin" account and set a password
# - Enable SSH service and allow in firewall
# - `ssh root@THEROUTER` using the password of the default "admin" user
# - Add this to the /etc.defaults/ddns_provider.conf file:
# [wosc.de]
#   modulepath=DynDNS
#   queryurl=https://pharos.wosc.de/dns-update?hostname=__HOSTNAME__&myip=__
