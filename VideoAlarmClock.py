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
import os

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
		
		Tkinter.Button(root, text='Select Date and Time', command=lambda:self.getdatetime(root)).grid(row=0, column=0, sticky=Tkinter.W, pady=20, padx=20)
		self.selected_datetime = Tkinter.StringVar(root)
		self.selected_datetime.set('Date and Time') 	# default text
		Tkinter.Label(root, textvariable=self.selected_datetime).grid(row=0, column=1, sticky=Tkinter.W)

		Tkinter.Button(root, text='Select Video File', command=self.askopenfilename).grid(row=1, column=0, sticky=Tkinter.W, padx=20, ipadx=13)
		# Display currently selected video file name to the right of the button
		self.selected_videofile = Tkinter.StringVar(root)
		self.selected_videofile.set('Video File')		# default text
		Tkinter.Label(root, textvariable=self.selected_videofile).grid(row=1, column=1, sticky=Tkinter.W)

		Tkinter.Button(root, text='Set Alarm', command=self.setalarm).grid(row=2, column=0, sticky=Tkinter.W)
		# When pressed, should check if selected date and time is valid; if not, a dialog should pop up to tell user to change the time

		# define options for opening or saving a file
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('Text Files', '.txt'), ('All Files', '.*')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = 'videos.txt'
		options['parent'] = root
		options['title'] = 'Select a file'

	def askopenfilename(self):
		# update the video file label with the file name
		self.selected_videofile.set(str(os.path.basename(tkFileDialog.askopenfilename(**self.file_opt))))

	def getdatetime(self, root):
		cd = CalendarDialog.CalendarDialog(root)
		if cd.result:
			self.selected_datetime.set(str(cd.result)[:-3])
			self.update_datetime_members(cd)
			td = TimeDialog.TimeDialog(root)
			if td.result:
				newtime = self.selected_datetime.get()[:-5] + td.result
				self.selected_datetime.set(newtime)
				self.hour = int(td.result[:2])
				self.minute = int(td.result[3:])

	def update_datetime_members(self, cd):
		self.year = int(cd.result.year)
		self.month = int(cd.result.month)
		self.day = int(cd.result.day)
		self.hour = int(cd.result.hour)
		self.minute = int(cd.result.minute)

	def setalarm(self):
		# will need to check if selected datetime and video file is valid

		# let's assume for now that they're valid
		# will need to extract datetime values like before
		current_time = datetime.now()
		alarm_time = datetime(self.year, self.month, self.day, self.hour, self.minute)
		time_difference_in_sec = int((alarm_time - current_time).total_seconds())

		# for now, just sleep until alarm_time
		t.sleep(time_difference_in_sec)

		# now, activate the alarm:
		# get random youtube url
		vf = open(self.selected_videofile.get())
		url = random.choice(vf.readlines())

		# play video in new tab
		webbrowser.open_new_tab(url)

		# change audio output to monitor's speakers and set volume to max
		p = subprocess.Popen(["C:\\NIRCMD\\SPEAKERS.BAT"])
		stdout, stderr = p.communicate()

		vf.close()

if __name__ == '__main__':
	root = Tkinter.Tk()
	root.title("Video Alarm Clock")
	VideoAlarmClockUI(root)
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


