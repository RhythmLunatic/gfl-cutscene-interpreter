#!/usr/bin/env python3
#Take the girlsfrontline.json and gf_flavortext.json from IOP and keep only the relevant data.
#
import json as JSON
import os

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
	
def RepresentsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

class ResizingList(list):
	
	def extendListIfTooShort(self,idx):
		diff_len=idx-len(self)
		if diff_len > 0:
			self+=[None]*diff_len
	
	def __setitem__(self,i,val):
		self.extendListIfTooShort(i+1)
		super(ResizingList,self).__setitem__(i,val)
	
	def quickInsertCostumeAtIdx(self,idx,name):
		#+2 because lists start at 0 but also because we want to add damaged art too
		#extendListIfTooShort(idx+2)
		internalName = self[0].split('_')[1].split('.')[0]
		#print(l)
		self[idx]='pic_'+internalName+'_'+name+'.png'
		self[idx+1]='pic_'+internalName+'_'+name+'_D.png'
		

		
	#def __getitem__(self,i):
	#	return self.l[i]
		#return l

#def quickAppendCostume(name):
#	return ['pic_'+name+'.png','pic_'+name+'_D.png']

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
				portraitDatabase[doll['internalName']] = ResizingList([doll['img']]);
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
															#TODO: Some dolls use multiple sprites in a story (ex. Team DEFY or AR), this will get it wrong if they do
															#Although for those it can probably just be overwritten at the end
															printWarn("Found unknown type "+str(charSpr)+" being used in "+charID)
															#portraitDatabase[doll['internalName']] = extendListIfTooShort(portraitDatabase[doll['internalName']],charSpr+2)
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
												except Exception as e:
													#printError(print(e))
													print(e)
													printError("This line is bugged... Just skipping.")
													printError(line)
											
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
	"special/版娘-8.png",
	None,
	None,
	"special/NPC-Kalin_11.png",
	"special/NPC-Kalin_12.png",
	"special/NPC-Kalin_13.png",
]

portraitDatabase['NPC-Ange'] = ResizingList([
	'NPC-Ange.png',
	'NPC-Ange_1.png',
	None,
	'NPC-Ange(3).png',
	'NPC-Ange(4).png',
	'NPC-Ange(5).png',
	'NPC-Ange(6).png',
	'NPC-Ange(7).png'
])
#portraitDatabase['NPC-Ange'][3] = 'NPC-Ange(3).png'


portraitDatabase['NPC-Persica'] = [
	"pic_NPC-Persica.png",
	None,
	"pic_NPC-Persica_J.png"
]
portraitDatabase["NPC-Helian"]=[
	"pic_NPC-Helian.png",
	"pic_NPC-Helian_A.png"
]
portraitDatabase['NPC-Deele']=[
	"pic_NPC-Deele.png"
]
portraitDatabase['NPC-Seele']=[
	"pic_NPC-Seele.png",
	"pic_NPC-Seele_1.png"
]
portraitDatabase['NPC-Dima']=[
	'NPC-Dima(0).png',
	'NPC-Dima(1).png',
	'NPC-Dima(2).png',
	'NPC-Dima(3).png'
]

portraitDatabase['NPC-Kyruger']=['pic_NPC-Kyruger.png']

portraitDatabase['G11story']=['special/shadow.png','special/shadow.png']
portraitDatabase['Jillmagic']=['pic_Jill_529.png']
portraitDatabase['RO635-NoArmor']=['special/pic_RO635_NoArmor0.png']
#portraitDatabase['BOSS-9']=['pic_BossArchitect_LL.png']
#portraitDatabase['BOSS-12']=['Eliza.png']

portraitDatabase['NytoIsomer'][4]="Nyto_Isomer_Shadow.png"

portraitDatabase['M1903bar']=["special/M1903_Bartender.png"]
portraitDatabase['M1903Cafe']=["special/M1903Cafe.png"]
portraitDatabase['M1903'].quickInsertCostumeAtIdx(8,"1107")

portraitDatabase['HK416'][2] = 'special/pic_HK416_1.png'
portraitDatabase['HK416'][3] = 'special/pic_HK416_2.png'

portraitDatabase['HK416Mod'][2]='special/pic_HK416Mod_1.png'

#M16 has more than two portraits, but this will have to do for now...
portraitDatabase['M16']=portraitDatabase["M16A1"]
portraitDatabase["MK2"]=portraitDatabase['StenMK2']
portraitDatabase['FAL']=portraitDatabase['FNFAL']
portraitDatabase['FAL'][2] = "pic_FNFAL_308.png"
portraitDatabase['FAL'][3] = "pic_FNFAL_308_D.png"

#Yes really
portraitDatabase['PPSh41']=portraitDatabase['PPsh41']
portraitDatabase['m1'] = portraitDatabase['M1']
portraitDatabase['m500'] = portraitDatabase['M500']

portraitDatabase["FAMASHalloween"]=["pic_FAMAS_2604.png"]

