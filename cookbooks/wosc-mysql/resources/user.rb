property :name, kind_of: String, name_property: true
property :password, kind_of: String, required: true


action :create do
  mysql = "mysql -Bs -uroot mysql"
  create = "CREATE USER '#{new_resource.name}'@'localhost';"
  setpass = ("SET PASSWORD FOR '#{new_resource.name}'@'localhost' = " +
             "PASSWORD('#{new_resource.password}');")
  user_exists = "SELECT * FROM user WHERE User='#{new_resource.name}';"

  execute "mysql_user_#{new_resource.name}_create" do
    command "echo \"#{create}\" | #{mysql}"
    not_if "echo \"#{user_exists}\" | #{mysql} | grep -q ."
  end
  execute "mysql_user_#{new_resource.name}_setpass" do
    command "echo \"#{setpass}\" | #{mysql}"
  end
end
