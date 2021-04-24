# Stage filename information

filenames are in the syntax of EPISODE-CHAPTER-PART(MODIFIER).txt

Stage 1-1: 1-1-1.txt, 1-1-2.txt

Stage 1-1 Emergency: 1-1-1E.txt, 1-1-2E.txt

Stage 1-1 Night: 1-1-1N.txt, 1-1-2N.txt


# opcode dictionary
Seriously, who designed this thing? What is this ridiculous mix of HTML tags and control characters?

Did `<Portrait type=1>RO635</Portrait>` make too much sense? And what's with all these special cases for the portrait command?

Why would you even create a syntax that has to look backwards to apply attributes? You're already using tags, you could have put them in the tag.

## Portrait Related

### XXX(n)
Set portrait. `XXX` is character sprite, `n` is type. Can have multiple of these. Actually does not need to be the first opcode.

**Note that if `n` is missing it won't show the portrait but instead the literal name of the sprite will be used as the speaker. (Why this is even a feature is a complete mystery)**

Examples:
* `()` - No portrait. Essentially does nothing, but the game requires at least one portrait command. (The interpreter does not)
* `RO635(0)` to display "RO635" with her default sprite (Type 0).
* `M1873(4)` to display Colt Revolver with her 'Queen of Miracles' costume (Type 4).
* `RO635()` Changes the speaker name to "RO635". Does not create a portrait.
* `(0)` Unknown (Read below)

### ;
Determines when to dim a portrait. If it's before the <Speaker> tag it dims the left, if it's after it dims the right.

The full-width `；` is also valid, for whatever reason.

### 通讯框

Ex. `<通讯框>`.

"Communication box". Display previous character portrait inside a communication box.

### Grey
Unknown. Probably colors the previous portrait grey.

Used in the valhalla collab.

### Shake

Portrait shakes left and right a little upon appearance. Used in HK416 MOD story (memoir/65_1.txt)

### Position

Ex. `<Position>x,y</Position>`

Set position of last portrait. x,y is probably offset from default position.

## Other

### BGM

ex. `<BGM>djmax_gloryday</BGM>`

Sets BGM. Usually whatever is in the tag is the exact file name, but this pulls from a dictionary in /assets/resources/dabao/textdata/AudioTemplate.txt

### BIN

ex. `<BIN>112</BIN>`

Set background. Aside from a few special cases it's whatever background is at that line in profiles.txt.

BIN 10 is a special case; It's a fully transparent image that shows the stage underneath. However when replaying it through the index it will pick PlaybackBG1 or PlaybackBG2. It doesn't seem to be determined by anything in the script but rather stage metadata.

Note that it's possible for there to be text without a background being set. I have no idea what the color would be in that case but you can probably just use black.

### Speaker

ex. `<Speaker>Dandelai</Speaker>`

Set the speaker name. Duh.

### || 
Separator. Things after this separator will be run later, maybe? Usually transition commands, shake effects, etc are after these

Sound effects are also after this

### <回忆>
Set orange textbox
### <关闭蒙版>
Unknown, possibly related to orange textbox

### SE1, SE2

ex. `<SE1></SE1>`, `<SE2></SE2>`

Not sure what the difference is between 1 or 2.

Like BGM, this pulls from a dictionary in /assets/resources/dabao/textdata/AudioTemplate.txt

## Screen transitions

### <黑点X>
Black dot screen transition. X=1 for in, 2 for out.

