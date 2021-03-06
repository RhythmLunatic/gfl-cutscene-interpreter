#!/usr/bin/env python3
import os
import json as JSON
from collections import OrderedDict
import re

#One day I will make this an import I swear
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

#https://stackoverflow.com/a/28777781
def write_roman(num):

	roman = OrderedDict()
	roman[1000] = "M"
	roman[900] = "CM"
	roman[500] = "D"
	roman[400] = "CD"
	roman[100] = "C"
	roman[90] = "XC"
	roman[50] = "L"
	roman[40] = "XL"
	roman[10] = "X"
	roman[9] = "IX"
	roman[5] = "V"
	roman[4] = "IV"
	roman[1] = "I"

	def roman_num(num):
		for r in roman.keys():
			x, y = divmod(num, r)
			yield roman[r] * x
			num -= (r * x)
			if num <= 0:
				break

	return "".join([a for a in roman_num(num)])


#
def tryint(s):
	try:
		return int(s)
	except:
		return s
		
def sortMixedList(k):
	try:
		return int(k)
	except:
		return 999

#https://stackoverflow.com/a/4623518
def alphanum_key(s):
	""" Turn a string into a list of string and number chunks.
		"z23a" -> ["z", 23, "a"]
	"""
	return [ tryint(c) for c in re.split('([0-9]+)', s) ]


def extendListIfTooShort(l,idx):
	diff_len=idx-len(l)
	if diff_len > 0:
		l=l+[None]*diff_len
	return l
	
def insertIntoListAt(l,idx,element):
	l=extendListIfTooShort(l,idx+1)
	l[idx]=element
	return l


files = os.listdir('../avgtxt')

def appendFromij(i,j,name,letter,isNight=False):
	ep = {
		#ex. Normal 1-6 -> [1-6-1.txt, 1-6-2.txt]
		'name':  name+' '+str(i)+'-'+str(j),
		'parts': [str(i)+'-'+str(j)+'-1'+letter+'.txt',
				str(i)+'-'+str(j)+'-2'+letter+'.txt']
	}
	#Workaround for episode 13... I don't really feel like adding an altMode=true
	if i == 13 and letter == '':
		ep['parts'] = [
			str(i)+'-'+str(j)+'-1First'+letter+'.txt',
			str(i)+'-'+str(j)+'-2End'+letter+'.txt'
		]
	
	#Account for mid-stage dialogue. Order doesn't really matter anyways.
	for p in range(3,6):
		matchString = str(i)+'-'+str(j)+'-'+str(p)+letter+'-'
		match = [file for file in files if file.startswith(matchString)]
		if match:
			printOK("Picked up mid-stage parts "+str(match)+' matched to '+matchString)
			for e in match:
				ep['parts'].insert(1,e)
				if 'part_names' not in ep:
					ep['part_names'] = [None]*len(ep['parts'])
				ep['part_names'].insert(1,'Mid-stage dialogue')
	
	if isNight:
		ep['night']=[isNight]*len(ep['parts'])
	return ep

def getAllByPrefix(files,prefix,episodeName):
	episodes = []
	#Some episodes start at 0 instead of 1. Manually search for them.
	startedAtZero=False
	prefixed = [filename for filename in files if filename.startswith(prefix+'-0')]
	if prefixed:
		startedAtZero=True
		episodes.append({'name':episodeName,'parts':prefixed})
	
	#Search normally for 1 onwards
	i=1
	while True:
		prefixed = [filename for filename in files if filename.startswith(prefix+'-'+str(i))]
		if prefixed:
			episodes.append({'name':episodeName + ' '+write_roman(i+1 if startedAtZero else i),'parts':prefixed})
			i=i+1
		else:
			return episodes
			
#Don't assume second is number
def getAllByPrefix2(files,prefix,episodeName = None):
	prefixed = [filename for filename in files if filename.startswith(prefix)]
	chNames = {}
	for part in prefixed:
		c = part[1:].split('-')[1]
		if c in chNames:
			chNames[c].append(part)
		else:
			chNames[c] = [part]
	chapters = []
	sortedNames = list(chNames.keys())
	sortedNames.sort(key=sortMixedList)
	#print(sortedNames)
	for chapter in sortedNames:
		chapters.append({'name':chapter,'parts':chNames[chapter],'part_names':chNames[chapter]})
	return chapters
	

#with open('mission_group_info.json','r') as f:
#	MissionGroupInfo=JSON.loads(f.read())
#with open('mission.json','r') as f:
#	MissionLocalizationData = JSON.loads(f.read())

with open('NormalActivityCampaign.txt','r') as f:
	evStoryInformation = f.readlines()
evStoryInformation = evStoryInformation[1:]
js = {'main':[],'event':[],'side':[],'crossover':[]}


#Special for chapter 0
chapterZero = []
for j in range(1,5):
	chapterZero.append(appendFromij(0,j,"Normal",''))
#print(chapterZero)
chapterZero[1]['parts'].append('0-2-3Round2.txt')
chapterZero[1]['part_names']=[None,None,"Unused part? (Not viewable in index, does not seem to match story)"]
#print(chapterZero)
js['main'].append({'name':"Chapter 0",'episodes':chapterZero});

