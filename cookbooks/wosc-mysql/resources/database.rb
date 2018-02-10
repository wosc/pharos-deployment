property :name, kind_of: String, name_property: true


action :create do
  mysql = "mysql -Bs -uroot mysql"
  create = ("CREATE DATABASE IF NOT EXISTS #{new_resource.name} " +
            "DEFAULT CHARACTER SET 'UTF8';")
  execute "mysql_database_#{new_resource.name}_create" do
    command "echo \"#{create}\" | #{mysql}"
  end
end
