package "exim4-daemon-heavy"
service "exim4" do
  supports :status => true, :restart => true, :reload => true
end


wosc_mysql_database "mailserver"
wosc_mysql_user "mail" do
  password node["mailserver"]["db_pass"]
end
wosc_mysql_grant "mailserver" do
  user "mail"
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
