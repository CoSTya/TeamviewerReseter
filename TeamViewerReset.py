"""
TeamViewerReset.py

Synopsis: The module contains various functions for tasks required 
for the resetting of TeamViewer's unique ID.

These tasks are:
	- Removal of some registry keys
	- Removal of a directory stored in AppData
	- Change of the network card's MAC address


Author: Alex Ioannidis <atipa@otenet.gr>
Date: June 2012

"""


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
	""" Return a list of dictionaries with the interface description and their repsective device ID

	Example dictionary:
	interface = {"Name" : "Broadcom NetXtreme Gigabit",
	"ID" : "pci/dev1232sys5456"} 

	"""

	interfacesList = []

	key = reg.HKLM.SYSTEM.CurrentControlSet.Control.Class

	interfaces_key = None


	# Find the registry key holding all the Network Interfaces

	for sk in key.subkeys():
		if "Class" in sk:
			if sk["Class"].data == "Net":
				interfaces_key = sk

	# Search in the interfaces, and add the ones with description and ID

	if interfaces_key:
		for sk in interfaces_key.subkeys():
			if "ComponentId" in sk:
				if "DriverDesc" in sk:
					interface = {"Description" : sk["DriverDesc"].data, 
					"ID" : sk["ComponentId"].data}
					
					interfacesList.append(interface)

	return interfacesList


def get_network_connections():
	""" Return a list of dictionaries with the connection names and their respective Device ID

	Example dictionary:
	connection = {"Name" : "Local Area Connection 4",
	"ID" : "pci/dev1232sys5456"}

	"""

	connectionsList = []

	key = reg.HKLM.SYSTEM.CurrentControlSet.Control.Network

	connections_key = None

	# Find the registry key holding all the available Network Connections

	# TODO: Modify function to work on Windows 7 (and possibly Vista aswell)
	# since the keys in Win7 doesn't have a value specifying which key holds
	# network connections info, so the code below is useless

	for sk in key.subkeys():
		if "Class" in sk:
			if sk["Class"].data == "Net":
				connections_key = sk

	# Search in the networks and find all the ones with a Name and a DeviceID

	for sk in connections_key.subkeys():
		if "Connection" in sk:
			connection = {"Name" : sk["Name"].data,
			"ID" : sk["PnpInstanceID"].data}

			connectionsList.append(connection)


	return connectionsList


def get_matching_networks_to_interfaces():
	""" Given two lists produced by the get_network_connections
	and get_network_interfaces functions, find the network connections
	that have DeviceIDs that match the IDs of the interfaces we have .

	After the matching process is completed, a new list is returned
	containing dictionaries holding the Connection Name, the Interface
	Description and the Interface ID.

	Example dictionary:
	matchedConnection = {"Name" : "Local Area Network 2",
	"InterfaceDesc" : "Broadcom NetXtreme Ethernet Adapter",
	"InterfaceID" : "pci/dev1232sys5456"}

	"""
	
	matchedConnectionsList = []

	connectionsList = get_network_connections()
	interfacesList = get_network_interfaces()

	for interface in interfacesList:
		for connection in connectionsList:
			if interface["ID"].upper() in connection["ID"].upper():
				matchedConnection = {"Name" : connection["Name"],
				"InterfaceDesc" : interface["Description"],
				"InterfaceID" : interface["ID"]}

				matchedConnectionsList.append(matchedConnection)

	return matchedConnectionsList


def get_available_networks(filterWord=""):
	""" Returns a list of dictionaries with all the network connections
	available. If a filter word is specified only connections 
	with device descriptions or device IDs containing the filter-word,
	will be returned

	"""
	
	availableNetworks = []

	matchedNetworks = get_matching_networks_to_interfaces()

	for m in matchedNetworks:
		
		filterWordInDesc = filterWord.upper() in m["InterfaceDesc"].upper()
		filterWordInID = filterWord.upper() in m["InterfaceID"].upper()

		if filterWordInDesc or filterWordInID:
			
			availableNetworks.append(m)

	return availableNetworks

def devcon_run(command, devID):
	""" Runs the devcon program with the specified command.
	If the result contains the devID which is given, then
	the command has been executed successfully and True is returned 

	"""

	VALID_COMMANDS = ["enable", "disable"]

	if command.lower() in VALID_COMMANDS:

		devconProc = subprocess.Popen(["bin\\devcon.exe", command, devID], stdout=subprocess.PIPE)
		result = devconProc.communicate()[0]

		return devID.upper() in result.upper()
	else:
		return False

def macshift_run(netName):
	""" Runs the macshift program, with the name of the network's
	MAC to be changed to a new random MAC

	"""

	# Network Name must be encoded in order to work with macshift
	netName = netName.encode("Windows-1253")

	macshiftProc = subprocess.Popen(["bin\\macshift.exe", "-r", "-i", netName], stdout=subprocess.PIPE)
	result = macshiftProc.communicate()[0]

	""" When macshift.exe fails to change the MAC, it says:
	"Could not find adapter name..."

	So checking if the string "Could not" is in the result
	is enough to tell if the MAC change was successful or not 

	"""

	success = not ("could not" in result.lower())

	return success
	
def change_mac(networkName, deviceID):
	""" Changes the MAC address of the specified network.
	The arguments that must be passed are the network's name
	and the device's ID. Return True if the change was successful 

	"""

	success = False

	if networkName and deviceID:
		if devcon_run("disable", deviceID):
			
			success = macshift_run(networkName)
			devcon_run("enable", deviceID)

	return success


def test():
	""" Function showing the features of the module """

	interfaces = get_network_interfaces()

	for i in interfaces:
		print "Interface Desc: %s" % i["Description"]
		print "Interface ID: %s" % i["ID"]

if __name__ == '__main__':
	test()