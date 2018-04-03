property :dbname, kind_of: String, name_property: true


action :create do
  mysql = "mysql -Bs -uroot mysql"
  create = ("CREATE DATABASE IF NOT EXISTS #{new_resource.dbname} " +
            "DEFAULT CHARACTER SET 'UTF8';")
  execute "mysql_database_#{new_resource.dbname}_create" do
    command "echo \"#{create}\" | #{mysql}"
  end
end
