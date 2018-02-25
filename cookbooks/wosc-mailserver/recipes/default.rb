package "exim4-daemon-heavy"
service "exim4" do
  supports :status => true, :restart => true, :reload => true
end


wosc_mysql_database node["mailserver"]["db_name"]
wosc_mysql_user node["mailserver"]["db_user"] do
  password node["mailserver"]["db_pass"]
end
wosc_mysql_grant node["mailserver"]["db_name"] do
  user node["mailserver"]["db_user"]
end

template "/etc/exim4/schema.sql" do
  source "schema.sql"
end
execute "mailserver_db_schema" do
  command "mysql -Bs -uroot mailserver < /etc/exim4/schema.sql"
  not_if "echo 'show tables' | mysql -uroot mailserver | grep -q ."
end


file "/etc/exim4/update-exim4.conf" do
  content "dc_eximconfig_configtype='none'"
  notifies :run, "execute[update-exim4.conf]"
end
execute "update-exim4.conf" do
  action :nothing
end

directory "/etc/exim4/domains"

link "/etc/exim4/system-filter" do
  to "/home/wosc/.dot/mail/.filter-system"
end
link "/var/mail/wosc@wosc.de/filter" do
  to "/home/wosc/.dot/mail/.filter"
  only_if "ls /var/mail/wosc@wosc.de"
end

template "/etc/aliases" do
  source "aliases"
end
file "/etc/email-addresses" do
  content "wosc: wosc@wosc.de"
end

template "/etc/exim4/exim4.conf" do
  source "exim4.conf"
  notifies :reload, "service[exim4]"
end

directory "/var/mail" do
  group "Debian-exim"
end


package "clamav"
package "clamav-daemon"
service "clamav-daemon"

group "Debian-exim" do
  action :manage
  append true
  members "clamav"
end

execute "sed -i -e 's/AllowSupplementaryGroups false/AllowSupplementaryGroups true/' /etc/clamav/clamd.conf" do
  only_if "grep -q 'AllowSupplementaryGroups false' /etc/clamav/clamd.conf"
  notifies :restart, "service[clamav-daemon]", :delayed
end

directory "/var/spool/exim4/scan" do
  owner "Debian-exim"
  group "Debian-exim"
  mode "0775"
end


package "courier-imap-ssl"
service "courier-imap-ssl"
package "courier-authlib-mysql"
service "courier-authdaemon"

group "courier" do
  action :manage
  append true
  members "Debian-exim"
end

template "/etc/courier/authdaemonrc" do
  source "courier/authdaemonrc"
  owner "daemon"
  group "daemon"
  mode "0660"
  notifies :restart, "service[courier-authdaemon]", :delayed
end
template "/etc/courier/authmysqlrc" do
  source "courier/authmysqlrc"
  owner "daemon"
  group "daemon"
  mode "0660"
  notifies :restart, "service[courier-authdaemon]", :delayed
end

template "/etc/courier/imapd-ssl" do
  source "courier/imapd-ssl"
  notifies :restart, "service[courier-imap-ssl]"
end
