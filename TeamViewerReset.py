import os
import regobj as reg
from shutil import rmtree


def del_appdata_tv_dir():
	""" Delete the Teamviewer folder stored in Application Data """

	os.chdir(os.getenv("APPDATA"))
	shutil.rmtree(os.getcwd() + "\\TeamViewer")


def del_tv_reg_keys():
	""" Delete Teamveiwer's registry keys, placed in HKLM and HKCU """

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


def test():
	""" Function showing the features the module """

	conns = get_networks_info()
	print "Default output"
	print_net_info(conns)

	raw_input()

	conns = get_networks_info("pci")
	print "Filtered output with \"PCI\""
	print_net_info(conns)
