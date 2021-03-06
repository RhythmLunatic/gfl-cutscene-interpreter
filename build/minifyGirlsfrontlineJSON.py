#!/usr/bin/env python3
#Take the girlsfrontline.json and gf_flavortext.json from IOP and keep only the relevant data.
#
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
	
def RepresentsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False
		
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

class ResizingList(list):
	
	def extendListIfTooShort(self,idx):
		diff_len=idx-len(self)
		if diff_len > 0:
			self+=[None]*diff_len
			
	def getInternalName(self):
		return self[0].split('_')[1].split('.')[0]
	
	def __setitem__(self,i,val):
		self.extendListIfTooShort(i+1)
		super(ResizingList,self).__setitem__(i,val)
	
	def quickInsertCostumeAtIdx(self,idx,name):
		#+2 because lists start at 0 but also because we want to add damaged art too
		#extendListIfTooShort(idx+2)
		internalName = self.getInternalName()
		#print(l)
		self[idx]='pic_'+internalName+'_'+name+'.png'
		self[idx+1]='pic_'+internalName+'_'+name+'_D.png'
		
	def quickInsertSpecial(self,idx):
		internalName = self.getInternalName()
		self[idx]='special/pic_'+internalName+'_'+str(idx)+'.png'
		
	def fillSpecial(self,name,begin,end):
		#internalName = self.getInternalName()
		for i in range(begin,end):
			self[i]='special/'+name+'('+str(i)+').png'
			
	def fillSpecial2(self,name,begin,end,isSpecial):
		if isSpecial:
			for i in range(begin,end):
				self[i]='special/'+name+'_'+str(i)+'.png'
		else:
			for i in range(begin,end):
				self[i]=name+'_'+str(i)+'.png'

def quickGenerateNPC(name,upToIdxInclusive,isSpecial=True,altMode=False):
	l = ResizingList([])
	if altMode:
		l.fillSpecial2(name,0,upToIdxInclusive+1,isSpecial)
	else:
		l.fillSpecial(name,0,upToIdxInclusive+1)
	return l

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
							#print(costumeID)
							#Search through costume story for an unknown ID for this T-Doll and assume it's the costume
							fPath = "../avgtxt/skin/"+ costumeID + ".txt"
							if os.path.isfile(fPath):
								with open(fPath,'r') as costumeStory:
									foundCostume=False
									for line in costumeStory.readlines():
										if foundCostume:
											break
										cmds = line.replace("：",':').replace('；',';').split(':')[0]
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
															print("Found unknown type "+str(charSpr)+" being used in "+charID)
															#portraitDatabase[doll['internalName']] = extendListIfTooShort(portraitDatabase[doll['internalName']],charSpr+2)
															print(doll['costumes'][i]['pic'])
															print(doll['costumes'][i+1]['pic'])
															portraitDatabase[doll['internalName']][charSpr]=doll['costumes'][i]['pic']
															portraitDatabase[doll['internalName']][charSpr+1]=doll['costumes'][i+1]['pic']
															printOK("Added to database")
															printOK(str(portraitDatabase[doll['internalName']]))
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
											
							#else:
								#print("No costume story? "+costumeID)
							
					
					#assert(len(portraitDatabase[doll['internalName']]) > 1)
				#Automatically search for special portraits since they're usually named correctly
				expressionFiles = glob.glob("../pic/special/pic_"+doll['internalName']+"_*")
				for expressionFile in expressionFiles:
					fParams = expressionFile.split("_")
					fNameNoDir = expressionFile.split("/")[-1]
					#If it's not 3 params... Just ignore it
					if len(fParams)==3:
						portraitType = fParams[-1][:-4]
						try:
							portraitIdx = int(portraitType)
							if len(portraitDatabase[doll['internalName']])-1 < portraitIdx or (len(portraitDatabase[doll['internalName']]) > portraitIdx and portraitDatabase[doll['internalName']][portraitIdx] == None):
								portraitDatabase[doll['internalName']][portraitIdx]='special/'+fNameNoDir
								printOK("Inserted special portrait: "+portraitDatabase[doll['internalName']][portraitIdx])
							else:
								printWarn("A portrait ID already exists where a special portrait was found. Not inserting portrait "+fNameNoDir)
								printWarn(str(portraitDatabase[doll['internalName']]))
						except Exception as e:
							pass
							#printError(str(e))
							#printError(str(portraitDatabase[doll['internalName']]))
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


