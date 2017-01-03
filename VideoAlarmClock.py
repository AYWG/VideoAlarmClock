# The top level script

import sys
from datetime import datetime
import time as t
import subprocess
import webbrowser
import random
import os
import const

# For the GUI
import Tkinter
import ttkcalendar
import tkSimpleDialog
import CalendarDialog
import ClockDialog
import WarningDialog
import tkFileDialog

class VideoAlarmClock:
	# basic constructor
	def __init__(self):
		pass

	# Checks if the given alarm time is invalid
	def is_invalid_alarm_datetime(self, alarm_datetime):
		if alarm_datetime <= datetime.now():
			return True
		return False

	def set_alarm(self, alarm_datetime):
		self.alarm_datetime = alarm_datetime

	def get_remaining_time_in_secs(self):
		if self.alarm_datetime:
			return int((self.alarm_datetime - datetime.now()).total_seconds())

	def activate_alarm(self, video_file_path):
		# get random youtube url
		vf = open(video_file_path)
		url = random.choice(vf.readlines())

		# play video in new tab
		webbrowser.open_new_tab(url)
		# change audio output to monitor's speakers and set volume to max
		p = subprocess.Popen([const.change_speakers_script_path])
		stdout, stderr = p.communicate()

		vf.close()

class VideoAlarmClockUI(Tkinter.Frame):

	def __init__(self, root):
		self.root = root
		Tkinter.Frame.__init__(self, root)
		# set fixed window size
		root.minsize(width=const.window_width, height=const.window_height)
		root.maxsize(width=const.window_width, height=const.window_height)

		top_container = Tkinter.Frame(root)
		top_container.pack(side='top', fill='both', expand=True)
		bottom_container = Tkinter.Frame(root)
		bottom_container.pack(side='top', fill='both', expand=True)

		self.alarm_clock = VideoAlarmClock()
		
		# create StringVar object that represents the UI's currently selected date and time
		self.selected_datetime = Tkinter.StringVar(root)
		self.selected_datetime.set(const.datetime_default) 	
				
		# create StringVar object that represents the UI's currently selected video file
		self.selected_videofile = Tkinter.StringVar(root)
		self.selected_videofile.set(const.videofile_default)

		# create StringVar object that represents the UI's current video alarm clock "state"
		self.alarm_state_text = Tkinter.StringVar(root)
		self.alarm_state_text.set(const.alarmstate_default)
		self.alarm_state = 0

		self.time_remaining = Tkinter.StringVar(root)

		# define options for opening a file
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('Text Files', '.txt')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = 'videos.txt'
		options['parent'] = root
		options['title'] = 'Select a file'

		# Set up the interface with the necessary widgets
		Tkinter.Button(top_container, text='Select Date and Time', command=self.get_datetime).grid(row=0, column=0, sticky=Tkinter.W, padx=20, pady=20)
		Tkinter.Label(top_container, textvariable=self.selected_datetime, anchor=Tkinter.W).grid(row=0, column=1, sticky=Tkinter.W)

		Tkinter.Button(top_container, text='Select Video File', command=self.get_videofile).grid(row=1, column=0, sticky=Tkinter.W, padx=20, ipadx=13)
		Tkinter.Label(top_container, textvariable=self.selected_videofile).grid(row=1, column=1, sticky=Tkinter.W)	

		# One button that alternates between const.alarmstate_default and const.alarm_cancel
		Tkinter.Button(bottom_container, textvariable=self.alarm_state_text, command=self.set_alarm).pack(padx=66, pady=15, ipadx=50)
		Tkinter.Label(bottom_container, textvariable=self.time_remaining, wraplength=200).pack(padx=20, pady=10)

	def get_videofile(self):
		# get the path of the file
		path_of_file = tkFileDialog.askopenfilename(**self.file_opt)
		# only update video file label with file name if user clicked "Open"
		if path_of_file: 
			if os.path.getsize(path_of_file) == 0:
				WarningDialog.WarningDialog(self.root, arg=const.emptyfile_warning)
			else:
				self.selected_videofile_path = path_of_file
				self.selected_videofile.set(str(os.path.basename(path_of_file)))

	def get_datetime(self):
		# open up the calendar in a new dialog
		cal = CalendarDialog.CalendarDialog(self.root)
		if cal.result:
			self.selected_datetime.set(str(cal.result)[:-3])
			self.update_datetime_members(cal)

			# open up the clock in a new dialog
			clk = ClockDialog.ClockDialog(self.root)
			if clk.result:
				newtime = self.selected_datetime.get()[:-5] + clk.result
				self.selected_datetime.set(newtime)
				self.hour = int(clk.result[:2])
				self.minute = int(clk.result[3:])

	def update_datetime_members(self, cal):
		self.year = int(cal.result.year)
		self.month = int(cal.result.month)
		self.day = int(cal.result.day)
		self.hour = int(cal.result.hour)
		self.minute = int(cal.result.minute)

	def set_alarm(self):
		if self.alarm_state == 0:
			# first, need to check if date/time and video file have been selected
			if self.selected_datetime.get() == const.datetime_default:
				WarningDialog.WarningDialog(self.root, arg=const.datetime_warning)
				return
			if self.selected_videofile.get() == const.videofile_default:
				WarningDialog.WarningDialog(self.root, arg=const.videofile_warning)
				return

			# then, need to check if selected datetime and video file is valid
			alarm_datetime = datetime(self.year, self.month, self.day, self.hour, self.minute)
			if self.alarm_clock.is_invalid_alarm_datetime(alarm_datetime):
				WarningDialog.WarningDialog(self.root, arg=const.future_warning)
				return

			self.alarm_clock.set_alarm(alarm_datetime)
			self.alarm_state_text.set(const.alarm_cancel)
			self.alarm_state = 1
			self.countdown_alarm()
		else:
			self.alarm_state = 0

	def countdown_alarm(self):
		# Alarm finished (reset)
		if self.alarm_clock.get_remaining_time_in_secs() <= 0:
			self.time_remaining.set(const.alarm_finished)
			self.alarm_state = 0
			self.alarm_state_text.set(const.alarmstate_default)
			self.alarm_clock.activate_alarm(self.selected_videofile.get())
		# Alarm has been canceled (reset)
		elif self.alarm_state == 0:
			self.alarm_state_text.set(const.alarmstate_default)
			self.time_remaining.set(const.alarm_canceled)
		# Alarm is counting down
		else:
			seconds_remaining = self.alarm_clock.get_remaining_time_in_secs()
			tr = 'Time until alarm: '

			days = seconds_remaining / const.seconds_in_a_day
			seconds_remaining -= days * const.seconds_in_a_day

			if days > 0:
				tr += str(days) + ' day(s), '

			hours = seconds_remaining / const.seconds_in_an_hour
			seconds_remaining -= hours * const.seconds_in_an_hour

			if hours > 0 or days > 0:
				tr += str(hours) + ' hour(s), '

			minutes = seconds_remaining / const.seconds_in_a_min
			seconds_remaining -= minutes * const.seconds_in_a_min

			if minutes > 0 or hours > 0 or days > 0:
				tr += str(minutes) + ' minute(s), '

			seconds = seconds_remaining
			tr += str(seconds) + ' second(s)'
			self.time_remaining.set(tr)

			# Wait 1000 ms before calling itself again.
			# Need to use after method (rather than sleep) to
			# avoid issues with mainloop()
			self.after(1000, self.countdown_alarm)