portraitDatabase['P7'].quickInsertCostumeAtIdx(2,"1404")
portraitDatabase['KSVK'].quickInsertCostumeAtIdx(4,"3805")
portraitDatabase['Ameli'].quickInsertCostumeAtIdx(2,"1605")
portraitDatabase["Welrod"].quickInsertCostumeAtIdx(4,"1401")
portraitDatabase["Spitfire"].quickInsertCostumeAtIdx(2,"1405")
portraitDatabase['Ithaca37'].quickInsertCostumeAtIdx(2,"1105")
portraitDatabase['95type'].quickInsertCostumeAtIdx(2,"1102")
portraitDatabase['m1'].quickInsertCostumeAtIdx(2,"1106")
portraitDatabase['FN57'].quickInsertCostumeAtIdx(6,"1109")
portraitDatabase['FAL'].quickInsertCostumeAtIdx(4,"2406")
portraitDatabase['KP31'].quickInsertCostumeAtIdx(6,"1103")
portraitDatabase['WA2000'].quickInsertCostumeAtIdx(6,'1108')
portraitDatabase['NTW20'].quickInsertCostumeAtIdx(6,'1101')
portraitDatabase['OC44'].quickInsertCostumeAtIdx(2,'1608')
portraitDatabase['CZ75'].quickInsertCostumeAtIdx(2,'1604')
portraitDatabase['RFB'].quickInsertCostumeAtIdx(2,'1601')

portraitDatabase['G11'].quickInsertCostumeAtIdx(6,'1602')
#This doesn't seem correct...
#portraitDatabase['G11'][1] = 'special/pic_G11_1.png'
#portraitDatabase['G11'][2] = 'special/pic_G11_2.png'
portraitDatabase['G11'][9] = 'special/pic_G11_9.png'

portraitDatabase['UMP9Mod'][4] = 'special/pic_UMP9Mod_angry.png'
portraitDatabase['UMP9Mod'][2] = 'special/pic_UMP9Mod_dislike.png'
portraitDatabase['UMP9Mod'][3] = 'special/pic_UMP9Mod_happy.png'

#portraitDatabase["MDR"].extend(["pic_MDR_2603.png","pic_MDR_2603_D.png"])
#portraitDatabase["BrenMK"].extend(["pic_BrenMK_2605.png","pic_BrenMK_2605_D.png"])
#portraitDatabase["SAT8"].extend(["pic_SAT8_1802.png","pic_SAT8_1802_D.png","pic_SAT8_2601.png","pic_SAT8_2601_D.png"])


#fairies
portraitDatabase['DJMAXSUEE']=['equip/fairy/DJMAXSUEE_1.png']
portraitDatabase['DJMAXPREIYA']=['equip/fairy/DJMAXPREIYA_1.png']
portraitDatabase['DJMAXSEHRA']=['equip/fairy/DJMAXSEHRA_1.png']
portraitDatabase['FairyWarrior']=['equip/fairy/fighting_1.png']

#TODO: This shouldn't be using extend
portraitDatabase['AR15'].extend(["special/AR15_T.png"])
portraitDatabase["M4A1"].extend([None,"special/M4A1_T.png"])

portraitDatabase['missing'] = ['missing.png']


with open('portraitInformation.json','wb') as file:
	j = JSON.dumps(portraitDatabase, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
	file.write(j)


musicDB = """
GF_Title_loop;Title - Y2064
GF_Lobby_New_loop;Main Menu - DAY1
GF_Factory_loop_old;Factory (old) - D.O.L.L
GF_Factory_loop;Factory - X5
GF_Simulation_loop;Simulation - INITIALIZE
GF_MAP1_BGM;MAP1 - SAFETY FIRST.B
GF_MAP2_BGM_0;MAP2 - GREENLIGHT.A
GF_MAP2_BGM_1;MAP2 - GREENLIGHT.B
GF_BOSS_Common;Vs. Boss - Made in Heaven;Boss battle theme
GF_Song;What Am I Fighting For
m_19summer_lobby;Shattered Connexion - Menu
m_19summer_mainenemy_n;Shattered Connexion - Normal Battle;Shattered Connexion normal battle theme
m_19summer_mainenemy_h;Shattered Connexion - Hard Battle;Shattered Connexion hard battle theme
m_19summer_song;Shattered Connexion - Ending Theme "Connexion" (Short cut);Shattered Connexion ending theme
DJMAX_GloryDay;DJMAX - Ending "glory day (Acoustic Ver.)";DJMax Event Ending Theme
DJMAX_BlackCat;DJMAX - Vs. El Fail "Black Cat";DJMax Event vs. FAIL
DJMAX_OBLIVION;DJMAX - OBLIVION
DJMAX_AskToWind;DJMAX - Minigame Song 1 "Ask To Wind"
DJMAX_IWantYou;DJMAX - ??? "I Want You"
m_halloween19_made_in_heaven;Halloween 2019 - Made In Heaven (Chiptune Ver.);Halloween 2019 event battle theme
m_halloween19_host;Halloween 2019 - Menu
"""