#Normal chapters
for i in range(1,14):
	curChapter = []
	for j in range(1,7):
		curChapter.append(appendFromij(i,j,"Normal",''))
	for j in range(1,5):
		curChapter.append(appendFromij(i,j,"Emergency",'E'))
	if i < 11: #No midnight chapters beyond ch11
		for j in range(1,5):
			curChapter.append(appendFromij(i,j,"Midnight",'N',True))
	js['main'].append({'name':'Chapter '+str(i),'episodes':curChapter});


prologue= []
for i in range(12):
	prologue.append({'name':"Start"+str(i),'parts':['startavg/Start'+str(i)+".txt"]});
js['event'].append({'name':"Prologue",'episodes':prologue});

va11 = {'name':"VA-11 HALL-A (WIP)",'episodes':[{
	'name':"Bartending Cutscenes",
	'parts':[]
	}]}
for i in range(8):
	va11['episodes'][0]['parts'].append('va11/VA11_'+str(i+1)+'.txt');
va11['episodes'].extend(getAllByPrefix(files,'-32','???'))

#gsg = {'name':"Gunslinger Girl",'episodes':getAllByPrefix(files,'-38','???')}
#js['crossover'].append(gsg)
js['crossover'].append({
	"name": "Gunslinger Girl",
	"episodes": [
		{
			"name": "Chapter 0: No. 9",
			"parts": [
				"-38-0-1.txt"
			]
		},
		{
			"name": "Chapter 1: Kaleidoscope",
			"parts": [
				"-38-1-1.txt"
			]
		},
		{
			"name": "Chapter 2: New Fork",
			"parts": [
				"-38-2-1.txt",
				"-38-2-2First.txt",
				"-38-2-2Round.txt",
				"-38-2-2End.txt",
				"-38-2-3.txt",
				"-38-2-4First.txt"
			],
			"part_names":[
				None,
				None,
				None,
				None,
				"Twilight Stars"
			]
		},
		{
			"name": "Chapter 3: Full Length Play",
			"parts": [
				"-38-3-1.txt",
				"-38-3-1First.txt",
				
				"-38-3-2Round.txt",
				"-38-3-2End.txt",
				
				"-38-3-3.txt"
			],
			"part_names":[
				"Full Length Play I",
				"Full Length Play I",
				"Interlude",
				"Full Length Play II",
				"Magic of Happiness"
			]
		},
		{
			"name": "Chapter 4",
			"parts": [
				"-38-4-1First.txt",
				"-38-4-1Round.txt",
				"-38-4-1End.txt",
			],
			"part_names":[
				"Honest Pinocchio",
				"Interlude",
				"Promised Dawn"
				
			]
		},
		{
			"name": "Chapter 5",
			"parts": [
				"-38-5-1First.txt",
				"-38-5-1Round.txt",
				"-38-5-1End.txt",
			],
			"part_names": [
				"Garden of Old",
				"Interlude",
				"Hai capito"
			]
		},
		{
			"name": "Chapter 6: That which must be protected",
			"parts": [
				"-38-6-1First.txt",
				"-38-6-1Round.txt",
				"-38-6-1End.txt",
			]
		},
		{
			"name": "Chapter 7: Perfect Harmony",
			"parts": [
				"-38-7-1.txt"
			]
		}
	]
})

js['crossover'].append(va11)


#I think the text files are identical to Operation Cube Plus, so no point in including it. I haven't checked though
#js['event'].append({'name':"CH. 5.5: Operation Cube (OLD)",'episodes':getAllByPrefix(files,'-1','Operation Cube')})

js['event'].append({
	"name": "CH. 5.5: Operation Cube+",
	"episodes": [
		{
			"name": "Operation Cube I",
			"parts": [
				"-6-1-1.txt",
				"-6-1-2First.txt"
			]
		},
		{
			"name": "Operation Cube II",
			"parts": [
				"-6-2-1.txt",
				"-6-2-2First.txt",
				"-6-2-2End.txt",
			]
		},
		{
			"name": "Operation Cube III",
			"parts": [
				"-6-3-1.txt",
				"-6-3-2First.txt",
				"-6-3-2End.txt",
			]
		},
		{
			"name": "Operation Cube IV",
			"parts": [
				"-6-4-1.txt",
				"-6-4-2First.txt",
				"-6-4-2End.txt",
			]
		},
		{
			"name": "Blindfold Theorem I",
			"parts": [
				"-7-1-1.txt",
				#"-7-1-3Round1.txt", #duplicate dialogue
				#"-7-1-4-Point3498.txt", #duplicate dialogue
				"-7-1-3Round2.txt",
				"-7-1-2First.txt",
				"-7-1-2End.txt",
			]
		},
		{
			"name": "Blindfold Theorem II",
			"parts": [
				"-7-2-1.txt",
				#"-7-2-3Round1.txt", #duplicate dialogue
				#"-7-2-3Round2.txt", #duplicate dialogue
				"-7-2-4-Point3342.txt", #not sure if this is supposed to go before or after first
				"-7-2-2First.txt",
				"-7-2-2End.txt",
			]
		},
		{
			"name": "Blindfold Theorem III",
			"parts": [
				"-7-3-1.txt",
				#"-7-3-3Round1.txt", #duplicate dialogue of the end of -7-3-1.txt
				#"-7-3-3Round2.txt", #duplicate part
				"-7-3-2First.txt",
				"-7-3-4-Point3533.txt",
				"-7-3-2End.txt",
			],
			"part_names":[
				None,
				None,
				"Mid-stage dialogue"
			]
		},
		{
			"name": "Blindfold Theorem IV",
			"parts": [
				"-7-4-1.txt",
				"-7-4-2First.txt",
				#"-7-4-3Round1.txt", #duplicate dialogue
				#"-7-4-3Round2.txt", #duplicate part
				"-7-4-4-Point3612.txt",
				"-7-4-2End.txt",
			],
			"part_names":[
				None,
				None,
				"Mid-stage dialogue"
			]
		}
	]
})

