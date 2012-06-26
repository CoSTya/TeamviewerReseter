import argparse
import TeamViewerReset as TVR
	

	return choices


def configure():
	""" Parse command line options """
	parser = argparse.ArgumentParser(description="Reset TeamViewer's ID")

	parser.add_argument(
		"-l", "--list", 
		action="store_true",
		help="List the available network devices")

	parser.add_argument(
		"filter", 
		nargs="?", 
		default="", 
		help="Show only the devices with an ID or description, which contains the filter-word")

	
	conf = parser.parse_args()

	return conf


def main(conf):
	

	if conf.list:
		networkInfo = TVR.get_networks_info(conf.filter)


	choiceList = format_combo_choices(networkInfo)
	for c in choiceList:
				print c


if __name__ == "__main__":
	main(configure())
