python_runtime "gitnotify" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/usr/local/gitnotify" do
  python "gitnotify"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/usr/local/gitnotify/requirements.txt" do
  source "gitnotify-requirements.txt"
end

pip_requirements "/usr/local/gitnotify/requirements.txt" do
  virtualenv "/usr/local/gitnotify"
  options "--no-deps"
end

ark "git-notifier" do
  # Version 0.7-17
  url "https://github.com/rsmmr/git-notifier/archive/06f43481f01f5a4f8eb28a6a55ef4c3d22f4a576.zip"
  action :dump
  path "/usr/local/gitnotify"
end

link "/usr/local/bin/git-notifier" do
  to "/usr/local/gitnotify/git-notifier"
end
link "/usr/local/bin/github-notifier" do
  to "/usr/local/gitnotify/github-notifier"
end

template "/usr/local/src/gitnotify-error.patch" do
  source "gitnotify-error.patch"
end
execute "patch -p0 < /usr/local/src/gitnotify-error.patch" do
  not_if "grep -q 'wosc patched' /usr/local/bin/github-notifier"
end

template "/usr/local/src/gitnotify-py3.patch" do
  source "gitnotify-py3.patch"
end
execute "patch -p0 < /usr/local/src/gitnotify-py3.patch" do
  not_if "grep -q 'Error as e' /usr/local/bin/github-notifier"
end

template "/usr/local/src/gitnotify-subject.patch" do
  source "gitnotify-subject.patch"
end
execute "patch -p0 < /usr/local/src/gitnotify-subject.patch" do
  not_if "grep -q 'wosc patched' /usr/local/bin/git-notifier"
end


directory "/home/wosc/gitmail" do
  # Put github-notifier.cfg here manually.
  owner "wosc"
  group "wosc"
end
cron "gitnotify" do
  command "cd /home/wosc/gitmail; /usr/local/bin/github-notifier"
  hour "5"
  minute "0"
  user "wosc"
  mailto "wosc@wosc.de"
end


package "mercurial"

directory "/home/wosc/hgmail" do
  # Clone repositories to watch here, with `hg clone -U`
  owner "wosc"
  group "wosc"
end

template "/home/wosc/hgmail/hgrc" do
  source "hgrc"
  owner "wosc"
  group "wosc"
end
cron "hgnotify" do
  command "bash -c 'export HGRCPATH=/home/wosc/hgmail/hgrc; for i in /home/wosc/hgmail/*/; do hg --quiet --repository $i pull; done'"
  hour "5"
  minute "30"
  user "wosc"
  mailto "wosc@wosc.de"
end
