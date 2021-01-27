# gfl-cutscene-interpreter
Girls' Frontline Cutscene Interpreter. Watch or read GFL cutscenes right in your browser.

In action: http://gfl.amaryllisworks.pw

# BUGS
- ~~Phaser cannot restart, a scene has to be used.~~ Even with the scene, it crashes. Probably a race condition.
- The interactive playback is VERY buggy right now
- Sometimes the text interpreter screws up.
- The UI for picking a chapter is... Horrible.
- Missing BGs, doll portraits, and much more...
- T-Doll dialogue section crashes mobile web browsers (too much memory?)

# TODO
- More dialogue
- A makefile
- Make public the modified gfl dumper (I modified abunpack.py to dump everything instead of whatever was in config.json)

# HOW DO I USE???
1. First, dump all the game data. Yes, all of it. It's required so you have portraits, music, and text.
2. Then put avgtxt and avgtexture in the same folder.
3. Then copy VA11 folder from resources/dabao/avgtxt/
4. Then run minifyGirlsfrontlineJSON.py and eventStoryStuff.py to generate the files for the webpage (sorry, I should really make a makefile)
5. Then host a webserver. You'll want to add this CSP to your webserver if you're allowing user created cutscenes to be loaded: `Header set Content-Security-Policy "default-src 'self' data: https://fonts.gstatic.com; style-src 'unsafe-inline' cdnjs.cloudflare.com https://fonts.gstatic.com https://fonts.googleapis.com; script-src 'unsafe-inline' cdnjs.cloudflare.com cdn.jsdelivr.net;"`

For debugging: `python3 -m http.server`, then go to http://localhost:8000 in your internet browser

# license
AGPLv3
- In case of the client side code used in this webpage being converted to server side (ex. txt -> json conversion in advance instead of on the fly), you must distribute the source code to comply with the license.
- Modifying the python scripts does require you to give out the source code, should you decide to host an instance of this software on your own webserver.
- Please include a link to the source code somewhere easily accessible. For example, at the bottom of the page like how it is on mine. (Of course if you don't ever modify anything you can just keep the link as-is)
