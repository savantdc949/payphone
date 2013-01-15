This is where code would/should/might go. Basically, all of the brute force code was lost in a drive crash. I'm too busy to bother starting over, sorry.

On the other hand, I've decided to try and have another go at the ACTS detection code. This is what I've got so far. I'm a crap coder so don't expect anything elegant. Bugs are expected.

===============
Goals:
===============
1. Learn Python (gotta start somewhere)
2. Learn Github (check!)
3. Make cool shit?
4. ...
5. Not profit. (open source joke, heh)

===============
ACTSdetect.py
===============

WHY:
ACTS, Automated Coin Toll Service, was the system the phone company would use to track how much money had been inserted into a payphone. (http://en.wikipedia.org/wiki/Traffic_Service_Position_System#Automated_Coin_Toll_System). I thought it would be cool to make it so the Asterisk open source PBX phone system could support ACTS so "red boxing" calls through Asterisk would be possible. 

Basically I started with Black Aura's Python DTMF decoding script, pygoertzel.py. It's awesome, and can be found here:

http://www.black-aura.com/blog/2011/12/10/python-implementation-of-the-goertzel-algorithm-dtmf-decoding/

Then I added in an additional check looking for 1700hz + 2200hz. If the code detects a tone, "R" is printed. I've added in some very kludgy "coin counting" which approximates how much "money" has been presented. Right now, I can only semi-reliably detect quarter tones, which are five 33ms chirps of 1700hz+2200hz, seperated by 33ms of silence. At this point I'm treating each "digit" detected as a quarter. If you've got more python/math skills than me and you know how to fix this, by all means please help out.


The ultimate goal of this is to be able to create an Asterisk EAGI which will prompt a user to "Please insert twenty-five cents", with my reference being the Pacific Bell RBOC circa 1995. I believe a quarter got you 10-15 minutes. So basically, the EAGI prompts you for a quarter, and then the call audio is recorded to a wave file and then analyzed for "coin" detection. For every coin tone, 10-15 minutes get added. At the end of the alloted time, the application will then prompt the user again for more money, or hang up the call.

The nice thing is, you *should* be able to use a REAL BOCOT payphone with a totalizer that generates ACTS as well as using a red box tone generator. I don't have a real one (though I sure would love an old PacBell payphone, pre-AT&T), so YMMV.

I have not yet removed any of Black Aura's DTMF detection stuff, so the code should also still decode DTMF touch tones. Pretty nifty, although I'll end up removing it later to try and optimize. Yeah, optimize. Doesn't that require someone to know what they're doing first?

Anyhow, this is barely more than vaporware anyway at this point.

USEAGE:

python ACTSdetect.py somewavefile.wav

The wav file should be resampled at 8000hz and 16bit. sox is your friend:

sox somewavefle.wav -b 16 -r 8000 somenewfile.wav

TODO:
Write code that works.
Write code that works better.
Write the actual EAGI.
Write a readme that doesn't suck.
