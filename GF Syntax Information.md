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
* `RO635()` Changes the speaker name to "RO635".

### ;
Determines when to dim a portrait. If it's before the <Speaker> tag it dims the left, if it's after it dims the right.

### 通讯框

Ex. `<通讯框>`.

"Communication box". Display previous character portrait inside a communication box.

### <Grey>
Unknown. Probably colors the previous portrait grey.

Used in the valhalla collab.

### Position

Ex. `<Position>i,j</Position>`

Set position of last portrait. No idea what i,j is but assume x and y values

## Other

### BGM

ex. <BGM>djmax_gloryday</BGM>

Sets BGM. Usually whatever is in the tag is the exact file name, but oddly enough some file names are different.

Known tags vs actual filenames:
* BGM_Sunshine -> home_formation_factory
* BGM_NightOPS -> GUN_CineTense_loop

### BIN

ex. <BIN>112</BIN>

Set background. Aside from a few special cases it's whatever background is at that line in profiles.txt.

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

## Screen transitions

### <黑点X>
Black dot screen transition. X=1 for in, 2 for out.

### <黑屏X>
Black screen fade in and out
		
### <震屏> 
Screen shake effect

		
## Animations/Background related

### <下雪>
Add snow animation to cutscene (Used in The Division)
### <火焰销毁>
Stop all cutscene animations, probably
		

## : 
End of opcodes, text goes after this (Other than +)


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

# Fun things I've found
If a tag is missing the end, the entire tag gets ignored.

One of the MOD stores contains three portrait commands in one line. The game doesn't support this, so the second portrait is replaced with the last used command.

There is a typo in the valhalla collab, -32-1-1.txt: `()<Speaker>Dana</Speaker>)||:Most of us are gone, along with our civilization.`. The `)` probably gets ignored.

Portraits don't match the internal names used for adjutant dialogue, for some reason. Also some portraits that should be types are their own name.

M4 SOPMOD II is in the database twice. In earlier files she's indexed as SOPII.

# Unknown usages


## Portrait type specificed without a portrait

It's possible this defaults to the gray shadow portrait. Which is funny, because it's already indexed as "G11story".
```
(0)<Speaker>Super-Shorty</Speaker>||:Batteries...
(0)<Speaker>Dana</Speaker>||:Huh?
```
