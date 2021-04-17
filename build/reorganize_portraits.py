#!/usr/bin/env python3
#I haven't tested this script because the GFL scraper for my Discord bot has it built in as part of the costume scanning step. So if it doesn't work, file an issue.
import json as JSON
import os
import glob

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def printWarn(text):
	print(bcolors.WARNING + text + bcolors.ENDC)
	
def printError(text):
	print(bcolors.FAIL + text + bcolors.ENDC)
	
def printOK(text):
	print(bcolors.OKGREEN + text + bcolors.ENDC)

with open('girlsfrontline.json','r') as gfld:
	for doll in JSON.loads(gfld.read()):
		for costumeFile in glob.glob("pic/pic_"+doll['internalName']+"_*"):
			fParams = costumeFile.split("_")
			fNameNoDir = costumeFile.split("/")[-1]
			if fParams[-1] == "N.png" or fParams[-1] == "D.png" or fParams[-1] == "M.png":
				continue
			elif fParams[-1] == "Boss.png":
				continue
			elif fParams[-1] == "hallo.png":
				continue
			elif len(fParams) == 2 or fParams[-1] == "elfeldt.png" or fParams[-1] == "Noel.png":
				continue
			elif len(fParams) == 3:
				costumeName = fParams[-1][:-4]
				try:
					int(costumeName)
					if not os.path.exists('pic/'+fNameNoDir[:-4]+"_D.png"):
						printError("No damage art found, not a costume! "+fNameNoDir[:-4]+"_D.png")
						raise Exception
				except:
					printWarn("Moving file into special folder because it doesn't seem to be a costume: "+fNameNoDir)
					if os.path.exists('pic/special/'+fNameNoDir):
						printWarn("File already exists, deleting it.")
						os.remove(costumeFile)
					else:
						os.rename(costumeFile,'pic/special/'+fNameNoDir)

for img in os.listdir("pic"):
	if img.endswith('_SS.png') or img.endswith('_LL.png') or img.endswith('_SS_1.png'):
		printWarn("Moving SF capture image into Sangvis folder: "+img)
		if os.path.exists('pic/Sangvis/'+img):
			printWarn("File already exists, deleting it.")
			os.remove('pic/'+img)
		else:
			os.rename('pic/'+img,'pic/Sangvis/'+img)
	elif '(' in img and ')' in img:
		printWarn("Moving special portrait: "+img)
		if os.path.exists('pic/special/'+img):
			printWarn("File already exists, deleting it.")
			os.remove('pic/'+img)
		else:
			os.rename('pic/'+img,'pic/special/'+img)
