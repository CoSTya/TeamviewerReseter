import os
import regobj as reg
from shutil import rmtree
import subprocess


def del_appdata_tv_dir():
	""" Delete the Teamviewer folder stored in Application Data """

	os.chdir(os.getenv("APPDATA"))
	shutil.rmtree(os.getcwd() + "\\TeamViewer")


def del_tv_reg_keys():
	""" Delete Teamviewer's registry keys, placed in HKLM and HKCU """

	key = reg.HKLM.Software
	key.del_subkey("Teamviewer")
	
	key = reg.HKCU.Software
	key.del_subkey("Teamviewer")


def get_network_interfaces():
	""" Return a dictionary with interface description, and their repsective
	device ID """

	interfaces = {}

	key = reg.HKLM.SYSTEM.CurrentControlSet.Control.Class

	interfaces_key = None


	for sk in key.subkeys():
		if "Class" in sk:
			if sk["Class"].data == "Net":
				interfaces_key = sk

	if interfaces_key:
		for sk in interfaces_key.subkeys():
			if "ComponentId" in sk:
				if "DriverDesc" in sk:
					interfaces[sk["DriverDesc"].data] = sk["ComponentId"].data

	return interfaces


def get_network_connections():
	""" Return a dictionary with the connection names and their
	respective Device ID """

	connections = {}

	key = reg.HKLM.SYSTEM.CurrentControlSet.Control.Network

	for sk in key.subkeys():
		if "Class" in sk:
			if sk["Class"].data == "Net":
				key = sk

	for sk in key.subkeys():
		if "Connection" in sk:
			connections[sk.Connection["Name"].data] = sk.Connection["PnpInstanceID"].data

	return connections


def match_interfaces_to_connections(interfaces, connections):
	""" Given two dictionaries, creates matches to determine
	the valid and running connections, and return a dictionary
	with the connection's name as the key and a tuple with
	the device ID and the device description as the key's value 

	Example:

	{"Local Area Connection 2: ("Broadcom NetXtreme Ethernet Adapter", "pci/dev1232sys5456"), ...}

	"""
	
	matches = {}

	for interface in interfaces:
		for conn in connections:
			if interfaces[interface].upper() in connections[conn]:
				matches[conn] = (interface, interfaces[interface])

	return matches


def get_networks_info(filterWord=""):
	""" Returns a dictionary with all the network connections
	available. If a filter word is specified only connections 
	with device descriptions or device IDs containing the
	filter word will be returned """
		

	interfaces = get_network_interfaces()
	connections = get_network_connections()
	matches = match_interfaces_to_connections(interfaces, connections)

	networksInfo = {}

	for m in matches:
		
		filterWordInDesc = filterWord.upper() in matches[m][0].upper() # ignore case
		filterWordInID = filterWord.upper() in matches[m][1].upper()

		if filterWordInDesc or filterWordInID:
			networksInfo[m] = matches[m]

	return networksInfo

def devcon_run(command, devID):
	""" Runs the devcon program with the specified command.
	If the result contains the devID which is given, then
	the command has been executed successfully and True is returned """

	VALID_COMMANDS = ["enable", "disable"]

	if command.lower() in VALID_COMMANDS:

		devconProc = subprocess.Popen(["bin\\devcon.exe", command, devID], stdout=subprocess.PIPE)
		result = devconProc.communicate()[0]

		return devID.upper() in result.upper()
	else:
		return False

def macshift_run(netName):
	""" Runs the macshift program, with the name of the network's
	MAC to be changed to a new random MAC"""

	# Network Name must be encoded in order to work with macshift
	netName = netName.encode("Windows-1253")

	macshiftProc = subprocess.Popen(["bin\\macshift.exe", "-r", "-i", netName], stdout=subprocess.PIPE)
	result = macshiftProc.communicate()[0]

	""" When macshift.exe fails to change the MAC, it says:
	"Could not find adapter name..."

	So checking if the string "Could not" is in the result
	is enough to tell if the MAC change was successful or not """

	success = not ("could not" in result.lower())

	return success
	
def change_mac(networkName, deviceID):
	""" Changes the MAC address of the specified network.
	The arguments that must be passed are the network's name
	and the device's ID. Return True if the change was successful """

	success = False

	if networkName and deviceID:
		if devcon_run("disable", deviceID):
			
			success = macshift_run(networkName)
			devcon_run("enable", deviceID)

	return success


def test():
	""" Function showing the features of the module """

	conns = get_networks_info()
	print "Default output"
	
	net_to_test = None

	for k in conns:
		print "%s - %s, %s" % (k, conns[k][0], conns[k][1])
		if "Y" in raw_input("Is it this one? (Y/) ").upper():
			net_to_test = k
			break

	if net_to_test:
		change_mac(net_to_test, conns[net_to_test][1])

if __name__ == '__main__':
	test()