js['event'].append({
	"name": "CH. 7.5: Arctic Warfare",
	"episodes": [
		{
			"name": "The Wolves Gather I",
			"parts": [
				"-2-1-1.txt",
				"-2-1-2First.txt",
				"-2-1-4-Point2007.txt",
				"-2-1-4-Point2179.txt",
				"-2-1-4-Point2207.txt",
			]
		},
		{
			"name": "The Wolves Gather II",
			"parts": [
				"-2-2-1.txt",
				"-2-2-2First.txt",
				"-2-2-4-Point2204.txt"
			]
		},
		{
			"name": "The Wolves Gather III",
			"parts": [
				"-2-3-1.txt",
				"-2-3-2First.txt",
				"-2-3-4-Point2058.txt",
				"-2-3-4-Point2215.txt"
			]
		},
		{
			"name": "The Wolves Gather IV",
			"parts": [
				"-2-4-1.txt",
				"-2-4-2First.txt",
				"-2-4-2End.txt"
			]
		},
		{
			"name": "Lighting Curfew I",
			"parts": [
				"-3-1-1.txt",
				"-3-1-2First.txt"
			]
		},
		{
			"name": "Lighting Curfew II",
			"parts": [
				"-3-2-1.txt",
				"-3-2-2First.txt"
			]
		},
		{
			"name": "Lighting Curfew III",
			"parts": [
				"-3-3-1.txt",
				"-3-3-2First.txt"
			]
		},
		{
			"name": "Lighting Curfew IV",
			"parts": [
				"-3-4-1.txt",
				"-3-4-2First.txt",
				"-3-4-2End.txt",
				"-3-4-4-Point2499.txt"
			]
		},
		{
			"name": "Operation Homecoming I",
			"parts": [
				"-4-1-1.txt",
				"-4-1-2First.txt"
			]
		},
		{
			"name": "Operation Homecoming II",
			"parts": [
				"-4-2-1.txt",
				"-4-2-2First.txt"
			]
		},
		{
			"name": "Operation Homecoming III",
			"parts": [
				"-4-3-1.txt",
				"-4-3-2First.txt"
			]
		},
		{
			"name": "Operation Homecoming IV",
			"parts": [
				"-4-4-1.txt",
				"-4-4-2First.txt",
				"-4-4-2End.txt",
			]
		}
	]
})
js['event'].append({
	"name": "CH. 7.5: Hypothermia",
	"episodes": [
		{
			"name": "Into The Rabbit Hole",
			"parts": [
				"-5-1-1.txt",
				"-5-1-3Round10.txt"
			]
		}
	]
})

for line in evStoryInformation:
	args = line.split("|")
	if float(args[2]) == 7.5 or float(args[2]) == 5.5: #These are manually sorted so skip them
		continue
	#print(args)
	chapterName = "CH. "+args[2]+": "+args[3]
	episodeName = args[4]
	filePrefixForChapter = args[0].split(",")
	chapterData = {'name':chapterName}
	episodes = []
	for n in filePrefixForChapter:
		episodes=getAllByPrefix(files,n,episodeName)
	chapterData['episodes'] = episodes
	#if chapterData['episodes'] in j
	
	foundExistingCh = False
	for chapter in js['event']:
		if chapterData['name'] == chapter['name']:
			chapter['episodes'].extend(episodes)
			foundExistingCh=True
			break;
	if not foundExistingCh:
		js['event'].append(chapterData)
#js['crossover'].append({'name':"DJMax Respect",'episodes':getAllByPrefix(files,'-19',"Chapter 1 ")})
#js['crossover'][-1]['episodes'].extend(getAllByPrefix(files,'-20',"Chapter 2"))
#-2 to -7 already indexed
js['crossover'].append({
	'name':"Guilty Gear x BlazBlue: Operation Rabbit Hunt",
	'shortName':'Guilty Gear x BlazBlue',
	'episodes':[
		{
			"name": "Part I",
			"parts": [
				"-8-1-1.txt",
				"-8-1-2First.txt"
			]
		},
		{
			"name": "Part II",
			"parts": [
				"-8-2-1.txt",
				"-8-2-2First.txt",
				"-8-2-2End.txt"
			]
		},
		{
			"name": "Part III",
			"parts": [
				"-8-3-1.txt",
				"-8-3-2First.txt"
			]
		},
		{
			"name": "Part IV",
			"parts": [
				"-8-4-1.txt",
				"-8-4-2First.txt",
				"-8-4-2End.txt"
			]
		}
	]
})
#No -9
js['crossover'].append({
	"name": "Houkai Gakuen 2nd: Only Master (Fantranslated)",
	"shortName":"Houkai Gakuen 2nd (Fantranslated)",
	"episodes": [
		{
			"name": "Stage 1-1: The Breakdown Descends",
			"parts": [
				"-14-1-1.txt",
				"-14-1-4-Point4968.txt",
				"-14-1-2First.txt"
			]
		},
		{
			"name": "Stage 1-2: Curiousity Killed The Cat",
			"parts": [
				"-14-2-1.txt",
				"-14-2-2First.txt"
			]
		},
		{
			"name": "Stage 1-3: Kiana Sorties",
			"parts": [
				"-14-3-1.txt",
				"-14-3-2First.txt"
			]
		},
		{
			"name": "Stage 1-4: Entry Forbidden",
			"parts": [
				"-14-4-1.txt",
				"-14-4-2First.txt",
				"-14-4-2End.txt"
			]
		},
		{
			"name": "Stage 2-1: Inauspicious Lightning",
			"parts": [
				"-15-1-1.txt",
				"-15-1-2First.txt"
			]
		},
		{
			"name": "Stage 2-2: Swelling Desire",
			"parts": [
				"-15-2-1.txt",
				"-15-2-2First.txt",
				"-15-2-2End.txt"
			]
		},
		{
			"name": "Stage 2-3: Resentment",
			"parts": [
				"-15-3-1.txt",
				"-15-3-2First.txt"
			]
		},
		{
			"name": "Stage 2-4: If Only, One Day...",
			"parts": [
				"-15-4-1.txt",
				"-15-4-2First.txt",
				"-15-4-2End.txt"
			]
		}
	]
})

