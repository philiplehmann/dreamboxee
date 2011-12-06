import mc
from BeautifulSoup import BeautifulStoneSoup

def loadTVList():
	config = mc.GetApp().GetLocalConfig()
	ipaddress = config.GetValue("ipaddress")
	url = "http://" + ipaddress + "/web/epgsearch?search="
	list = mc.GetActiveWindow().GetList(120)
	data = mc.Http().Get(url)
	soup = BeautifulStoneSoup(data)
	mc.ShowDialogNotification("load data from " + url)
	itemList = mc.ListItems()
	for event in soup.findAll('e2event'):
		item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_OTHER)
		print event.e2eventservicename.renderContents()
		item.SetLabel(event.e2eventservicename.renderContents())
		item.SetPath("http://" + ipaddress + ":8001/" + event.e2eventservicereference.renderContents())
		itemList.append(item)
	mc.GetActiveWindow().GetList(120).SetItems(itemList)

def loadRadioList():
	mc.ShowDialogNotification("load radiolist. will be implemented later!")

def loadEPG():
	mc.ShowDialogNotification("load epg. will be implemented later!")

