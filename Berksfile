# -*- ruby -*-

cookbooks_dir = File.expand_path(File.dirname(__FILE__) + "/cookbooks")
Dir.glob(cookbooks_dir + "/*/").each do |path|
  cookbook File.basename(path), path: path
end

source "https://supermarket.chef.io"
