property :database, kind_of: String, name_property: true
property :user, kind_of: String, required: true


action :create do
  mysql = "mysql -Bs -uroot mysql"
  grant = ("GRANT ALL ON #{new_resource.name}.* TO " +
           "'#{new_resource.user}'@'localhost';")
  execute "mysql_grant_#{new_resource.name}" do
    command "echo '#{grant}' | #{mysql}"
  end
end
