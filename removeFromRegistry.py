import _winreg
import RegistryManager as rm

HKCUKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\")

subs = rm.getSubKeysList(HKCUKey)

rm.walkSubkeys(HKCUKey)