#First scan for missing portraits that might match, like case insensitive matches
with open('chapterDatabase.json','r') as f:
	j = JSON.loads(f.read())
	chapters = j['story']
	backgrounds = j['bg']
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
								if p[0] not in portraitDatabase:
									for p2 in portraitDatabase:
										if p[0].lower() == p2.lower():
											printOK("Found portrait with different capitalization, renaming: "+p2+ " -> "+p[0])
											portraitDatabase[p[0]]=portraitDatabase[p2]
											break
									for fName in [p[0]+'.png','pic_'+p[0]+'.png','special/'+p[0]+'.png']:
										if os.path.isfile('../pic/'+fName):
											printOK("Missing portrait '"+p[0]+"' matches "+fName+", adding to DB.")
											portraitDatabase[p[0]]=ResizingList([fName])
											break

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
	'special/版娘Armor.png',
	None,
	"special/NPC-Kalin_11.png",
	"special/NPC-Kalin_12.png",
	"special/NPC-Kalin_13.png",
]

portraitDatabase['NPC-Yegor'] = [
	'NPC-Yegor.png',
	'NPC-YegorArm.png',
	'NPC-YegorArm2.png',
	'NPC-YegorArm3.png',
	'NPC-YegorArm4.png'
]
portraitDatabase['NPC-Soldier'] = ['NPC-YegorArm3.png']

portraitDatabase['NPC-Ange'] = ResizingList([
	'NPC-Ange.png',
	'NPC-Ange_1.png',
	None,
	'special/NPC-Ange(3).png',
	'special/NPC-Ange(4).png',
	'special/NPC-Ange(5).png',
	'special/NPC-Ange(6).png',
	'special/NPC-Ange(7).png'
])

portraitDatabase['NPC-AngeDamage'] = ResizingList([
	'special/NPC-AngeDamage.png',
	None,
	None, #"special/NPC-AngeDamage2.png", #Unconfirmed
	None, #"special/NPC-AngeDamage3.png", #Unconfirmed
	"special/NPC-AngeDamage4.png" #This is identical to NPC-Ange_1.png, I have no idea why they used a separate image
])


portraitDatabase['NPC-Persica'] = [
	"pic_NPC-Persica.png",
	"pic_NPC-Persica_C.png",
	"pic_NPC-Persica_J.png",
	"pic_NPC-Persica_T.png"
]
portraitDatabase["NPC-Helian"]=[
	"pic_NPC-Helian.png",
	"pic_NPC-Helian_A.png",
	"pic_NPC-Helian_F.png",
	"pic_NPC-Helian_T.png"
]
portraitDatabase['NPC-Deele']=[
	"pic_NPC-Deele.png"
]
portraitDatabase['NPC-Seele']=[
	"pic_NPC-Seele.png",
	"pic_NPC-Seele_1.png"
]
portraitDatabase['NPC-Dima']=quickGenerateNPC('NPC-Dima',3)
portraitDatabase['NPC-Light']=quickGenerateNPC('NPC-Light',5)
#print(quickGenerateNPC('NPC-Light',5))

portraitDatabase['NPC-Jason']=["NPC-Jason.png","NPC-Jason_1.png"]
portraitDatabase['NPC-Havel']=["NPC-Havel.png","NPC-Havel2.png"]
portraitDatabase['NPC-Morridow'] = quickGenerateNPC('pic_NPC-Morridow',7,False,True)


portraitDatabase['Seele'][2]='SeeleVollerei.png'

portraitDatabase['AK12'][2]='special/AK12_angry.png'
portraitDatabase['AK47'].quickInsertSpecial(2)

portraitDatabase['Jillmagic']=['pic_Jill_529.png']
portraitDatabase['RO635-NoArmor']=['special/pic_RO635_NoArmor0.png']


