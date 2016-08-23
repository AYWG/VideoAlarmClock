import Tkinter
import ttkcalendar

import tkSimpleDialog

class TimeDialog(tkSimpleDialog.Dialog):
	"""Dialog box that displays a clock and returns the selected time"""
	def body(self, master):
		self.calendar = ttkcalendar.Calendar(master)
		self.calendar.pack()

	def buttonbox(self):
		box = Tkinter.Frame(self)

		w = Tkinter.Button(box, text="OK", width=10, command=self.ok, default=Tkinter.ACTIVE)
		w.pack(side=Tkinter.LEFT, padx=5, pady=5)
		w = Tkinter.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=Tkinter.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack()

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()

	def apply(self):
		self.result = self.calendar.selection