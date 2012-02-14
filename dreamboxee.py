import mc
from BeautifulSoup import BeautifulStoneSoup
from datetime import datetime

config = mc.GetApp().GetLocalConfig()
current_navigation = 'none'
tv_list = None
epg_list = None
radio_services = None
# get the ip from the config
ipaddress = config.GetValue("ipaddress")

#tv start
def loadTVList(update = False):
	global current_navigation
	# exit function if it already is loaded
	if current_navigation == 'tv':
		return
		
	current_navigation = 'tv'
	
	mc.GetActiveWindow().GetList(120).SetItems(createTVList(False))

def createTVList(update = False):
	global tv_list, config, ipaddress

	# create new list
	itemList = mc.ListItems()

	epg_list = loadTVEpg(True)

	# iterate services
	for service in epg_list:
		item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_OTHER)
		item.SetPath("http://" + ipaddress + ":8001/" + service['reference'])

		label = service['servicename']
		try:
			label += " - " + datetime.fromtimestamp(float(service['start'])).strftime("%H:%M")
			label += " " + service['title']
			item.SetDescription(service['description'] + ' ' + service['descriptionextended'], False)
		except ValueError:
			print "DREAMBOXEE: no descriptin aviable for: " + service['servicename']

		item.SetLabel(label)
		itemList.append(item)

	tv_list = itemList
	return tv_list

def loadTVEpg(update = False):
	global epg_list, config, ipaddress
	if epg_list is not None and update == False:
		return epg_list
	# get the current epg list
	epg_url = "http://" + ipaddress + "/web/epgnow?bRef=1:7:1:0:0:0:0:0:0:0:(type%20==%201)%20||%20(type%20==%2017)%20||%20(type%20==%20195)%20||%20(type%20==%2025)%20ORDER%20BY%20name"
	epg_data = mc.Http().Get(epg_url)
	epg_events = BeautifulStoneSoup(epg_data)
	epg_list = []
	for event in epg_events.findAll('e2event'):
		epg_list.append({
			'reference': event.e2eventservicereference.renderContents(),
			'id': event.e2eventid.renderContents(),
			'start': event.e2eventstart.renderContents(),
			'duration': event.e2eventcurrenttime.renderContents(),
			'currenttime': event.e2eventservicereference.renderContents(),
			'title': event.e2eventtitle.renderContents(),
			'description': event.e2eventdescription.renderContents(),
			'descriptionextended': event.e2eventdescriptionextended.renderContents(),
			'servicename': event.e2eventservicename.renderContents()
		})
	epg_list.sort(compareEpgList)
	return epg_list

def compareEpgList(a, b):
	return cmp(a['servicename'], b['servicename'])
# tv end

# begin radio
def loadRadioList():
	global current_navigation, config, radio_services, ipaddress
	current_navigation = 'radio'
	if radio_services is None:
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
	#http://192.168.0.160/web/movielist?dirname=/hdd/movie/&tag=
	mc.GetActiveWindow().GetList(120).SetItems(mc.ListItems())
	mc.ShowDialogNotification("load recordlist. will be implemented soon")

def loadEPG():
	global current_navigation
	current_navigation = 'epg'
	mc.GetActiveWindow().GetList(120).SetItems(mc.ListItems())
	mc.ShowDialogNotification("load epg. will be implemented soon")