#Slot 0 and 1 are normal and damage
portraitDatabase['RO635'][2] = 'special/pic_RO635_1.png'
portraitDatabase['RO635'][3] = 'special/pic_RO635_2.png'
portraitDatabase['RO635'][4] = 'special/pic_RO635_3.png'
portraitDatabase['RO635'][5] = 'special/pic_RO635_4.png'
portraitDatabase['RO635'][6] = 'special/RO635Dinergate.png'

#portraitDatabase['BOSS-9']=['pic_BossArchitect_LL.png']
#portraitDatabase['BOSS-12']=['Eliza.png']
portraitDatabase['BossDestroyerPlus']=['DestroyerPlus.png']

portraitDatabase['Nyto'][7]="special/Nyto_7.png"
portraitDatabase['NytoWhite']=["Nyto_white.png"]
portraitDatabase['Nytochild01']=["Nytochild01_1.png","Nytochild01_2.png","Nytochild01_3.png"]
portraitDatabase['Nytochild02']=["Nytochild02_1.png","Nytochild02_2.png"] #Does not have a third portrait
portraitDatabase['Nytochild03']=["Nytochild03_1.png","Nytochild03_2.png","Nytochild03_3.png"]


#Seems like they intended for there to be more expressions? They're all dupes though
portraitDatabase['NytoIsomer'][3]="Nyto_Isomer_Shadow.png"
portraitDatabase['NytoIsomer'][4]="Nyto_Isomer_Shadow.png"
portraitDatabase['NytoIsomer'][5]="Nyto_Isomer_Shadow_nervous.png"

portraitDatabase['AbandonedIsomer']=['Abandoned_Isomer.png']

portraitDatabase['M1903bar']=["special/M1903_Bartender.png"]
portraitDatabase['M1903'].quickInsertCostumeAtIdx(8,"1107")

#Not incorrect, slot 1 is occupied by damaged art
portraitDatabase['HK416'][2] = 'special/pic_HK416_1.png'
portraitDatabase['HK416'][3] = 'special/pic_HK416_2.png'

#Not incorrect either
portraitDatabase['HK416Mod'][2]='special/pic_HK416Mod_1.png'

#Since slot 1 is taken
portraitDatabase['SL8'][2] = 'special/pic_SL8_1.png'
portraitDatabase['SL8'][3] = 'special/pic_SL8_3.png' #There is no pic_SL8_2 so I can only assume this is what is supposed to be here...


portraitDatabase['M16']=portraitDatabase["M16A1"]
portraitDatabase['M16'][4]='special/pic_M16A1_2.png'
portraitDatabase['M16'][5]='special/pic_M16A1_3.png'
portraitDatabase['M16'][6]='special/pic_M16A1_4.png'
portraitDatabase['M16'][7]='special/pic_M16A1_5.png'

portraitDatabase['M16A1BOSS']=['pic_M16A1_Boss.png','special/pic_M16A1_1.png']
portraitDatabase["MK2"]=portraitDatabase['StenMK2']
portraitDatabase['FAL']=portraitDatabase['FNFAL']
portraitDatabase['FAL'][2] = "pic_FNFAL_308.png"
portraitDatabase['FAL'][3] = "pic_FNFAL_308_D.png"

portraitDatabase['SOPII'] = portraitDatabase['M4 SOPMOD II']
portraitDatabase['SOPII'][2] = portraitDatabase['SOPII'][0]
portraitDatabase['SOPII'][3] = portraitDatabase['SOPII'][0] #Weird, I guess they originally planned to draw more?
portraitDatabase['SOPIIDamage'] = ResizingList(['special/M4 SOPMOD IIDamage.png','special/M4 SOPMOD IIDamage2.png','special/M4 SOPMOD IIDamage3.png'])


portraitDatabase['M4 SOPMOD IIMod-Noarmor'] = ['pic_M4 SOPMOD IIMod_NoArmor1.png']

portraitDatabase['pa15'].quickInsertCostumeAtIdx(2,"4202")

portraitDatabase["FAMASHalloween"]=["pic_FAMAS_2604.png"]


