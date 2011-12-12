import mc
from BeautifulSoup import BeautifulStoneSoup
from datetime import datetime

current_navigation = 'none'
tv_services = None
tv_list = None
epg_events = None
radio_services = None
config = mc.GetApp().GetLocalConfig()

def loadTVList(update = False):
	global current_navigation, tv_list
	# exit function if it already is loaded
	if current_navigation == 'tv':
		return
		
	current_navigation = 'tv'
	
	mc.GetActiveWindow().GetList(120).SetItems(createTVList(False))

def loadRadioList():
	global current_navigation, config, radio_services
	current_navigation = 'radio'
	if radio_services is None:
		ipaddress = config.GetValue("ipaddress")
		radio_url = "http://" + ipaddress + "/web/getservices?sRef=1:7:2:0:0:0:0:0:0:0:(type%20==%202)%20ORDER%20BY%20name"
		radio_data = mc.Http().Get(radio_url)
		radio_services = BeautifulStoneSoup(radio_data)
	
	# create new list
	itemList = mc.ListItems()
	for service in radio_services.findAll('e2service'):
		item = mc.ListItem(mc.ListItem.MEDIA_AUDIO_RADIO)
		
		reference = service.e2servicereference.renderContents()
		item.SetPath("http://" + ipaddress + "/web/stream.m3u?ref=" + reference)
		item.SetLabel(service.e2servicename.renderContents())
		itemList.append(item)
	mc.GetActiveWindow().GetList(120).SetItems(itemList)

def loadRecordList():
	global current_navigation
	current_navigation = 'record'
	mc.GetActiveWindow().GetList(120).SetItems(mc.ListItems())
	mc.ShowDialogNotification("load recordlist. will be implemented soon")

def loadEPG():
	global current_navigation
	current_navigation = 'epg'
	mc.GetActiveWindow().GetList(120).SetItems(mc.ListItems())
	mc.ShowDialogNotification("load epg. will be implemented soon")


def loadTVServices(update = False):
	global tv_services, config
	if tv_services is not None and update == False: return tv_services
	# get the ip from the config
	ipaddress = config.GetValue("ipaddress")
	# get service list
	service_url = "http://" + ipaddress + "/web/getservices?sRef=1:7:1:0:0:0:0:0:0:0:(type%20==%201)%20||%20(type%20==%2017)%20||%20(type%20==%20195)%20||%20(type%20==%2025)%20ORDER%20BY%20name"
	service_data = mc.Http().Get(service_url)
	tv_services = BeautifulStoneSoup(service_data)
	return tv_services

def createTVList(update = False):
	global tv_list, config
	
	ipaddress = config.GetValue("ipaddress")
	
	# create new list
	itemList = mc.ListItems()
	
	service_soup = loadTVServices(False)
	epg_soup = loadTVEpg(update)
	
	# iterate services
	for service in service_soup.findAll('e2service'):
		item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_OTHER)
		
		reference = service.e2servicereference.renderContents()
		item.SetPath("http://" + ipaddress + "/web/stream.m3u?ref=" + reference)
		epg = False
		for event in epg_soup.findAll('e2event'):
			if event.e2eventservicereference.renderContents() == reference:
				epg = event
				break
		label = service.e2servicename.renderContents()
		if epg:
			start = epg.e2eventstart.renderContents()
			title = epg.e2eventtitle.renderContents()
			desc  = epg.e2eventdescriptionextended.renderContents()
			try:
				label += " - " + datetime.fromtimestamp(float(start)).strftime("%H:%M")
				label += " " + title
				item.SetDescription(desc, False)
			except ValueError:
				print "no valid data available, skip channel: " + service.e2servicename.renderContents()
			
		item.SetLabel(label)
		itemList.append(item)
	
	tv_list = itemList
	return tv_list

def loadTVEpg(update = False):
	global epg_events, config
	if epg_events is not None and update == False:
		return epg_events
	# get the ip from the config
	ipaddress = config.GetValue("ipaddress")
	# get the current epg list
	epg_url = "http://" + ipaddress + "/web/epgnow?bRef=1:7:1:0:0:0:0:0:0:0:(type%20==%201)%20||%20(type%20==%2017)%20||%20(type%20==%20195)%20||%20(type%20==%2025)%20ORDER%20BY%20name"
	epg_data = mc.Http().Get(epg_url)
	epg_events = BeautifulStoneSoup(epg_data)
	return epg_events

