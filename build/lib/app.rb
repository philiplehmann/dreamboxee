require './lib/app_descriptor'

class App
  
  def self.get_description(env)
    
    descriptor_file = get_file env
    
    unless File.exists? descriptor_file
      descriptor_file = get_file(:default)
    end
    
    return AppDescriptor.from_xml descriptor_file
  end
  
  private 
    def self.get_file(env)
      if env == :default
        return "./../descriptor.xml"
      else
        return "./../descriptor.#{env}.xml"
      end
    end
end