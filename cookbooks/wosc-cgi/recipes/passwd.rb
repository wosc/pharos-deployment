python_runtime "passwd" do
  version "3.6"
  provider :system
end

python_virtualenv "/srv/cgiserv/passwd" do
  user "cgiserv"
  group "cgiserv"
  python "passwd"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/cgiserv/passwd/requirements.txt" do
  source "passwd/requirements.txt"
end

pip_requirements "/srv/cgiserv/passwd/requirements.txt" do
  virtualenv "/srv/cgiserv/passwd"
  options "--no-deps"
end


file "/etc/sudoers.d/webpasswd" do
  content "cgiserv ALL=(root) NOPASSWD: /srv/cgiserv/passwd/bin/webpasswd-change\n"
end


file "/srv/cgiserv/apache.d/passwd.conf" do
  content "ScriptAlias /passwd /srv/cgiserv/passwd/bin/webpasswd-cgi\n"
  notifies :run, "execute[supervisorctl restart cgiserv]", :delayed
end
file "/srv/cgiserv/nginx.d/passwd.conf" do
  content "location /passwd { proxy_pass http://cgi; }\n"
  notifies :reload, "service[nginx]", :delayed
end
