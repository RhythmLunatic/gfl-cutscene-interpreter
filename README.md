# gfl-cutscene-interpreter
Girls' Frontline Cutscene Interpreter. Watch or read GFL cutscenes right in your browser.

In action: http://gfl.amaryllisworks.pw

# BUGS
- ~~Phaser cannot restart, a scene has to be used.~~ Even with the scene, it crashes. Probably a race condition.
- The interactive playback is VERY buggy right now
- Sometimes the text interpreter screws up.
- The UI for picking a chapter is... Horrible.
- Missing BGs, doll portraits, and much more...

# TODO
- More dialogue

# HOW DO I USE???
First, dump all the game data.
Then put avgtxt and avgtexture in the same folder.
Then copy VA11 folder from resources/dabao/avgtxt/

Then host a webserver. 

For debugging: `python3 -m http.server`, then go to http://localhost:8000 in your internet browser

# license
AGPLv3
