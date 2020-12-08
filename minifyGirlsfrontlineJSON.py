#!/usr/bin/env python3
#Take the girlsfrontline.json and gf_flavortext.json from IOP and keep only the relevant data.
#
import json as JSON
import os

def extendListIfTooShort(l,idx):
	diff_len=idx-len(l)
	if diff_len > 0:
		l=l+[None]*diff_len
	return l
	
def RepresentsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

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
			#This should be moved to a separate loop since we don't want to pollute girlsfrontline-min with portrait IDs but we also need those IDs to correctly search portraits.
			#ex. FNFAL is FAL in the portrait database
			if 'img' in doll:
				portraitDatabase[doll['internalName']] = [doll['img']];
				#if doll['internalName'] == "BrenMK":
				#	print(doll['costumes'])
				if 'costumes' in doll:
					portraitDatabase[doll['internalName']].append(doll['costumes'][1]['pic'])
					#Skip the first two costumes, only check even (non damaged) art
					for i in range(2,len(doll['costumes']),2):
						#print(i)
						#print(doll['costumes'][i]['pic'])
						costumeID = doll['costumes'][i]['pic'].split('_')[-1].split('.')[0]
						#print(costumeID)
						#Ignore non costumes
						if RepresentsInt(costumeID):
							print(costumeID)
							#Search through costume story for an unknown ID for this T-Doll and assume it's the costume
							fPath = "avgtxt/skin/"+ costumeID + ".txt"
							if os.path.isfile(fPath):
								with open(fPath,'r') as costumeStory:
									foundCostume=False
									for line in costumeStory.readlines():
										if foundCostume:
											break
										cmds = line.replace("：",':').split(':')[0]
										#print(cmds)
										for j in range(5):
											charTagEnd = cmds.find(")");
											if charTagEnd != -1:
												#It's +1 to get rid of the ;
												charTagStart = max(cmds.rfind(";",0,charTagEnd)+1,0)
												#print(charTagStart)
												try:
													charID,charSpr = cmds[charTagStart:charTagEnd].split("(")
													if charID != "" and charSpr != "":
														#print(charSpr)
														charSpr=int(charSpr)
														#print(charID)
														#print(charSpr)
														#console.log(charID)
														#console.log(charSpr)
														#Ignore empty sprite IDs, they do nothing.
														if charID == doll['internalName'] and charSpr > 1:
															print("Found unknown type "+str(charSpr)+" being used in "+charID)
															portraitDatabase[doll['internalName']] = extendListIfTooShort(portraitDatabase[doll['internalName']],charSpr+2)
															print(doll['costumes'][i]['pic'])
															print(doll['costumes'][i+1]['pic'])
															portraitDatabase[doll['internalName']][charSpr]=doll['costumes'][i]['pic']
															portraitDatabase[doll['internalName']][charSpr+1]=doll['costumes'][i+1]['pic']
															print("Added to database")
															print(portraitDatabase[doll['internalName']])
															foundCostume=True
															break
													cmds = cmds[:0]+cmds[charTagEnd+1:];
													#print("newCMDS: "+cmds)
												except:
													print("This line is bugged... Just skipping")
											
											else:
											
												#print("No portraits left in this line")
												break;
											
							else:
								print("No costume story? "+costumeID)
							
					
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
portraitDatabase['NPC-Deele']=[
	"pic_NPC-Deele.png"
]
portraitDatabase['NPC-Seele']=[
	"pic_NPC-Seele.png",
	"pic_NPC-Seele_1.png"
]

portraitDatabase['G11story']=['special/shadow.png','special/shadow.png']
portraitDatabase['Jillmagic']=['pic_Jill_529.png']
portraitDatabase['BOSS-9']=['pic_BossArchitect_LL.png']
portraitDatabase['BOSS-12']=['Eliza.png']

portraitDatabase['M1903bar']=["special/M1903_Bartender.png"]
portraitDatabase['M1903Cafe']=["special/M1903Cafe.png"]

portraitDatabase['HK416'][2] = ['special/pic_HK416_1.png']
portraitDatabase['HK416'][3] = ['special/pic_HK416_2.png']

portraitDatabase["MK2"]=portraitDatabase['StenMK2']
portraitDatabase['FAL']=portraitDatabase['FNFAL']

portraitDatabase["FAMASHalloween"]=["pic_FAMAS_2604.png"]

#portraitDatabase["MDR"].extend(["pic_MDR_2603.png","pic_MDR_2603_D.png"])
#portraitDatabase["BrenMK"].extend(["pic_BrenMK_2605.png","pic_BrenMK_2605_D.png"])
#portraitDatabase["SAT8"].extend(["pic_SAT8_1802.png","pic_SAT8_1802_D.png","pic_SAT8_2601.png","pic_SAT8_2601_D.png"])

portraitDatabase['AR15'].extend(["special/AR15_T.png"])
portraitDatabase["M4A1"].extend([None,"special/M4A1_T.png"])
portraitDatabase['missing'] = ['missing.png']

with open('portraitInformation.json','wb') as file:
	j = JSON.dumps(portraitDatabase, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
	file.write(j);
