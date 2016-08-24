# A program that accepts command line arguments for what time to go off, and when it does it launches a Youtube video 
# in a new browser tab that will start playing. The program reads in a text file that contains URLs to different 
# Youtube videos and will randomly choose one and launch it. It also switches audio output to my monitor's speakers 
# and sets the volume to max (to ensure I hear it)

import sys
from datetime import datetime
import time as t
import subprocess
import webbrowser
import random

# For the GUI
import Tkinter
import Tkconstants
import ttkcalendar
import tkSimpleDialog
import CalendarDialog
import TimeDialog
import tkFileDialog

class VideoAlarmClockUI(Tkinter.Frame):

	def __init__(self, root):

		Tkinter.Frame.__init__(self, root)

		# set minimum window size
		root.minsize(width=300, height=200)

		# options for buttons
		button_opt = {'fill': Tkconstants.BOTH, 'padx': 30, 'pady': 10}

		# define button for setting time and date here
		
		Tkinter.Button(root, text='Select Date and Time', command=lambda:self.getdatetime(root)).pack(**button_opt)
		Tkinter.Button(root, text='Select Video File', command=self.askopenfilename).pack(**button_opt)
		#Tkinter.Button(root, text='Set Alarm', command=self.setalarm).pack(**button_opt)

		# define options for opening or saving a file
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = 'videos.txt'
		options['parent'] = root
		options['title'] = 'This is a title'

	def askopenfilename(self):
		return tkFileDialog.askopenfilename(**self.file_opt)

	def getdatetime(self, root):
		cd = CalendarDialog.CalendarDialog(root)
		if cd.result:
			td = TimeDialog.TimeDialog(root)
		print cd.result

if __name__ == '__main__':
	root = Tkinter.Tk()
	root.title("Video Alarm Clock")
	VideoAlarmClockUI(root).pack()
	root.mainloop()
	quit()

# Check number of arguments
if len(sys.argv) != 6:
	print "Invalid number of arguments."
	print "Usage: python VideoAlarmClock.py [time in 24-hour format] [day] [month] [year] [video_file.txt]"
	print "For example, to set alarm clock for 00:30 on June 24th 2016 using videos.txt, run:"
	print "python VideoAlarmClock.py 00:30 24 6 2016 videos.txt"
	quit()

script, time, day, month, year, video_file = sys.argv

current_time = datetime.now()

if (len(time) != 5 or time[2] != ':'): 	# format = xx:yy, so length == 5
	print "Incorrect time format."
	print "Please provide a time of the form: xx:yy"
	print "where xx is the hour and yy is the minute (in 24-hour format)"
	quit() 

try:
	alarm_year = int(year)
	alarm_month = int(month)
	alarm_day = int(day)
	alarm_hour = int(time[:2])
	alarm_min = int(time[3:])
except ValueError:
	print "Invalid time/date value"
	quit()

if (alarm_year < current_time.year or
	(alarm_year == current_time.year and alarm_month < current_time.month) or
	(alarm_year == current_time.year and alarm_month == current_time.month and alarm_day < current_time.day) or
	(alarm_year == current_time.year and alarm_month == current_time.month and alarm_day == current_time.day
	 and alarm_hour < current_time.hour) or
	(alarm_year == current_time.year and alarm_month == current_time.month and alarm_day == current_time.day
	 and alarm_hour == current_time.hour and alarm_minute <= current_time.minute)):
	print "The provided time/date of the alarm clock is in the past."
	print "Please provide a time and date in the future."
	quit()

alarm_time = datetime(alarm_year, alarm_month, alarm_day, alarm_hour, alarm_min)
time_difference_in_sec = int((alarm_time - current_time).total_seconds())

seconds_in_a_day = 86400
seconds_in_an_hour = 3600
seconds_in_a_min = 60

try:
	for time_remaining in xrange(time_difference_in_sec, -1, -1):
		sys.stdout.write('\r')
		sys.stdout.write('Time until alarm: ')
		seconds_remaining = time_remaining

		days = seconds_remaining / seconds_in_a_day
		seconds_remaining -= days * seconds_in_a_day

		if days > 0:
			sys.stdout.write(str(days) + ' day(s), ')

		hours = seconds_remaining / seconds_in_an_hour
		seconds_remaining -= hours * seconds_in_an_hour

		if hours > 0 or days > 0:
			sys.stdout.write(str(hours) + ' hour(s), ')

		minutes = seconds_remaining / seconds_in_a_min
		seconds_remaining -= minutes * seconds_in_a_min

		if minutes > 0 or hours > 0 or days > 0:
			sys.stdout.write(str(minutes) + ' minute(s), ')

		seconds = seconds_remaining
		sys.stdout.write(str(seconds) + ' second(s)' + ' ' * 20)
		sys.stdout.flush()
		t.sleep(1)
except KeyboardInterrupt:
	print '\nAlarm canceled'
	quit()

# now, activate the alarm:
# get random youtube url
vf = open(video_file)
url = random.choice(vf.readlines())

# play video in new tab
webbrowser.open_new_tab(url)

# change audio output to monitor's speakers and set volume to max
p = subprocess.Popen(["C:\\NIRCMD\\SPEAKERS.BAT"])
stdout, stderr = p.communicate()

vf.close()


