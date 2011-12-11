require 'xmlsimple'
require 'FileUtils'

class AppDescriptor < Hash
  
  def copy_for_deployment(descriptor_additions, version)
    
    deployment_descriptor = AppDescriptor.new
    deployment_descriptor.replace self
    deployment_descriptor.merge! descriptor_additions
    deployment_descriptor['version'] = version
    deployment_descriptor.delete 'test-app'
    
    return deployment_descriptor
  end
  
  def to_xml(xml_file)
    xml = XmlSimple.xml_out(Hash[self], {'NoAttr' => true, 'RootName' => 'app', 'OutputFile' => xml_file})
  end
  
  def self.from_xml(xml_file)
    
    descriptor = new
    descriptor.replace XmlSimple.xml_in(xml_file, 'ForceArray' => false)    
    return descriptor
    
  end
  
end