js['crossover'].append({
	"name": "DJMax Respect: Glory Day",
	"episodes": [
		{
			"name": "Stage 1-1: Stalker",
			"parts": [
				"-19-1-1.txt",
				#"-19-1-2First.txt", #duplicate file
				"-19-1-2.txt",
			]
		},
		{
			"name": "Stage 1-2: Heartbeat",
			"parts": [
				"-19-2-1.txt",
				#"-19-2-2First.txt", #duplicate file
				"-19-2-2.txt",
			]
		},
		{
			"name": "Stage 1-3: Waiting For You",
			"parts": [
				"-19-3-1.txt",
				#"-19-3-2First.txt", #duplicate file
				"-19-3-2.txt",
			]
		},
		{
			"name": "Stage 2-1: Sunset Rider",
			"parts": [
				"-20-1-1.txt",
				"-20-1-2First.txt",
			]
		},
		{
			"name": "Stage 2-2: Fate",
			"parts": [
				"-20-2-1.txt",
				"-20-2-2First.txt",
			]
		},
		{
			"name": "Stage 2-3: End of the Moonlight",
			"parts": [
				"-20-3-1.txt",
				"-20-3-2First.txt",
				"-20-3-2End.txt",
			]
		},
		{
			'name':'Stage 1-2 Minigame',
			'parts': [
				"-19-2-4-Point6737.txt",
				"-19-2-4-Point6738.txt",
				"battleavg/-19-2-EGG.txt"
			]
		},
		{
			'name':"Stage 1-3 Minigame",
			"parts": [
				"-19-3-4-Point6750.txt",
				"-19-3-4-Point7023.txt",
				"battleavg/-19-3-EGG.txt"
			]
		},
		{
			'name':"Stage 2-1 Minigame",
			"parts":[
				"-20-1-4-Point6780.txt",
				"-20-1-4-Point7026.txt",
				"battleavg/-20-1-EGG.txt"
			]
		},
		{
			'name':"Stage 2-2 Minigame",
			"parts":[
				"-20-2-4-Point6819.txt",
				"-20-2-4-Point7029.txt",
				"battleavg/-20-2-EGG.txt"
			]
		},
		{
			"name":"Stage 2-3 Minigame",
			"parts": [
				"-20-3-4-Point6845.txt",
				"-20-3-4-Point6846.txt",
				"battleavg/-20-3-EGG.txt"
			]
		}
	]
})
#Nothing from 21 to 23, 24-28 alrady indexed

#js['event'].append({'name':"CH. 11.5: ISOMER (Unsorted)",'episodes':getAllByPrefix(files,'-31','???')})
js['event'].append({
	"name": "CH. 11.5: ISOMER",
	"episodes": [
		{
			"name": "Prologue: Souvenir",
			"parts": [
				"-31-0-1.txt"
			]
		},
		{
			"name": "EP.1 Path I - Illusory Peace",
			"parts": [
				"-31-1A1-1.txt",
				"-31-1A11-1.txt",
				"-31-1A2-1.txt",
				"-31-1A21-1.txt",
				"-31-1A3-1.txt",
				"-31-1A4-1.txt",
				"-31-1A5-1.txt",
			]
		},
		{
			"name": "EP.1 Path II - Cat And Mouse",
			"parts":[
				"-31-1B1-1.txt",
				"-31-1B2-1.txt",
				"-31-1B3-1.txt",
				"-31-1B31-1.txt",
				"-31-1B4-1.txt",
			]
		},
		{
			"name": "EP.1 Path III - Beyond the Border",
			"parts":[
				"-31-1C1-1.txt",
				"-31-1C2-1.txt",
				"-31-1C3-1.txt",
				"-31-1C4-1.txt"
			]
		},
		{
			"name": "EP.2 Path I - Faith of Blood",
			"parts": [
				"-31-2A1-1.txt",
				"-31-2A11-1.txt",
				"-31-2A12-1.txt",
				"-31-2A2-1.txt",
				"-31-2A21-1.txt",
				"-31-2A3-1.txt",
			]
		},
		{
			"name": "EP.2 Path II - Wolf and Owl",
			"parts": [
				"-31-2B1-1.txt",
				"-31-2B11-1.txt",
				"-31-2B2-1.txt",
				"-31-2B3-1.txt",
				"-31-2B4-1.txt",
			]
		},
		{
			"name": "EP.2 Path III - Under the Wall",
			"parts": [
				"-31-2C1-1.txt",
				"-31-2C2-1.txt"
			]
		},
		{
			"name": "EP.3 Path I - Lost Bargaining Chip",
			"parts": [
				"-31-3A1-1.txt",
				"-31-3A2-1.txt",
				"-31-3A3-1.txt",
			]
		},
		{
			"name": "EP.3 Path II - Shark and the Sea",
			"parts": [
				"-31-3B1-1.txt",
				"-31-3B2-1.txt",
				"-31-3B3-1.txt",
				"-31-3B4-1.txt",
				"-31-3B5-1.txt",
				"-31-3B6-1.txt",
				"-31-3B7-1.txt",
			]
		},
		{
			"name": "EP.4 - Above the Hubbub",
			"parts": [
				"-31-3C1-1.txt",
				"-31-3C2-1.txt",
				"-31-3C21-1.txt",
				"-31-3C3-1.txt",
				"-31-3C4-1.txt",
				"-31-3C5-1.txt",
				"-31-3C6-1.txt",
				"-31-3C61-1.txt",
				"-31-3C62-1.txt"
			],
			"mission_id":[
				None,
				None,
				None,
				None,
				None,
				None,
				None,
				None,
				10252
			]
		},
		{
			"name": "Reign of Chaos",
			"parts": [
				"-31-4-1.txt"
			]
		}
	]
})
#-32 is valhalla
#js['event'].append({'name':"CH. 11.75: Shattered Connexion (WIP)",'episodes':getAllByPrefix2(files,'-33','???')})

