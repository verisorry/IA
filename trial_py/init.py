import os, sys, shutil

def start():
	if os.path.exists("QPResults"):
		shutil.rmtree("QPResults")
	if os.path.exists("MSResults"):
		shutil.rmtree("MSResults")

	
	system = sys.platform
	os_name = os.name
	if system == "darwin" or system == "linux":
		os.system("pip install -r requirements.txt")
		os.system("clear")
		return True
	elif system == "win32":
		return False

start()