if __name__ == '__main__':
	# If only argument is script name, run GUI
	if len(sys.argv) == 1:
		root = Tkinter.Tk()
		root.title("Video Alarm Clock")
		VideoAlarmClockUI(root)
		root.mainloop()
		quit()
##### otherwise, run command-line version ############################################################
	else:
		# Check number of arguments
		if len(sys.argv) != 6:
			print "Note: to use the GUI, simply run the script without any arguments.\n"
			print "Invalid number of arguments."
			print "Usage: python VideoAlarmClock.py [year] [month] [day] [time in 24-hour format] [ path/to/video_file.txt ]"
			print "For example, to set alarm clock for 00:30 on June 24th 2016 using videos.txt (stored on C drive), run:"
			print "python VideoAlarmClock.py 2016 6 24 00:30 C:/videos.txt"
			quit()

		script, year, month, day, time, video_file_path = sys.argv

		if not os.path.isfile(video_file_path):
			print "Error: file does not exist."
			quit()

		if os.path.getsize(video_file_path) == 0:
			print "Error: empty file."
			quit()

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

		alarm_clock = VideoAlarmClock()
		alarm_datetime = datetime(alarm_year, alarm_month, alarm_day, alarm_hour, alarm_min)
		if alarm_clock.is_invalid_alarm_datetime(alarm_datetime):
			print "The provided time/date of the alarm clock is in the past."
			print "Please provide a time and date in the future."
			quit()

		alarm_clock.set_alarm(alarm_datetime)

		try:
			while alarm_clock.get_remaining_time_in_secs() > 0:
				sys.stdout.write('\r')
				sys.stdout.write('(Press CTRL + C to cancel) --- Time until alarm: ')
				seconds_remaining = alarm_clock.get_remaining_time_in_secs()

				days = seconds_remaining / const.seconds_in_a_day
				seconds_remaining -= days * const.seconds_in_a_day

				if days > 0:
					sys.stdout.write(str(days) + ' day(s), ')

				hours = seconds_remaining / const.seconds_in_an_hour
				seconds_remaining -= hours * const.seconds_in_an_hour

				if hours > 0 or days > 0:
					sys.stdout.write(str(hours) + ' hour(s), ')

				minutes = seconds_remaining / const.seconds_in_a_min
				seconds_remaining -= minutes * const.seconds_in_a_min

				if minutes > 0 or hours > 0 or days > 0:
					sys.stdout.write(str(minutes) + ' minute(s), ')

				seconds = seconds_remaining
				sys.stdout.write(str(seconds) + ' second(s)' + ' ' * 20)
				sys.stdout.flush()
				t.sleep(1)
		except KeyboardInterrupt:
			print '\nAlarm Canceled'
			quit()

		print "\nTime's Up!"
		alarm_clock.activate_alarm(video_file_path)



