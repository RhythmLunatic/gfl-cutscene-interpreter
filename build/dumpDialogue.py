#!/usr/bin/env python3
import json
import os

"""
WHAT THIS DOES:
Give it chapterDatabase.json and it will take all the files and output dialogue in a folder named 'outTxt' without any codes

This script will assume avgtxt/ is in the same location as chapterDatabase.json.

"""

def getFromTag(s,tag):
	beginTag = "<"+tag+">"
	endTag = "</"+tag+">"
	n = s.find(beginTag)
	if n != -1:
		return s[n+len(beginTag):s.find(endTag)]
	return None


arr = ['/media/LocalHDD/Programming/Projects/HTML/GFL VN Interpreter/avgtxt/-1-1-1.txt']
database = None
with open('../chapterDatabase.json','r') as f:
	database = json.load(f)['story']

for t in database: #main, side, etc
	for ep in database[t]:
		for ep in ep['episodes']:
			fullEpText = ''
			for part in ep['parts']:
				fName = '../avgtxt/'+part
				if not os.path.isfile(fName):
					continue
				with open(fName,'r') as f:
					for line in f.readlines():
						cmds,text = line.replace("：",':').replace("；",";").split(':',1)
						
						fullEpText+=text.replace('+',' ')
						continue
						
						speakerRes = getFromTag(cmds,"Speaker")
						s = ""
						if speakerRes != None:
							s+=speakerRes+": "
							pass
							
						s+=text
						#print(str(len(s.split(' '))))
						print(s, end='')
			print('{:<30} {:<30}'.format(ep['name'],str(len(fullEpText.split(' ')))))
