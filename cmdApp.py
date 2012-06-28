import sys
import argparse
import TeamViewerReset as TVR
		

def configure():
	""" Parse command line options and return them """
	
	# Top level parsers	
	parser = argparse.ArgumentParser(description="Reset TeamViewer's ID")


	list_group = parser.add_argument_group("List", "List network connections and their info")
	reset_group = parser.add_argument_group("Reset", "Actions to reset the TeamViewer ID")
	

	list_group.add_argument(
		"-l", "--list", 
		nargs="?",
		default="",
		dest="filter",
		metavar="FILTER",
		help="List the available network devices")

	reset_group.add_argument(
		"-r", "--registry",
		action="store_true",
		help="Remove the registry values")

	reset_group.add_argument(
		"-d", "--directory",
		action="store_true",
		help="Remove the AppData sub-directory")

	reset_group.add_argument(
		"-m", "--MAC",
		action="store_true",
		help="Change the MAC of the network that's specified" +
		"interactive mode is entered")

	reset_group.add_argument(
		"-a", "-all", 
		action="store_true",
		help="Execute all the actions to reset the TeamViewer ID")

	reset_group.add_argument(
		"network",
		nargs="?",
		default="",
		help="If a network index is not specified")

	conf = parser.parse_args()

	return conf


def list_networks(filterWord=""):
	""" Prints the available networks. The function accepts
	an optional filter-word argument so that only certain
	network connections can be viewed

	 """

	networkInfo = TVR.get_networks_info(filterWord)

	# Create index numbers for the networks


	for k in networkInfo:
		print "%s - %s" % (k, networkInfo[k][0])


def main(conf):
	""" Gets the parsed arguments and handles them """

	# List network connections
	if conf.filter:
		list_networks(conf.filter)
		return 0



if __name__ == "__main__":
	sys.exit(main(configure()))
