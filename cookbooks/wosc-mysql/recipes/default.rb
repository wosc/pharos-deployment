package "mysql-server-5.7"
package "mysql-client-5.7"

template "/usr/local/bin/mysql-backup" do
  source "mysql-backup"
  mode "0755"
end
template "/usr/local/bin/mysql-restore" do
  source "mysql-restore"
  mode "0755"
end
link "/etc/cron.daily/mysql-backup" do
  to "/usr/local/bin/mysql-backup"
end
