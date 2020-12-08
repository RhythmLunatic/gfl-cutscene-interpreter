#!/usr/bin/env python3
import os
import json as JSON
from collections import OrderedDict

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

def appendFromij(i,j,name,letter):
	return {
		'name':  name+' '+str(i)+'-'+str(j),
		'parts': [str(i)+'-'+str(j)+'-1'+letter+'.txt',
				str(i)+'-'+str(j)+'-2'+letter+'.txt']
	}

def getAllByPrefix(files,prefix,episodeName):
	episodes = []
	i=1
	while True:
		prefixed = [filename for filename in files if filename.startswith(prefix+'-'+str(i))]
		if prefixed:
			episodes.append({'name':episodeName + ' '+write_roman(i),'parts':prefixed})
			i=i+1
		else:
			return episodes

files = os.listdir('./avgtxt')

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
for j in range(5):
	chapterZero.append(appendFromij(0,j,"Normal",''))
#print(chapterZero)
js['main'].append({'name':"Chapter 0",'episodes':chapterZero});

#Normal chapters
for i in range(1,13):
	curChapter = []
	for j in range(1,7):
		curChapter.append(appendFromij(i,j,"Normal",''))
	for j in range(1,5):
		curChapter.append(appendFromij(i,j,"Emergency",'E'))
	for j in range(1,5):
		curChapter.append(appendFromij(i,j,"Midnight",'N'))
	js['main'].append({'name':'Chapter '+str(i),'episodes':curChapter});


prologue= []
for i in range(12):
	prologue.append({'name':"Start"+str(i),'parts':['startavg/Start'+str(i)+".txt"]});
js['event'].append({'name':"Prologue",'episodes':prologue});

va11 = {'name':"VA-11 HALL-A",'episodes':[{
	'name':"Bartending Cutscenes",
	'parts':[]
	}]}
for i in range(8):
	va11['episodes'][0]['parts'].append('va11/VA11_'+str(i+1)+'.txt');
va11['episodes'].extend(getAllByPrefix(files,'-32','???'))

gsg = {'name':"Gunslinger Girl",'episodes':getAllByPrefix(files,'-38','???')}
js['crossover'].append(gsg)

js['crossover'].append(va11)


for line in evStoryInformation:
	args = line.split("|")
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
js['event'].append({'name':"CH. ??: ISOMER",'episodes':getAllByPrefix(files,'-31','???')})

skinStories = []
with open('girlsfrontline.json') as gfld:
	frontlinedex = JSON.loads(gfld.read())
	SkinStoryFiles = os.listdir('./avgtxt/skin')
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
modStoryFiles = os.listdir('./avgtxt/memoir')
for doll in frontlinedex:
	if doll['num'] and 'mod' not in doll:
		#episodes = []
		parts = sorted(['memoir/'+filename for filename in modStoryFiles if filename.startswith(str(doll['num'])+'_')])
		if parts:
			modStories.append({'name':doll['name'],'parts':parts})
js['side'].append({'name':"MOD 3 Stories",'episodes':modStories})

with open('chapterDatabase.json','wb') as f:
	f.write(JSON.dumps(js, sort_keys=False, indent='\t', separators=(',', ': '), ensure_ascii=False).encode('utf8'))
	
#with open('profiles.txt','r') as backgrounds:
#	print([line.strip() for line in backgrounds.readlines()])