### <黑屏X>
Black screen fade in and out. 1 = out, 2 = in (Yes, it's reversed from the above one for some reason)

Accepts two parameters, which might be speed and ???. Otherwise only the beginning tag is present.

Example in Honkai Impact 2nd (-15-3-2First.txt): `芽衣()<Speaker>芽衣</Speaker>||<黑屏1>5</黑屏1>`

Example in ISOMER: `Nyto(0)<Speaker></Speaker>||<黑屏1>0.5,0.5</黑屏1>`

### <震屏> 
Screen shake effect

### 睁眼
Translates to 'eyes open', eye open screen in transition

		
## Animations/Background related

### Night
Take a wild guess. Applies a blue filter over the previous background.

Works on any background, not just outdoors ones.

Blue filter is roughly brightness -100 and color temperature 3000 in GIMP.

Since I have no idea what that is in raw RGB value manipulation the algorithm in the interpreter is just R/2, G/2 (B is untouched)

Screen transitions will disable night BG.

### 平移
Pan background from left to right.

There's only one background in the entire game that's in widescreen (StoryCG5). It's only ever seen in Chapter 0-4.

The whole command: `<黑屏2><黑屏1><平移><SE1>Battlefield</SE1><刮花><边框>2</边框><BIN>20</BIN>`

### 边框
Add frame around background.

Multiple frames exist.

I don't know where the frames are stored.

### 下雪
Add snow animation to cutscene (Used in The Division)

### 火花
Add fire animation to cutscene. Takes a float as an argument, probably related to speed.

Example: `<火花>1.7</火花>`

### 关闭火花
Disable fire animation.

### 刮花
A different fire animation. It appears to be the textures in `/atlasclips/_nospritepacker/avg/`, just colored orange.

### 闪屏
Unknown. Translates to 'splash screen'.

Uses `duration` command for some reason.

example: `<闪屏><duration>5</duration></闪屏>`

### 火焰销毁
Stop all cutscene animations, probably.

An end tag is not required.

### 分支
Branch destination. See `<c>` for more info.

### CGDelay
Unknown. Appears to be text related? Might delay drawing text?

## : 
End of opcodes, text and text commands go after this.

Full width `:` is also valid.

## Text related

### + 
End text. Text will continue in a new box (no close/open animation) when clicked.

### color

ex. `<color=#00CCFF>This is holo blue</color>`

Take a wild guess

### size

ex. `<size=60>THIS IS LARGE TEXT</size>`

Take a wild guess. 

Known sizes:
* 25 is small.
* 55 is slightly larger.
* 60 is very large.

### c
Choice.
Looks like choice will be up until the next command.

Example: `... <c>I don't have a clue. <c>I'm not telling you. <c>She never would have told me.` creates choices `["I don't have a clue.", "I'm not telling you.", "She never would have told me."]`

The result is stored as an int and the game searches until it finds the corresponding branch (1-indexed) marked with `分支`.

Full example:
```
Nyto(0)<Speaker>Commander</Speaker>||:... <c>I don't have a clue. <c>I'm not telling you. <c>She never would have told me.
Nyto(0)<Speaker>Nyto</Speaker>||<分支>1</分支>:Indeed, we have no evidence to either support or refute your claim.
Nyto(0)<Speaker>Nyto</Speaker>||<分支>2</分支>:We know. It is an answer we expected.
Nyto(0)<Speaker>Nyto</Speaker>||<分支>3</分支>:Then I can assume that she does not trust you all that much.
```

### b

Take a wild guess.

It makes text bold. Only used one entire time in 'TMP - Red-Eared Cat' skin story (2807.txt)

# Fun things I've found
If a tag is missing the end, the entire tag gets ignored.

One of the MOD stores contains three portrait commands in one line. The game doesn't support this, so the second portrait is replaced with the last used command.

`98k(0);98k(0)<Speaker>Kar98k</Speaker>;STG44Mod(0)<通讯框>||:Nein, we still have a chance.` 10-3 Night has this typo.

There is a typo in the valhalla collab, -32-1-1.txt: `()<Speaker>Dana</Speaker>)||:Most of us are gone, along with our civilization.`. The `)` probably gets ignored.

Portraits don't match the internal names used for adjutant dialogue, for some reason. Also some portraits that should be types are their own name.

M4 SOPMOD II is in the database twice. In earlier files she's indexed as SOPII.

The ID 'G11story' is not indexed in EN for some reason. It should be G11 dressed in green and maid costume.

# Unknown usages

## Portrait type specificed without a portrait

It's possible this defaults to the gray shadow portrait, which is used when an invalid ID is specificed.
```
(0)<Speaker>Super-Shorty</Speaker>||:Batteries...
(0)<Speaker>Dana</Speaker>||:Huh?
```

Also seen in /avgtxt/skin/3501.txt. R93's Holiday Lucky Star skin story.

# Unofficial opcodes

Stuff the interpreter can do.

### i

This is probably officially implemented, but since it's never used it's "unofficial" until the existence can be confirmed.
