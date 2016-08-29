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
import ttkcalendar
import tkSimpleDialog
import CalendarDialog
import ClockDialog
import WarningDialog
import tkFileDialog

seconds_in_a_day = 86400
seconds_in_an_hour = 3600
seconds_in_a_min = 60

class VideoAlarmClock:

	def __init__(self):
		# when I create a VideoAlarmClock object, what should I initialize it with, if anything?
		pass

	def is_invalid_alarm_datetime(self, alarm_datetime):
		if alarm_datetime <= datetime.now():
			return True
		return False

	def set_alarm(self, alarm_datetime):
		self.alarm_datetime = alarm_datetime

	def get_remaining_time_in_secs(self):
		if self.alarm_datetime:
			return int((self.alarm_datetime - datetime.now()).total_seconds())

	def activate_alarm(self, video_file_name):
		# get random youtube url
		vf = open(video_file_name)
		url = random.choice(vf.readlines())

		# play video in new tab
		webbrowser.open_new_tab(url)
		# change audio output to monitor's speakers and set volume to max
		p = subprocess.Popen(["C:\\NIRCMD\\SPEAKERS.BAT"])
		stdout, stderr = p.communicate()

		vf.close()

class VideoAlarmClockUI(Tkinter.Frame):

	def __init__(self, root):

		Tkinter.Frame.__init__(self, root)

		# set fixed window size
		root.minsize(width=300, height=200)
		root.maxsize(width=300, height=200)

		self.alarm_clock = VideoAlarmClock()
		
		# create StringVar object that represents the UI's currently selected date and time
		self.selected_datetime = Tkinter.StringVar(root)
		self.selected_datetime.set('Date and Time') 	# default text
				
		# create StringVar object that represents the UI's currently selected video file
		self.selected_videofile = Tkinter.StringVar(root)
		self.selected_videofile.set('Video File')		# default text

		# create StringVar object that represents the UI's current video alarm clock "state"
		self.alarm_state = Tkinter.StringVar(root)
		self.alarm_state.set('Set Alarm')

		self.time_remaining = Tkinter.StringVar(root)
		self.time_remaining.set('Blank')

		# define options for opening a file
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('Text Files', '.txt'), ('All Files', '.*')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = 'videos.txt'
		options['parent'] = root
		options['title'] = 'Select a file'

		self.__initUI(root)

	# Sets up the interface with the necessary widgets
	def __initUI(self, root):

		Tkinter.Button(root, text='Select Date and Time', command=lambda:self.get_datetime(root)).grid(row=0, column=0, sticky=Tkinter.W, padx=20, pady=20)
		Tkinter.Label(root, textvariable=self.selected_datetime).grid(row=0, column=1, sticky=Tkinter.W)

		Tkinter.Button(root, text='Select Video File', command=self.get_videofile).grid(row=1, column=0, sticky=Tkinter.W, padx=20, ipadx=13)
		Tkinter.Label(root, textvariable=self.selected_videofile).grid(row=1, column=1, sticky=Tkinter.W)	

		# One button that alternates between 'Set Alarm' and 'Cancel Alarm'
		Tkinter.Button(root, textvariable=self.alarm_state, command=self.set_alarm).grid(row=3, columnspan=2, sticky=Tkinter.E, padx=66, pady=20, ipadx=50)
		#Tkinter.Button(root, text='Cancel Alarm', command=self.set_alarm).grid(row=3, column=1, sticky=Tkinter.W, ipadx=18)

		Tkinter.Label(root, textvariable=self.time_remaining).grid(row=4, columnspan=2, sticky=Tkinter.W + Tkinter.E, padx=20)

	def get_videofile(self):

		# get the path of the file
		path_of_file = tkFileDialog.askopenfilename(**self.file_opt)
		# only update video file label with file name if user clicked "Open"
		if path_of_file: 
			self.selected_videofile.set(str(os.path.basename(path_of_file)))

	def get_datetime(self, root):
		# open up the calendar in a new dialog
		cd = CalendarDialog.CalendarDialog(root)
		if cd.result:
			self.selected_datetime.set(str(cd.result)[:-3])
			self.update_datetime_members(cd)

			td = ClockDialog.ClockDialog(root)
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

	def set_alarm(self):
		# will need to check if selected datetime and video file is valid
		alarm_datetime = datetime(self.year, self.month, self.day, self.hour, self.minute)
		if self.alarm_clock.is_invalid_alarm_datetime(alarm_datetime):
			WarningDialog.WarningDialog(root, arg='Error: Invalid date and/or time')
			return

		# let's assume for now that they're valid
		# will need to extract datetime values like before
		#current_time = datetime.now()
		#alarm_time = datetime(self.year, self.month, self.day, self.hour, self.minute)
		#time_difference_in_sec = int((alarm_time - current_time).total_seconds())
		self.alarm_clock.set_alarm(alarm_datetime)

		self.countdown_alarm()

	def countdown_alarm(self):
		if self.alarm_clock.get_remaining_time_in_secs() <= 0:
			self.time_remaining.set("Time's up!")
			self.alarm_clock.activate_alarm(self.selected_videofile.get())
		else:
			seconds_remaining = self.alarm_clock.get_remaining_time_in_secs()
			tr = 'Time until alarm: '

			days = seconds_remaining / seconds_in_a_day
			seconds_remaining -= days * seconds_in_a_day

			if days > 0:
				tr += str(days) + ' day(s), '

			hours = seconds_remaining / seconds_in_an_hour
			seconds_remaining -= hours * seconds_in_an_hour

			if hours > 0 or days > 0:
				tr += str(hours) + ' hour(s), '

			minutes = seconds_remaining / seconds_in_a_min
			seconds_remaining -= minutes * seconds_in_a_min

			if minutes > 0 or hours > 0 or days > 0:
				tr += str(minutes) + ' minute(s), '

			seconds = seconds_remaining
			tr += str(seconds) + ' second(s)'
			self.time_remaining.set(tr)
			self.after(1000, self.countdown_alarm)


if __name__ == '__main__':
	if len(sys.argv) == 1:
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

current_time = datetime.now()
alarm_time = datetime(alarm_year, alarm_month, alarm_day, alarm_hour, alarm_min)

if alarm_time <= current_time:
	print "The provided time/date of the alarm clock is in the past."
	print "Please provide a time and date in the future."
	quit()

time_difference_in_sec = int((alarm_time - current_time).total_seconds())

seconds_in_a_day = 86400
seconds_in_an_hour = 3600
seconds_in_a_min = 60

try:
	for time_remaining in xrange(time_difference_in_sec, -1, -1):
		sys.stdout.write('\r')
		sys.stdout.write('(Press CTRL + C to cancel) --- Time until alarm: ')
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