js['event'].append({
	"name": "CH. 11.75: Shattered Connexion",
	"episodes": [
		{
			"name": "Episode 1: Tallinn",
			"parts": [
				"-33-1-1First.txt",
				"-33-3-1First.txt",
				"-33-4-1First.txt",
				"-33-5-1First.txt",
				"-33-7-1First.txt"
			],
			"part_names": [
				"Quiet Presence",
				"Two Jobs",
				"Tracing the Source",
				"Reunion with Old Friends",
				"Shackled Spirit I"
			]
		},
		{
			"name": "Episode 2: Ghosttown",
			"parts": [
				"-33-9-1First.txt",
				"-33-11-1First.txt",
				"-33-13-1First.txt",
				"-33-15-1First.txt",
				"-33-17-1First.txt"
			],
			"part_names": [
				"Bound Spirit II",
				"Intangible Sigh I",
				"Nameless Exiles I",
				"Nameless Exiles II",
				"Intangible Sigh II"
			]
		},
		{
			"name": "Episode 3: Immolation",
			"parts": [
				"-33-18-1First.txt",
				"-33-43-1First.txt", #Yeah I don't know why either
				"-33-20-1First.txt",
				"-33-22-1First.txt",
				"-33-23-1First.txt",
				"-33-25-1First.txt"
			],
			"part_names": [
				"Fractured Cognition I",
				"Fractured Cognition II",
				"Subsurface Homecoming I",
				"The Unwelcome",
				"Fractured Cognition III",
				"Fractured Cognition IV"
			]
		},
		
		{
			"name": "Episode 4: Connexion",
			"parts": [
				"-33-26-1First.txt",
				"-33-27-1First.txt",
				"-33-29-1First.txt",
				"-33-31-1First.txt",
				"-33-33-1First.txt"
			],
			"part_names": [
				"Infinite Connections",
				"Subsurface Homecoming II",
				"Isomer I",
				"Subsurface Homecoming III",
				"Isomer II"
			]
		},
		{
			"name": "Episode 5: Queen of the Night",
			"parts": [
				"-33-35-1First.txt",
				"-33-37-1First.txt",
				"-33-40-1First.txt",
				"-33-42-1First.txt",
				"-33-45-1First.txt", 
				"-33-46-1First.txt", #Not sure when this is used. Maybe after battle dialogue? Mission data says there's Combat I and Combat II so I guess this is a two part mission or something
				"-33-48-1First.txt" 
			],
			"part_names": [
				"A Rock and a Hard Place",
				"Operation Defang I",
				"Operation Defang II",
				"All-Devouring Sea of Flowers",
				"Farewell, Tallinn I - Combat I",
				"Farewell, Tallinn I - Combat II",
				"Farewell, Tallinn II"
			]
		},
		{
			"name": "Episode 5.5: Flowers of the End",
			"parts":[
				"-33-49-1First.txt"
			]
		},
		{
			"name":"Episode 6: Confidential Information",
			"parts":[
				"-33-73-1First.txt",
				"-33-74-1First.txt",
				"-33-75-1First.txt",
				"-33-76-1First.txt",
				"-33-77-1First.txt",
				"-33-78-1First.txt",
				"-33-79-1First.txt",
				"-33-80-1First.txt",
				"-33-81-1First.txt",
				"-33-82-1First.txt",
				"-33-83-1First.txt",
				"-33-84-1First.txt",
				"-33-85-1First.txt",
				"-33-86-1First.txt",
				"-33-87-1First.txt"
			
			]
		},
		{
			"name": "Ranking Map Tips",
			"parts": [
				"-33-51-4-Point13117.txt",
				"-33-52-4-Point13142.txt",
				"-33-59-4-Point13290.txt",
				"-33-59-4-Point80174.txt",
				"-33-62-4-Point13467.txt",
				"-33-72-4-Point13325.txt",
				"-33-72-4-Point83325.txt"
			],
		}
	]
})


