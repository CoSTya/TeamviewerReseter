import wx
import TeamViewerReset


class MainWindow(wx.Frame):
		
	def __init__(self, parent, title):

		wx.Frame.__init__(self, parent, title=title, size=(400,300), 
			style=(wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION))

		self.init_ui()

	def init_ui(self):

		pnl = wx.Panel(self)

		networkInfo = TeamViewerReset.get_networks_info()
		choiceList = format_combo_choices(networkInfo)


		cb = wx.ComboBox(pnl, value=choiceList[0], choices=choiceList, 
			style=(wx.CB_READONLY|wx.CB_SORT))

		self.rb1 = wx.RadioButton(pnl, label="All", pos=(30, 30))
		self.rb2 = wx.RadioButton(pnl, label="PCI", pos=(30, 50))

		self.CreateStatusBar()

		self.Centre()
		self.Show(True)


def format_combo_choices(network_info):

	choices = []

	connectionName = network_info.keys()

	connectionDevice = network_info.values()

	choices = [("%s - %s" % (x, network_info[x][0])) for x in network_info]

	

	return choices


app = wx.App(False)
frame = MainWindow(None, 'TeamViewer Reset')
app.MainLoop()