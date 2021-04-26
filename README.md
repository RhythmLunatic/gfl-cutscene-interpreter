# gfl-cutscene-interpreter
Girls' Frontline Cutscene Interpreter. Watch or read GFL cutscenes right in your browser.

In action: http://gfl.amaryllisworks.pw

# Features
- Read cutscenes in the browser, straight from the original game files and converted on the fly
- (WIP) write your own cutscenes
- Named chapters, named episodes
- Dark mode, light mode, etc
- Material design. Webpage works on your phone, of course.
- Free and open source copyleft software


# BUGS
- ~~Phaser cannot restart, a scene has to be used.~~ Even with the scene, it crashes. Probably a race condition.
- The interactive playback is VERY buggy right now
- ~~Sometimes the text interpreter screws up.~~ This has been mostly resolved by now
- The UI for picking a chapter is... Horrible.
- Missing a couple portraits, since the portrait database doesn't seem to exist anywhere.
- T-Doll dialogue section crashes mobile web browsers (too much memory?)

# TODO
- More dialogue
- Make public the modified gfl dumper (I modified abunpack.py to dump everything instead of whatever was in config.json)
- Check issues page on github

# HOW DO I SELF-HOST?
1. First, dump all the game data. Yes, all of it. It's required so you have portraits, music, and text.
2. Copy avgtxt, avgtexture, pic, and audio to the root folder (next to the index.html).
3. Then copy VA11 and fetter folder from resources/dabao/avgtxt/ and put in the folder in your root.
4. put 'special' and 'equip' folders inside pic folder.
5. After a while I started reorganizing the pic folder because MICA doesn't know how to organize shit and it's really annoying to search two different places for portrait variants. So go into build folder and run the reorganize_portraits.py file.
6. Then host a webserver. You'll want to add this CSP to your webserver if you're allowing user created cutscenes to be loaded: `Header set Content-Security-Policy "default-src 'self' data: https://fonts.gstatic.com; style-src 'unsafe-inline' cdnjs.cloudflare.com https://fonts.gstatic.com https://fonts.googleapis.com; script-src 'unsafe-inline' cdnjs.cloudflare.com cdn.jsdelivr.net;"`

For debugging: `python3 -m http.server`, then go to http://localhost:8000 in your internet browser

# HOW DO I BUILD?
**Building is optional, the repo will always have the latest built json files.**

1. Put the following files in the build folder:
* AudioTemplate.txt (Audio database)
* profiles.txt (Background database)
* fetter.json
* fetter_story.json
* NormalActivityCampaign.txt
* mission.json
* NewCharacterVoice.json
2. cd to build. Run 'make dl' to download the latest girlsfrontline.json, then run 'make build'. It will overwrite the json files in the root dir with new ones. Your portrait files will be checked in case you're missing anything or they're in the wrong location.

# license
AGPLv3
- In case of the client side code used in this webpage being converted to server side (ex. txt -> json conversion in advance instead of on the fly or static HTML pages), you must distribute the source code to comply with the license.
- Modifying the build scripts does require you to give out the source code, should you decide to host an instance of this software on your own webserver.
- Please include a link to the source code somewhere easily accessible. For example, at the bottom of the page like how it is on mine. (Of course if you don't ever modify anything you can just keep the link as-is)

- Webpage mostly built using https://materializecss.com/