js['side'].append({'name':"Halloween 2019",'episodes':getAllByPrefix(files,'-34','Episode')})
js['side'].append({
	"name": "Christmas 2019",
	"episodes": [
		{
			"name": "Episode I",
			"parts": [
				"-35-1-1First.txt",
				"-35-1-2End.txt"
			]
		},
		{
			"name": "Episode II",
			"parts": [
				"-35-2-1First.txt",
				"-35-2-2End.txt"
			]
		},
		{
			"name": "Episode III",
			"parts": [
				"-35-3-1First.txt",
				"-35-3-2End.txt",
			]
		},
		{
			"name": "Episode IV",
			"parts": [
				"-35-4-1First.txt",
				"-35-4-2End.txt"
			]
		}
	]
})
#js['side'].append({'name':"Christmas 2019",'episodes':getAllByPrefix(files,'-35','Episode')})
#js['event'].append({'name':"Polarized Light (Untranslated)",'episodes':getAllByPrefix(files,'-36','???')})
js['event'].append({
	"name": "CH 12.5: Polarized Light",
	"episodes": [
		{
			"name": "Chapter 1: Unpolarized Light Source",
			"parts": [
				"-36-1-1.txt",
				"-36-1-2.txt",
				"-36-1-3.txt",
				"-36-1-4.txt", #Side 404
				"-36-1-5.txt",
				"-36-1-6.txt", #Side 404
				"-36-1-7.txt",
				"-36-1-8.txt",
				"-36-1-9.txt",
				"-36-1-10.txt",
			],
			"part_names":[
				"Lamp Starter",
				"Propigation",
				"Refraction Point",
				"Critical Angle",
				"Reflector",
				"Critical Angle Pt.2",
				"Total Internal Reflection",
				"Sine Curve",
				"Reversibility",
				"Cosine Signal"
			]
		},
		{
			"name": "Chapter 2: Bifocal Prism",
			"parts": [
				"-36-2-1.txt",
				"-36-2-2.txt",
				"-36-2-3.txt",
				"-36-2-4.txt",
				"-36-2-5.txt",
				"-36-2-6.txt",
				"-36-2-7.txt",
				"-36-2-8.txt",
				"-36-2-9.txt",
				"-36-2-10.txt",
			],
			"part_names":[
				"Polarizer",
				"Diffraction Grating",
				"Waveguide",
				"Beam Splitter",
				"Interferometer",
				"Aperture",
				"Vacuum Tube",
				"Accelerator",
				"Spectrometer",
				"Analyzer"
			]
		},
		{
			"name": "Chapter 3: Polarized",
			"parts": [
				"-36-3-1.txt",
				"-36-3-2.txt",
				"-36-3-3.txt",
				"-36-3-4.txt",
				"-36-3-5.txt",
				"-36-3-6.txt",
				"-36-3-7.txt",
				"-36-3-8.txt",
				#"-36-3-12-Point90429.txt", #Ranking map junk
				#"-36-3-14-Point90521.txt",
				#"-36-3-16-Point90564.txt",
				#"-36-3-30-Point90663.txt",
				#"-36-3-30-Point90687.txt",
				#"-36-3-38-Point90883.txt",
			],
			'part_names':[
				'Enantiometer Overload I',
				'Enantiometer Overload II',
				"Recrystalization Resolution I",
				"Shattered Plane of Polarization I",
				"Recrystalization Resolution II",
				"Shattered Plane of Polarization II",
				"Asymmetric Induction I",
				"Optical Isomer"
			]
		},
		{
			"name": "Chapter 4: Crystal Recasting",
			"parts": [
				"-36-4-1.txt",
				"-36-4-2.txt",
				"-36-4-3.txt",
				"-36-4-4.txt",
				"-36-4-5.txt",
				"-36-4-6.txt",
				"-36-4-7.txt",
				"-36-4-8.txt",
				"-36-4-9.txt",
				"-36-4-10.txt",
				"-36-4-11.txt",
				"-36-4-12.txt",
				"-36-4-13.txt",
				#"-36-4-27-Point91119.txt",
			],
			'part_names':[
				"Milling",
				"Mixing",
				"Pre-Heating",
				"Sintering",
				"Foaming",
				"Foam Stabilization",
				"Molding",
				"Annealing",
				"Tempering",
				"Cutting",
				"Polishing",
				"Silvering",
				"Virtual Image Reforging"
			]
		},
		{
			"name": "Chapter 5",
			"parts": [
				"-36-5-1.txt", #It's out of order for some reason..
				"-36-5-4.txt",
				"-36-5-2.txt",
				"-36-5-3.txt",
				"-36-5-5.txt",
				"-36-5-6First.txt",
				"-36-5-6End.txt",
				#"-36-5-EX.txt" #Ranking stuff
			],
			"part_names":[
				"Unfathomable Singularity",
				"Casuality Separating Plane",
				"Observable Limits",
				None,
				"Blackbody Radiation"
			],
			"mission_id":[
				None,
				None,
				None,
				None,
				None,
				None,
				10473 #Required for credits sequence to work
			]
		}
	]
})
js['side'].append({
	'name':"White Day 2020: The Photo Studio Mystery",
	'shortName':"White Day 2020",
	'episodes':[
		{
			"name": "Episode I: Rumors of the Haunted Mansion",
			"parts": [
				"-37-1-1.txt"
			]
		},
		{
			"name": "Episode II: The Empty House",
			"parts": [
				"-37-2-1.txt"
			]
		},
		{
			"name": "Episode III: The Griffin Builder",
			"parts": [
				"-37-3-1First.txt",
				"-37-3-4-Point70626.txt", #I know it's strange, but these are during the stage
				"-37-3-4-Point70633.txt",
				"-37-3-2End.txt",
			]
		},
		{
			"name": "Episode IV: The Missing MDR",
			"parts": [
				"-37-4-1.txt",
				"-37-4-4-Point70712.txt"
			]
		},
		{
			"name": "Episode V: The Crooked Man",
			"parts": [
				"-37-5-1First.txt",
				"-37-5-2End.txt"
			]
		},
		{
			"name": "Episode VI: The Seven Tangerine Pips",
			"parts": [
				"-37-6-1.txt",
				"-37-6-4-Point70901.txt",
				"-37-6-4-Point70905.txt",
				"-37-6-4-Point70906.txt",
				"-37-6-4-Point70912.txt",
				"-37-6-4-Point70918.txt",
				"-37-6-4-Point70919.txt",
				"-37-6-4-Point70923.txt",
			]
		},
		{
			"name": "Episode VII: The Second Neural Cloud",
			"parts": [
				"-37-7-1First.txt",
				"-37-7-4-Point71024.txt",
				"-37-7-2End.txt"
			]
		},
		{
			"name": "Episode VIII: Lee Enfield's Last Bow I",
			"parts": [
				"-37-8-1.txt"
			]
		},
		{
			"name": "Episode IX: Lee Enfield's Last Bow II",
			"parts": [
				"-37-9-1.txt"
			]
		}
	]
})
#-38 is gunslinger girl
#-39 is just one dialogue box
js['side'].append({'name':"Summer 2020: Far Side of the Sea",'episodes':getAllByPrefix(files,'-40','Episode')})
js['event'].append({'name':"CH. 13.5: Dual Randomness (Untranslated)",'episodes':getAllByPrefix(files,'-41','???')})
js['side'].append({'name':"Halloween 2020? (Untranslated)",'episodes':getAllByPrefix(files,'-42','???')})
js['crossover'].append({
	"name": "The Division",
	"episodes": [
		{
			"name": "Chapter 0: The Night Before",
			"parts": [
				"-43-0-1.txt"
			]
		},
		{
			"name": "Chapter 1: 0:05 Hudson Refugee Camp",
			"parts": [
				"-43-1-1.txt",
				"-43-1-2.txt",
				"-43-1-3.txt"
			]
		},
		{
			"name": "Chapter 2: 0:07 New York Public Library",
			"parts": [
				"-43-2-1.txt",
				"-43-2-2.txt",
				"-43-2-3.txt",
				"-43-2-4.txt"
			]
		},
		{
			"name": "Chapter 3: 0:23 Grand Central Terminal",
			"parts": [
				"-43-3-1.txt",
				"-43-3-2.txt",
				"-43-3-3.txt"
			]
		},
		{
			"name": "Chapter 4: 0:50 Dark Zone",
			"parts": [
				"-43-4-1.txt",
				"-43-4-2.txt",
				"-43-4-3.txt"
			]
		},
		{
			"name": "Chapter 5: 1:10 Extraction Point",
			"parts": [
				"-43-5-1.txt",
				"-43-5-2.txt"
			]
		},
		{
			"name": "Side Chapter: Squad Am RFB",
			"parts": [
				"-43-A-1.txt"
			],
			"part_names":[
				"Connection Successful"
			]
		},
		{
			"name":"Side Chapter: Squad AK-47",
			"parts":[
				"-43-B-1.txt",
				"-43-B-2.txt",
				"-43-B-3.txt"
			],
			"part_names":[
				"Chug It!",
				"Pickled Cucumber!",
				"Big Ivan!"
			]
		},
		{
			"name": "Side Chapter: Squad Springfield",
			"parts": [
				"-43-C-1.txt",
				"-43-C-2.txt",
				"-43-C-3.txt"
			],
			"part_names":[
				"Stir the Ingredients",
				"Cut and Decorate",
				"Story of Baking"
			]
		},
		{
			"name":"Side Chapter: Squad M870",
			"parts":[
				"-43-D-1.txt",
				"-43-D-2.txt"
			],
			"part_names":[
				"Alcohol Detector",
				"Scales of Justice"
			]
		},
		{
			"name":"Side Chapter: Squad Vector",
			"parts":[
				"-43-E-1.txt",
				"-43-E-2.txt"
			],
			"part_names":[
				"A Small Target",
				"A Large Target"
			]
		},
		{
			"name":"Side Chapter: Squad 404",
			"parts":[
				"-43-F-1.txt",
				"-43-F-2.txt",
				"-43-F-3.txt"
			],
			"part_names":[
				"Hide Behind the Wall!",
				"Hide Behind the Bushes!",
				"Hide Behind the Bug!"
			]
		},
	]
})

