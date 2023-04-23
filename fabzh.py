#Fabz - Cubzh Modloader
import os, time, threading, json, io, shutil, sys
from pathlib import Path
from fabzh_filejoiner import merge_files

if len(sys.argv) == 1:
	print("[Fabzh] No launch args. Try to use --start or --mods")
	sys.exit()

try:
	from colorama import init, Fore, Back, Style
	init()
	pref = f"{Fore.BLUE}[Fabzh]{Fore.WHITE}"
except:
	print("Colorama not installed, skipping..")
	pref = f"[Fabzh]"

print("Fabzh starting..")

if os.name == 'nt':
	ResourcesPath = Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Voxowl\\Particubes")
	GameCommand = '"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Cubzh\\Cubzh.exe"'
	ModsPath = Path(f"Mods\\")
elif os.name == 'posix':
	#Change to own path
	ResourcesPath = Path(f"~/Library/Group Containers/9JFN8QQG65.com.voxowl.particubes")
	GameCommand = 'open ~/Library/Application\\ Support/Steam/steamapps/common/Cubzh/Cubzh.app'
	ModsPath = Path(f"Mods/")

if "--mods" in sys.argv:
	files = os.walk(ModsPath)
	mods = []
	for file in files:
		if file[0] != "Mods":
			if "mod.json" in file[2]:
				try:
					jsonf = io.open(file[0]+"\\mod.json", mode="r", encoding="utf-8")
					content = ""
					for line in jsonf:
						content += line
					props = json.loads(content)
					if props['Name'] == "":
						raise ValueError('Name is empty')
					if props['Author'] == "":
						raise ValueError('Author is empty')
					if props['Version'] == "":
						raise ValueError('Version is empty')
					if props['Priority'] == "":
						raise ValueError('Priority is empty')
					add = True
					notadd = ""
					for mod in mods:
						if mod[3]['Name'] == props['Name']:
							if int(mod[3]['Version'].replace(".", "").replace("v", "").replace(" ", "")) >= int(props['Version'].replace(".", "").replace("v", "").replace(" ", "")):
								add = False
					if add:
						filea = (file[0], file[1], file[2], props)
						mods.append(filea)
						print(f"{pref} {props['Name']} {props['Version']}")
				except Exception as err:
					pass
			else:
				throw_err = True
				for mod in mods:
					if mod[0].replace("Mods\\", "") not in file[0]:
						continue
					else:
						throw_err = False
						break
				if throw_err == True:
					pass

	if len(mods) == 0:
		print(f"{pref} Mods not found")

	sys.exit()

if "--start" in sys.argv:
	LaunchArgs = ""

	files = os.walk(ModsPath)
	mods = []
	for file in files:
		if file[0] != "Mods":
			if "mod.json" in file[2]:
				try:
					jsonf = io.open(file[0]+"\\mod.json", mode="r", encoding="utf-8")
					content = ""
					for line in jsonf:
						content += line
					props = json.loads(content)
					if props['Name'] == "":
						raise ValueError('Name is empty')
					if props['Author'] == "":
						raise ValueError('Author is empty')
					if props['Version'] == "":
						raise ValueError('Version is empty')
					if props['Priority'] == "":
						raise ValueError('Priority is empty')
					add = True
					notadd = ""
					for mod in mods:
						if mod[3]['Name'] == props['Name']:
							if int(mod[3]['Version'].replace(".", "").replace("v", "").replace(" ", "")) >= int(props['Version'].replace(".", "").replace("v", "").replace(" ", "")):
								add = False
								notadd = "Same mod, but newer or equal version finded"
					if add:
						filea = (file[0], file[1], file[2], props)
						mods.append(filea)
						print(f"{pref} {props['Name']} {props['Version']} added to loading queue")
					else:
						print(f"{pref} Mod {props['Name']} {props['Version']} will not be loaded. {notadd}")
				except Exception as err:
					print(f"{pref} Mod {file[0].replace('Mods', '')[1:]} will not be loaded. {err}")
			else:
				throw_err = True
				for mod in mods:
					if mod[0].replace("Mods\\", "") not in file[0]:
						continue
					else:
						throw_err = False
						break
				if throw_err == True:
					print(f"{pref} Mod {file[0].replace('Mods', '')[1:]} will not be loaded. Missing mod.json")

	if len(mods) == 0:
		print(f"{pref} Mods not found")

	print(f"{pref} Starting Cubzh..")
	def cubzh():
		os.system(GameCommand + ' ' + LaunchArgs)
	cubzh_thread = threading.Thread(target=cubzh, args=())
	cubzh_thread.start()
	print(f"{pref} Cubzh started!")

	#Adjust it if not working
	time.sleep(1)

	if os.name == 'nt':
		os.system(os.path.abspath('PSTools\\pssuspend.exe') + ' "Cubzh.exe"')
	elif os.name == 'posix':
		os.system(f'kill -STOP com.voxowl.cubzh')
	time.sleep(0.1)
	print(f"{pref} Game suspended!")

	print(f"{pref} Sorting mods by priority..")

	def mods_sort(elem):
		return elem[3]['Priority']

	try:
		mods.sort(key = mods_sort)
	except Exception as err:
		print(f"{pref} Error when sorting mods. {err}, continuing without sorting.")

	print(f"{pref} Loading mods..")

	for mod in mods:
		print(f"{pref} Mod {mod[3]['Name']} {mod[3]['Version']} Loading..")
		try:
			if "bundle" in mod[1]:
				path = Path(mod[0]+"\\bundle\\")
				files = os.walk(path)
				for file in files:
					if file[0].replace(f"{mod[0]}\\bundle", "") != "":
						if len(file[2]) != 0:
							for moddedfile in file[2]:
								shutil.copy(os.path.abspath(file[0] + "\\" + moddedfile), os.path.join(str(ResourcesPath), file[0].replace(f"{mod[0]}\\", "")))
		except Exception as err:
			print(f"{pref} Error when loading {mod[3]['Name']}. {err}")
		time.sleep(0.05) # Fix drive issues (i think)

	print(f"{pref} Mods loaded!")
	time.sleep(0.1)
	if os.name == 'nt':
		os.system(os.path.abspath('PSTools\\pssuspend.exe') + ' -r "Cubzh.exe"')
	elif os.name == 'posix':
		os.system(f'kill -CONT com.voxowl.cubzh')
	print(f"{pref} Game resumed!")

	cubzh_thread.join()
	print(f"{pref} Cubzh stopped..")
	sys.exit()