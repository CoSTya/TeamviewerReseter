import sys
import argparse
import TeamViewerReset as TVR
		

def configure():
	""" Parse command line options and return them """
	
	parser = argparse.ArgumentParser(description="Reset TeamViewer's ID")

	parser.add_argument(
		"-l", "--list", 
		action="store_true",
		help="List the available network devices")

	parser.add_argument(
		"filter",
		nargs='?',
		default="",
		help="Show only the devices with an ID or description, which contains the filter-word")
	
	conf = parser.parse_args()

	return conf

def list_networks(filterWord=""):
	""" Prints the available networks. The function accepts
	an optional filter-word argument so that only certain
	network connections can be viewed """

	networkInfo = TVR.get_networks_info(filterWord)

	for k in networkInfo:
		print "%s - %s" % (k, networkInfo[k][0])



def main(conf):
	""" Gets the parsed arguments and handles them """

	# List network connections
	if conf.list:
		list_networks(conf.filter)
		print "Press any key to exit..."
		raw_input()
		return 0


if __name__ == "__main__":
	sys.exit(main(configure()))
