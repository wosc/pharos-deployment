package "supervisor"
service "supervisor" do
  supports :status => true, :restart => true, :reload => true
  action :enable
end

link "/usr/local/bin/sv" do
  to "/usr/bin/supervisorctl"
end

file "/usr/lib/tmpfiles.d/supervisor.conf" do
  content "# Generated by wosc-fastcgi::supervisor\nd /var/run/supervisor 0755 root root"
end
