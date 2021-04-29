#!/usr/bin/env python3
import json as JSON
import os
import glob
import sys

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

with open('portraitInformation.json','r') as f:
	portraits = JSON.loads(f.read())
with open('chapterDatabase.json','r') as f:
	j = JSON.loads(f.read())
	chapters = j['story']
	backgrounds = j['bg']

def getCharsFromLine(cmds):
	foundPortraits = []
	for j in range(5):
		charTagEnd = cmds.find(")");
		if charTagEnd != -1:
			#It's +1 to get rid of the ;
			charTagStart = max(cmds.rfind(";",0,charTagEnd)+1,0)
			try:
				charID,charSpr = cmds[charTagStart:charTagEnd].split("(")
				if charID != "" and charSpr != "" and '<' not in charID:
					charSpr=int(charSpr)
					cmds= cmds[:0]+cmds[charTagEnd+1:]
					foundPortraits.append((charID, charSpr))
			except Exception as e:
				break
		else:
			break
	return foundPortraits
	
def getFromTag(s,tag):
	beginTag = "<"+tag+">"
	endTag = "</"+tag+">"
	n = s.find(beginTag)
	if n != -1:
		return s[n+len(beginTag):s.find(endTag)]
	return None

missingPortraitFiles = []
missingPortraitsDB = {}
def appendToMissingPortraits(section,epName,fileName):
	if section not in missingPortraitsDB:
		missingPortraitsDB[section] = {}
	if epName not in missingPortraitsDB[section]:
		missingPortraitsDB[section][epName] = fileName


for section in chapters:
	#print(section)
	for chapter in chapters[section]:
		#print(chapter)
		for episode in chapter['episodes']:
			#print(episode)
			#sys.exit(0)
			for part in episode['parts']:
				fName = '../avgtxt/'+part
				if os.path.isfile(fName):
					#print(fName)
					with open(fName,'r') as partText:
						for line in partText.readlines():
							cmds = line.replace("：",':').split(':')[0]
							foundPortraits = getCharsFromLine(cmds)
							for p in foundPortraits:
								#if '<' in p[0]:
								#	printWarn("Ignoring mistyped portrait: "+str(p)+ " "+fName+" "+chapter['name']+ " - " + episode['name'])
								#	continue
								#If portrait with that ID is not registered
								#Or portrait is registered but type is greater than registered
								if p[0] not in portraits or p[1] > len(portraits[p[0]])-1 or portraits[p[0]][p[1]] == None:
									if fName not in missingPortraitFiles:
										missingPortraitFiles.append(fName)
										if section == "main":
											appendToMissingPortraits(section,episode['name'],part)
										else:
											appendToMissingPortraits(section,chapter['name']+ " - " + episode['name'],part)
										#print("Portrait "+str(p)+" missing in "+fName+ " "+ chapter['name']+" - "+episode['name'])
										print("Missing portrait {:<30} from {:<35}".format(str(p),fName)+chapter['name']+" - "+episode['name'])

for doll in portraits:
	#print(portraits[doll])
	for variant in portraits[doll]:
		if variant is not None:
			if not os.path.isfile("../pic/"+variant):
				printError("File "+variant+" missing from folder!!")

missingBGs = {}
for i in range(len(backgrounds)):
	bg = backgrounds[i]
	fName = '../avgtexture/'+bg+'.png'
	if not os.path.isfile(fName):
		missingBGs[i]=bg

#Same dumb shit as last time...
if len(missingBGs) > 0:
	for section in chapters:
		for chapter in chapters[section]:
			for episode in chapter['episodes']:
				for part in episode['parts']:
					fName = '../avgtxt/'+part
					if os.path.isfile(fName):
						with open(fName,'r') as partText:
							for line in partText.readlines():
								cmds = line.replace("：",':').split(':')[0]
								t = getFromTag(cmds,"BIN")
								if t and int(t) in missingBGs:
										printError("Missing background {:<30} from {:<35}".format(missingBGs[int(t)],fName)+chapter['name']+" - "+episode['name'])

#print(missingPortraits)
#Now go through all of them and convert them to routing strings since it's what the interpreter takes
def getRoutingString(section,fName):
	for i in range(len(chapters[section])):
		for j in range(len(chapters[section][i]['episodes'])):
			for part in chapters[section][i]['episodes'][j]['parts']:
				if fName==part:
					return section+'-'+str(i)+'-'+str(j)
	raise Exception("Part not found in DB.")
	
for section in missingPortraitsDB:
	for episode in missingPortraitsDB[section]:
		missingPortraitsDB[section][episode]=getRoutingString(section,missingPortraitsDB[section][episode])

with open('missingPortraits.json','wb') as file:
	j = JSON.dumps(missingPortraitsDB, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
	file.write(j)
				#sys.exit(0)

