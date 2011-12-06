import mc
import dreamboxee

config = mc.GetApp().GetLocalConfig()
ipaddress = config.GetValue("ipaddress")
if ipaddress:
	mc.ShowDialogNotification("IP address is: " + ipaddress)
else:
	ipaddress = mc.ShowDialogKeyboard("Dreambox IP", "", False)
	config.SetValue("ipaddress", ipaddress)

mc.ActivateWindow(14000)