portraitDatabase['P7'].quickInsertCostumeAtIdx(2,"1404")
#portraitDatabase['P7'][6]='special/pic_P7_6.png'
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
#It seems like  this was intended for the first slot, but it's identical to the regular expression aside from having a corrupted transparency. So instead, I'm using the regular image.
#portraitDatabase['G11'][1] = 'special/pic_G11.png' 
portraitDatabase['G11'][1] = 'pic_G11.png' 
portraitDatabase['G11'][2] = 'special/pic_G11_1.png' #Confirmed in second slot
portraitDatabase['G11'][3] = 'special/pic_G11_2.png' #I checked memoir/103_4.txt and confirmed this is being used in the third slot

#Fun fact, this ID is missing from the EN servers: https://youtu.be/di7khdQ3vbE?t=559
portraitDatabase['G11story']=['special/pic_G11_rugged.png','special/pic_G11_maid.png']

portraitDatabase['UMP9story'] = ResizingList(['special/ump9.png'])

#Slot 1 and 2 is normal and damage
portraitDatabase['UMP9'][2]='special/pic_UMP9_1.png'
portraitDatabase['UMP9'][3]='special/pic_UMP9_2.png'
portraitDatabase['UMP9'][4]='special/pic_UMP9_3.png'
portraitDatabase['UMP9Mod'][2] = 'special/pic_UMP9Mod_dislike.png'
portraitDatabase['UMP9Mod'][3] = 'special/pic_UMP9Mod_happy.png'
portraitDatabase['UMP9Mod'][4] = 'special/pic_UMP9Mod_angry.png'
portraitDatabase['UMP9Mod'][5] = 'special/pic_UMP9Mod_helpness.png'
portraitDatabase['UMP9Mod'][6] = 'special/pic_UMP9Mod_sad.png'

portraitDatabase['UMP40'][5] = 'special/pic_UMP40_angry.png'
portraitDatabase['UMP45_Young'] = ResizingList(['special/UMP45-Young.png','special/UMP45-Young_sad.png','special/UMP45-Young_serious.png','special/UMP45-Young_angry.png'])

#Because it normally wouldn't overwrite idx 1
portraitDatabase['Henrietta'].quickInsertSpecial(1)

#portraitDatabase["MDR"].extend(["pic_MDR_2603.png","pic_MDR_2603_D.png"])
#portraitDatabase["BrenMK"].extend(["pic_BrenMK_2605.png","pic_BrenMK_2605_D.png"])
#portraitDatabase["SAT8"].extend(["pic_SAT8_1802.png","pic_SAT8_1802_D.png","pic_SAT8_2601.png","pic_SAT8_2601_D.png"])


#fairies
portraitDatabase['DJMAXSUEE']=['equip/DJMAXSUEE_1.png']
portraitDatabase['DJMAXPREIYA']=['equip/DJMAXPREIYA_1.png']
portraitDatabase['DJMAXSEHRA']=['equip/DJMAXSEHRA_1.png']
portraitDatabase['FairyWarrior']=['equip/fighting_1.png']

portraitDatabase['AR15'][2] = "special/AR15_T.png"
#AR15 originally had something in the third slot, but since a costume overwrote it we'll never know what it was. There aren't any files for the third slot anyways so it had to have been a dupe.

portraitDatabase['AR15Mod'][2] = 'special/AR15Mod_伤心.png'
portraitDatabase['AR15Mod'][3] = 'special/AR15Mod_微笑.png' #Unconfirmed, but it's the only free slot so it's probably correct
portraitDatabase['AR15Mod'][4] = 'special/AR15Mod_无奈.png'
portraitDatabase['AR15Mod'][5] = 'special/AR15Mod_紧张.png'

portraitDatabase["M4A1"][2] = "special/M4A1_SAD.png"
portraitDatabase["M4A1"][3] = "special/M4A1_T.png"

portraitDatabase['M4A1Mod'][2]='special/M4A1Mod_微笑.png' #Smile
portraitDatabase['M4A1Mod'][3]='special/M4A1Mod_悲伤.png'
portraitDatabase['M4A1Mod'][4]='special/M4A1Mod_紧张.png'

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