js['event'].append({
	'name':"CH. 13.75: Mirror Stage (Untranslated) (Good Luck)",
	'shortName':"CH. 13.75: Mirror Stage",
	'episodes':getAllByPrefix2(files,'-44')
})

fetter = {'name':"Bookshelf of Memories",'episodes':[]}
with open('fetter.json','r') as f:
	fj = JSON.loads(f.read())
	with open('fetter_story.json','r') as f2:
		fj2 = JSON.loads(f2.read())
		for epKey in fj.keys():
			num = int(epKey[8:])
			epName = fj[epKey]
			if not epName:
				epName = "(Untranslated) Event "+str(num)
			#I don't feel like using a lambda
			files = os.listdir('../avgtxt/fetter/'+str(num))
			files.sort(key=alphanum_key)
			ep = {'name':epName,'parts':['fetter/'+str(num)+'/'+file for file in files]}
			
			namedParts = []
			for i in range(len(files)):
				fName = files[i]
				partNameKey = "fetter_story-10000"+fName.split('.')[0]
				#print(partNameKey)
				if partNameKey in fj2 and fj2[partNameKey] != "":
					namedParts=insertIntoListAt(namedParts,i,fj2[partNameKey])
			if namedParts:
				ep['part_names'] = namedParts
					#print(fj2[partNameKey])
			#for partNameKey in fk2.keys():
				#partNum = int(partNameKey[13:])-10000000
			
			fetter['episodes'].append(ep)
		
