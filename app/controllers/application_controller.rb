class ApplicationController < ActionController::Base
  protect_from_forgery
  
  def index
    
  end
  
  def xml2json
    channels = {}
    p params
    render :json => channels
  end
end
