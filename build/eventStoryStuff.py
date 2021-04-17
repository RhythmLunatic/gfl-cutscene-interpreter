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

def appendFromij(i,j,name,letter,isNight=False):
	return {
		'name':  name+' '+str(i)+'-'+str(j),
		'parts': [str(i)+'-'+str(j)+'-1'+letter+'.txt',
				str(i)+'-'+str(j)+'-2'+letter+'.txt'],
		'night':[isNight,isNight]
	}

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
	

files = os.listdir('../avgtxt')

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
chapterZero[2]['parts'].append('0-2-3Round2.txt')
#print(chapterZero)
js['main'].append({'name':"Chapter 0",'episodes':chapterZero});

#Normal chapters
for i in range(1,13):
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
	if float(args[2]) == 7.5: #If Arctic Warfare, do a special case since the secret mission is a separate entry... It's like this on the index too
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
'''
{
	"name": "Waste",
	"parts": [
		"-24-2-1.txt",
		"-24-2-2.txt"
	]
},
'''
#js['crossover'].append({'name':"DJMax Respect",'episodes':getAllByPrefix(files,'-19',"Chapter 1 ")})
#js['crossover'][-1]['episodes'].extend(getAllByPrefix(files,'-20',"Chapter 2"))
#-2 to -7 already indexed
js['crossover'].append({
	'name':"Guilty Gear x BlazBlue: Operation Rabbit Hunt",
	'shortName':'Guilty Gear x BlazBlue',
	'episodes':getAllByPrefix(files,'-8','Part')
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
	"name": "DJMax Respect",
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
			"name":"Bonus Cutscenes During Stages",
			"parts": [
				"-19-2-4-Point6737.txt",
				"-19-2-4-Point6738.txt",
				"-19-3-4-Point6750.txt",
				"-19-3-4-Point7023.txt",
				"-20-1-4-Point6780.txt",
				"-20-1-4-Point7026.txt",
				"-20-2-4-Point6819.txt",
				"-20-2-4-Point7029.txt",
				"-20-3-4-Point6845.txt",
				"-20-3-4-Point6846.txt"
			]
		}
	]
})
#Nothing from 21 to 23, 24-28 alrady indexed

js['event'].append({'name':"CH. ??: ISOMER (Unsorted)",'episodes':getAllByPrefix(files,'-31','???')})
#-32 is valhalla
js['event'].append({'name':"CH. ??: Shattered Connexion (WIP)",'episodes':getAllByPrefix2(files,'-33','???')})
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
	"name": "Polarized Light (Untranslated)",
	"episodes": [
		{
			"name": "Chapter I",
			"parts": [
				"-36-1-1.txt",
				"-36-1-2.txt",
				"-36-1-3.txt",
				"-36-1-4.txt",
				"-36-1-5.txt",
				"-36-1-6.txt",
				"-36-1-7.txt",
				"-36-1-8.txt",
				"-36-1-9.txt",
				"-36-1-10.txt",
			]
		},
		{
			"name": "Chapter II",
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
			]
		},
		{
			"name": "Chapter III",
			"parts": [
				"-36-3-1.txt",
				"-36-3-2.txt",
				"-36-3-3.txt",
				"-36-3-4.txt",
				"-36-3-5.txt",
				"-36-3-6.txt",
				"-36-3-7.txt",
				"-36-3-8.txt",
				"-36-3-12-Point90429.txt",
				"-36-3-14-Point90521.txt",
				"-36-3-16-Point90564.txt",
				"-36-3-30-Point90663.txt",
				"-36-3-30-Point90687.txt",
				"-36-3-38-Point90883.txt",
			]
		},
		{
			"name": "Chapter IV",
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
				"-36-4-27-Point91119.txt",
			]
		},
		{
			"name": "Chapter V",
			"parts": [
				"-36-5-1.txt",
				"-36-5-2.txt",
				"-36-5-3.txt",
				"-36-5-4.txt",
				"-36-5-5.txt",
				"-36-5-6First.txt",
				"-36-5-6End.txt",
				"-36-5-EX.txt"
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
js['event'].append({'name':"Dual Randomness (Untranslated)",'episodes':getAllByPrefix(files,'-41','???')})
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

js['event'].append({'name':"Mirror Stage (Untranslated) (Good Luck)",'episodes':getAllByPrefix2(files,'-44')})

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
skinStories = sorted(skinStories,key=lambda k: k['name'])
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



	

