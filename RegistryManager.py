import _winreg

def getSubKeysList(key):

	subkeysList = []

	try:
		index = 0
		while(True):
			subkeysList.append(_winreg.EnumKey(key, index))
			index += 1
	except:
		pass

	return subkeysList


def getValuesList(key):

	valuesList = []

	try:
		index = 0
		while(True):
			valuesList.append(_winreg.EnumValue(key, index))
			index += 1
	except:
		pass

	return valuesList


def delKey(key):
	
	
	subkeys = getSubKeysList(key)

	for k in subkeys:
		delKey(_winreg.OpenKey(key, k))

	_winreg.DeleteKey(key, r"")

def walkSubkeys(key):

	subkeys = getSubKeysList(key)
	for subkey in subkeys:
		print subkey
		walkSubkeys(_winreg.OpenKey(key, subkey))

