directory "/srv/letsencrypt/public" do
  owner "letsencrypt"
end
directory "/srv/letsencrypt/data" do
  owner "letsencrypt"
  group "letsencrypt"
  mode "0770"
end


[
  "grmusik.de",
  "wosc.de",
  "mail.wosc.de",
  "pharos.wosc.de",
].each do |domain|
  directory "/srv/letsencrypt/public/#{domain}" do
    owner "letsencrypt"
  end

  directory "/srv/letsencrypt/data/#{domain}" do
    owner "letsencrypt"
  end
  cookbook_file "/srv/letsencrypt/data/#{domain}/account_key.json" do
    source "#{domain}.account"
    owner "letsencrypt"
    group "letsencrypt"
    mode "0600"
  end
  cookbook_file "/srv/letsencrypt/data/#{domain}/key.pem" do
    source "#{domain}.key"
    owner "letsencrypt"
    group "letsencrypt"
    mode "0640"
  end
end

cookbook_file "/srv/letsencrypt/data/mail.wosc.de/update" do
  source "mail.wosc.de.update"
  mode "0755"
end
