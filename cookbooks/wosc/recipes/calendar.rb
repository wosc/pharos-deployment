python_runtime "ical" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/usr/local/ical" do
  python "ical"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/usr/local/ical/requirements.txt" do
  source "ical-requirements.txt"
end

pip_requirements "/usr/local/ical/requirements.txt" do
  virtualenv "/usr/local/ical"
  options "--no-deps"
end


caldav = "/srv/radicale/data/wosc@wosc.de"

# Sends reminder email for upcoming birthdays
cron "cal-remind" do
  command "/usr/local/ical/bin/python /home/wosc/bin/icalremindmail.py < #{caldav}/geburtstage.ics"
  hour "6"
  minute "0"
  user "wosc"
  mailto "wosc@wosc.de"
end
# Provides acces to my doodle participations via my default caldav source
cron "cal-doodle" do
  command "curl --silent #{node['wosc']['doodle_ical']} | sed -e 's/@doodle.biz/doodle.biz/' > #{caldav}/doodle.ics"
  minute "*/30"
  user "wosc"
  mailto "wosc@wosc.de"
end
# Provides access to scheduled todos via my default caldav source
cron "cal-thinkgingrock" do
  command "/usr/local/ical/bin/python /home/wosc/bin/ical_filter_thinkingrock.py < /home/wosc/sync/plan/wosc.ics > #{caldav}/thinkingrock.ics; chmod g+w #{caldav}/thinkingrock.ics"
  minute "*/5"
  user "wosc"
  mailto "wosc@wosc.de"
end
cron "cal-haemera" do
  command "curl --silent http://localhost:7078/ical/scheduled > #{caldav}/haemera.ics"
  minute "*/5"
  user "wosc"
  mailto "wosc@wosc.de"
end
