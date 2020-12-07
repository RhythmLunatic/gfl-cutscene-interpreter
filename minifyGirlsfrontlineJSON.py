#!/usr/bin/env python3
#Take the girlsfrontline.json and gf_flavortext.json from IOP and keep only the relevant data.
#
import json as JSON

newDatabase = []
portraitDatabase = {}
with open('girlsfrontline.json','r') as gfld:
	frontlinedex = JSON.loads(gfld.read())
	with open('gf_flavortext.json','r') as gflb:
		bonusdex = JSON.loads(gflb.read())
		for doll in frontlinedex:
			if doll['name'] in bonusdex:
				if 'alias' in bonusdex[doll['name']]:
					doll['alias'] = bonusdex[doll['name']]['alias']
				'''
				To inject, a lot of checks are needed.
				1. quotes must be loaded.
				2. doll must have a quotes key in the bonusdex.
				3. doll must have its internal name, since the quotedex works by internal names.
				'''
				#if quotedex and 'quotes' in bonusdex[doll['name']] and 'internalName' in doll:
				#	quotedex[doll['internalName']] = bonusdex[doll['name']]['quotes']
	
	for doll in frontlinedex:
		newDoll = {};
		newDoll['name'] = doll['name']
		newDoll['type'] = doll['type']
		newDoll['num'] = doll['num']
		newDoll['rating'] = doll['rating']
		if 'internalName' in doll:
			#Oops, turns out MOD 1 and MOD 2 data was overwriting the portraitDatabase
			if 'mod' in doll and doll['mod'] != 3:
				continue
			newDoll['internalName'] = doll['internalName']
			if 'img' in doll:
				portraitDatabase[doll['internalName']] = [doll['img']];
				#if doll['internalName'] == "BrenMK":
				#	print(doll['costumes'])
				if 'costumes' in doll:
					portraitDatabase[doll['internalName']].append(doll['costumes'][1]['pic'])
					#assert(len(portraitDatabase[doll['internalName']]) > 1)
		#if 'img' in doll:
		#	newDoll['img'] = doll['img']
		#I don't know if this is gonna be needed later
		#if 'costumes' in doll:
			#newDoll['costumes'] = doll['costumes']
		#	newDoll['costumes']
		newDatabase.append(newDoll)

with open('girlsfrontline-min.json','wb') as file:
	j = JSON.dumps(newDatabase, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
	#j = JSON.dumps(newDatabase, sort_keys=False, separators=(',', ':'), ensure_ascii=False).encode('utf8')
	file.write(j)


portraitDatabase["NPC-Kalin"] = [
	"special/版娘.png",
	"special/版娘-1.png",
	"special/版娘-2.png",
	"special/版娘-3.png",
	"special/版娘-4.png",
	"special/版娘-5.png",
	"special/版娘-6.png",
	"special/版娘-7.png",
	"special/版娘-8.png"
]
portraitDatabase['NPC-Persica'] = [
	"pic_NPC-Persica.png",
	None,
	"pic_NPC-Persica_J.png"
]
portraitDatabase["NPC-Helian"]=[
	"pic_NPC-Helian.png"
]
portraitDatabase["MK2"]=[
	"pic_StenMK2.png"
]
portraitDatabase["FAMASHalloween"]=[
	"pic_FAMAS_2604.png"
]
portraitDatabase["MDR"].extend(["pic_MDR_2603.png","pic_MDR_2603_D.png"])
portraitDatabase["BrenMK"].extend(["pic_BrenMK_2605.png","pic_BrenMK_2605_D.png"])
portraitDatabase["SAT8"].extend(["pic_SAT8_1802.png","pic_SAT8_1802_D.png","pic_SAT8_2601.png","pic_SAT8_2601_D.png"])

portraitDatabase['AR15'].extend(["special/AR15_T.png"])
portraitDatabase["M4A1"].extend([None,"special/M4A1_T.png"])

with open('portraitInformation.json','wb') as file:
	j = JSON.dumps(portraitDatabase, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
	file.write(j);