js['side'].append(fetter)


#TODO: Check for any unknown prefixes

skinStories = []
with open('girlsfrontline.json') as gfld:
	frontlinedex = JSON.loads(gfld.read())
	SkinStoryFiles = os.listdir('../avgtxt/skin')
	#print(SkinStoryFiles)
	for f in SkinStoryFiles:
		for doll in frontlinedex:
			if 'costumes' in doll:
				n = f.split('.')[0]
				for c in doll['costumes']:
					if c['pic'].endswith('_'+n+'.png'):
						skinStories.append({'name':doll['name']+' - '+c['name'],'parts':["skin/"+f]})

#print(skinStories)
skinStories = sorted(skinStories,key=lambda k: k['name'].lower())
js['side'].append({'name':"Skin Stories",'episodes':skinStories})

modStories = []
modStoryFiles = os.listdir('../avgtxt/memoir')
for doll in frontlinedex:
	if doll['num'] and 'mod' not in doll:
		#episodes = []
		parts = sorted(['memoir/'+filename for filename in modStoryFiles if filename.startswith(str(doll['num'])+'_')])
		if parts:
			modStories.append({'name':doll['name'],'parts':parts})

js['side'].append({'name':"MOD 3 Stories",'episodes':modStories})

anniStories = []
anniStoryFiles = os.listdir('../avgtxt/anniversary')
for fName in anniStoryFiles:
	n = int(fName.split('.')[0])
	found = False
	for doll in frontlinedex:
		if doll['num'] == n:
			anniStories.append({'name':doll['name'],'parts':['anniversary/'+fName]})
			found=True
			break
	if not found:
		if n == -1:
			continue
		else:
			printError("Doll with ID "+str(n)+ " missing from database.")
			anniStories.append({'name':"Unknown (ID:"+str(n)+")",'parts':['anniversary/'+fName]})

anniStories = sorted(anniStories,key=lambda k: k['name'].lower())
#Insert at the beginning
anniStories.insert(0,{'name':"Kalina",'parts':['anniversary/-1.txt']})
#anniStories.insert(0,{'name':"All of them at once (AKA crash the server with no survivors)",'parts':[p['parts'][0] for p in anniStories],'part_names':[p['name'] for p in anniStories]})
js['side'].append({'name':"3rd Anniversary",'episodes':anniStories})

#Audit the mod stories... This should be moved somewhere else
dollsWithModStories = []
for f in modStoryFiles:
	tID = int(f.split('_')[0])
	if tID not in dollsWithModStories:
		dollsWithModStories.append(tID)
for tID in dollsWithModStories:
	dexHasMod = False
	for doll in frontlinedex:
		if doll['num'] == tID:
			if 'mod' in doll:
				dexHasMod = True
				break
	if dexHasMod == False:
		for doll in frontlinedex:
			if doll['num'] == tID:
				print('\033[93m'+'T-Doll '+doll['name']+'\'s MOD is missing from girlsfrontline.json.'+'\033[0m')
				break


#This should be last, nobody wants to click on this
js['side'].append({'name':"Interpreter Test Room",'episodes':[{'name':file,'parts':['testroom/'+file]} for file in os.listdir('../avgtxt/testroom')]})

for t in js: #main, side, etc
	for ep in js[t]:
		for ep in ep['episodes']:
			for part in ep['parts']:
				fName = '../avgtxt/'+part
				if not os.path.isfile(fName):
					printError("Hey idiot, "+fName+" doesn't exist, fix the database: " +ep['name'])


musicDB = {}
with open('AudioTemplate.txt','r') as f:
	for line in f.readlines():
		#Skip
		if line.isspace() or line.startswith('//'):
			continue
		if line.startswith('AudioBGM'):
			audioInfo = line.split("|")
			if audioInfo[2].isspace()==False and audioInfo[1] != audioInfo[2]:
				musicDB[audioInfo[1]] = audioInfo[2]

backgrounds = None
with open('profiles.txt','r') as f:
	backgrounds = [line.strip() for line in f.readlines()]



with open('chapterDatabase.json','wb') as f:
	f.write(JSON.dumps({'music':musicDB,'story':js,'bg':backgrounds}, sort_keys=False, indent='\t', separators=(',', ': '), ensure_ascii=False).encode('utf8'))
	print("Generated chapterDatabase.json")



	

