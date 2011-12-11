require './lib/app'
require './lib/app_descriptor'
require './lib/zipper'

class Packager
  
  def initialize(packaging_dir, zipper)
    @packaging_dir = packaging_dir
    @zipper = zipper
  end
  
  def package(env_config, version)

    env = env_config.first
    puts "packaging for '#{env}'"
    
    descriptor = App.get_description env
    
    descriptor_for_packaging = descriptor.copy_for_deployment env_config[1], version
    descriptor_for_packaging.to_xml File.join(@packaging_dir, 'descriptor.xml')
    
    @zipper.zip descriptor_for_packaging['id'], version
    
  end
  
end
