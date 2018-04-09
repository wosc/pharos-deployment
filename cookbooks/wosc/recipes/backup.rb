directory "/root/.ssh"

# Used by rsnapshot from laptop
file "/root/.ssh/authorized_keys" do
  content "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvbphVBqmZQdb+p6ve6MteU89ufDWTfDKL/aZBnA3gTlulFSrlfOns9Smhzyo1AjrTkFlF5kAXH2RYrHbjU+nHzUN0S8Jx6AdXHVo7NZd2Qi/7YVca2vDeSAnC5/vungj0uc9IR2LDK+wMDoY/uaVJM9e8R2weqmylepUjJQE1JM71zK70uoy4qCR3DHI7MJmfD1ZGejLdqsolUpTnAqhzd/Vp5ZZFHOPN/sWmqHw4PVyJpcc6+4wDqr0dRdMkApQNshHVdLhK6U+//00UJ5RmM6x1d5qMauHUOs0AJig7SpHr9p9gbOmUPjNhD0yE/e9U+MgP2dN/lakrY9Y1kvjfw== root@nautis.wosc.de"
  mode "0600"
end


# Hourly calendar backup
directory "/srv/radicale/backup" do
  owner "radicale"
  group "radicale"
end

package "rsnapshot"
template "/srv/radicale/backup/wosc.conf" do
  source "rsnapshot-calendar.conf"
end

cron "rsnapshot-calendar-hourly" do
  command "rsnapshot -c /srv/radicale/backup/wosc.conf hourly"
  minute "0"
  user "radicale"
end
cron "rsnapshot-calendar-daily" do
  command "rsnapshot -c /srv/radicale/backup/wosc.conf daily"
  minute "15"
  hour "0"
  user "radicale"
end
