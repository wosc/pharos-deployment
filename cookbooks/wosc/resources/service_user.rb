property :name, kind_of: String, name_property: true
property :shell, kind_of: String, default: "/bin/false"


action :create do
  user new_resource.name do
    home "/srv/#{new_resource.name}"
    shell new_resource.shell
  end

  directory "/srv/#{new_resource.name}" do
    owner new_resource.name
  end
end
