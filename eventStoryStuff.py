#!/usr/bin/env python3
import os
import json as JSON

evStoryInformation = """-1|Operation Cube|EP.|5.5
-2,-3,-4,-5|Arctic Warfare|EP.|7.5
-7|Operation Cube+|EP.|7.75
-10,-11,-12,-13|Deep Dive|EP.|8.5
-16,-17,-18|Singularity|EP.|10.5
-24,-25,-26,-28|Continuum Turbulence|EP.|10.75"""
files = os.listdir('./avgtxt')

j = []

for line in evStoryInformation.splitlines():
	args = line.split("|",1)
	#print(args)
	chapterName = args[1]
	filePrefixForChapter = args[0].split(",")
	chapterData = {'name':chapterName}
	episodes = []
	for n in filePrefixForChapter:
		i=1
		while True:
			prefixed = [filename for filename in files if filename.startswith(n+'-'+str(i))]
			if prefixed:
				episodes.append({'name':n+'-'+str(i),'parts':prefixed})
				i=i+1
			else:
				break
	chapterData['episodes'] = episodes
	j.append(chapterData)
	
with open('tmp.json','wb') as f:
	f.write(JSON.dumps(j, sort_keys=False, indent='\t', separators=(',', ': '), ensure_ascii=False).encode('utf8'))


#{name:knownFiles[i],parts:['skin/'+knownFiles[i]]}
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
with open('tmp2.json','wb') as f:
	f.write(JSON.dumps(skinStories, sort_keys=False, indent='\t', separators=(',', ': '), ensure_ascii=False).encode('utf8'))

