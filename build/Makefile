#objects := $(wildcard *.py)

#Don't use this
dist:
	rm -r dist && mkdir dist
	mv index.html dist/index.html
	mv chapterDatabase.json dist/chapterDatabase.json
	mv girlsfrontline-min.json dist/girlsfrontline-min.json
	mv portraitInformation.json dist/portraitInformation.json
	rsync -ahr --progress avgtxt/ dist/avgtxt
	rsync -ahr --progress avgtexture/ dist/avgtexture
	cd dist/avgtexture
	find *.png -exec convert {} -gravity center -crop 1024x576+0+0 +repage {} \;
	cd ..
	#rsync -ahr --progress dump/out/wav/ dist/avgtexture

build: girlsfrontline.json fetter.json fetter_story.json NormalActivityCampaign.txt
	#if test -d avgtxt; then echo 
	#echo $(objects)
	#python3 
	./eventStoryStuff.py
	./minifyGirlsfrontlineJSON.py
	./auditPortraits.py
	
	mv chapterDatabase.json ../
	mv portraitInformation.json ../
	mv missingPortraits.json ../
	mv girlsfrontline-min.json ../
	#ifdef local
	#	./gtml -DLOCAL_ONLY=True index.gtml
	#else
	#	./gtml index.gtml
	#endif
	#./gtml index.gtml
	@echo "All done..."
	#@echo "All done... Run 'make dist' if you want to copy everything in a distributable format"
	
dump:
	dump/dump.sh
	cp dump/out/text/table/fetter.json fetter.json
	cp dump/out/text/table/fetter_story.json fetter_story.json
	cp dump/out/avgtxt avgtxt
	cp dump/out/assets/resources/dabao/avgtxt/fetter avgtxt/fetter
	cp dump/out/assets/resources/dabao/avgtxt/va11 avgtxt/va11
	if test -f girlsfrontline.json || echo "Please run make dl to download girlsfrontline.json"

dl:
	test -f girlsfrontline.json && rm girlsfrontline.json
	wget --header='Accept-Encoding: gzip' -O - https://github.com/RhythmLunatic/Girls-Frontline-Discord-Search/raw/master/girlsfrontline.json | gunzip -c > girlsfrontline.json

clean:
	git fetch origin
	git reset --hard origin/master

all:
	dump dl build
.PHONY: all
