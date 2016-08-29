import Tkinter
import ttk

# Builds a clock in Tkinter

class Clock(Tkinter.Frame):

	def __init__(self, master):

		Tkinter.Frame.__init__(self, master)

		# Initial option is 'Hour' (not actually valid)
		# Accepted options range from 0-23
		self.hourOptions = []
		self.hourOptions.append('Hour')
		for hour in range(24):
			self.hourOptions.append(str('{:02d}').format(hour))

		# Initial option is 'Minute' (not actually valid)
		# Accepted options range from 0-59
		self.minuteOptions = []
		self.minuteOptions.append('Minute')
		for minute in range(60):
			self.minuteOptions.append(str('{:02d}').format(minute))

		self.hourVar = Tkinter.StringVar(master)
		self.hourVar.set(self.hourOptions[0]) # default value

		self.minuteVar = Tkinter.StringVar(master)
		self.minuteVar.set(self.minuteOptions[0]) # default value

		self.buildClock(master)

	def buildClock(self, master):

		# Create clock using Combobox
		# Note: since both boxes are read only, when a value changes
		# (i.e. a ComboBoxSelected event) selection_clear() should be called;
		# otherwise they look a bit odd

		self.hourBox = ttk.Combobox(master, textvariable=self.hourVar, state='readonly')
		self.hourBox['values'] = self.hourOptions
		self.hourBox.bind('<<ComboboxSelected>>', self.clear_hourBox)
		self.hourBox.pack(side=Tkinter.LEFT)

		Tkinter.Label(master, text=':').pack(side=Tkinter.LEFT)
		
		self.minuteBox = ttk.Combobox(master, textvariable=self.minuteVar, state='readonly')
		self.minuteBox['values'] = self.minuteOptions
		self.minuteBox.bind('<<ComboboxSelected>>', self.clear_minuteBox)
		self.minuteBox.pack(side=Tkinter.RIGHT)

	def clear_hourBox(self, event):
		self.hourBox.selection_clear()

	def clear_minuteBox(self, event):
		self.minuteBox.selection_clear()

	@property
	def selection(self):
		return str(self.hourVar.get()) + ':' + str(self.minuteVar.get())
		

			