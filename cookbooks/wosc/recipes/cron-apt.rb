file "/etc/apt/apt.conf.d/20auto-upgrades" do
  action :delete
end

package "cron-apt"
template "/etc/cron-apt/config" do
  source "cron-apt.conf"
end
