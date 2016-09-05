# VideoAlarmClock

<img src="https://github.com/AYWG/VideoAlarmClock/blob/master/img/VAC1.jpg" alt="VAC Screenshot 1" width="250" height="200">
<img src="https://github.com/AYWG/VideoAlarmClock/blob/master/img/VAC2.jpg" alt="VAC Screenshot 2" width="250" height="200">
<img src="https://github.com/AYWG/VideoAlarmClock/blob/master/img/VAC3.jpg" alt="VAC Screenshot 3" width="250" height="200">

A simple alarm clock developed in Python, using [Tkinter](https://wiki.python.org/moin/TkInter) for its GUI.
The program receives from the user:

1. A date and time in the future for when the alarm should activate
2. A text file containing Youtube URLs (one per line)

Once the current system time reaches the alarm time, the program will randomly choose one of the URLs in the given text file and launch it in a new browser tab.

*The program also functions solely through the command line (no GUI needed).*

Makes use of [tkinter_components](https://github.com/moshekaplan/tkinter_components) (with some slight modifications and additions). Also uses [tkFileDialog](http://tkinter.unpythonic.net/wiki/tkFileDialog).

---

### Personal note:
I wrote this program as another means of keeping myself awake when staying up late at night. Because I tend to alternate my computer's audio output settings 
(sound can either come from my headphones or my monitor's speakers), the following situation can occur:

1. I doze off
2. I'm not wearing my headphones / my headphones slip off of my ears
3. The program launches a Youtube video, but the sound is still playing through my headphones (which means I won't hear it)

To deal with this, the program uses [NirCmd](http://www.nirsoft.net/utils/nircmd.html) to switch audio output to my monitor's speakers and set the volume to the maximum level, ensuring that I'll be able to hear the video.

