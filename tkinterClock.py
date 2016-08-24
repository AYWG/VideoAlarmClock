import Tkinter

class Clock(Tkinter.Frame):

	def __init__(self, master):

		Tkinter.Frame.__init__(self, master)

		self.hourOptions = []
		self.hourOptions.append('Hour')
		for hour in range(24):
			self.hourOptions.append(str('{:02d}').format(hour))

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
		apply(Tkinter.OptionMenu, (master, self.hourVar) + tuple(self.hourOptions)).pack(side=Tkinter.LEFT)
		Tkinter.Label(master, text=':').pack(side=Tkinter.LEFT)
		apply(Tkinter.OptionMenu, (master, self.minuteVar) + tuple(self.minuteOptions)).pack(side=Tkinter.RIGHT)

	@property
	def selection(self):
		pass

			