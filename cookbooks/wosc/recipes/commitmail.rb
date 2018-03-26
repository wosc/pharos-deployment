python_runtime "gitnotify" do
  version "3.5"
  provider :system
end

python_virtualenv "/usr/local/gitnotify" do
  python "gitnotify"
  setuptools_version "38.4.1"
  pip_version "9.0.1"
  wheel_version "0.30.0"
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
