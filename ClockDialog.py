import Tkinter
import tkinterClock
import tkSimpleDialog

class ClockDialog(tkSimpleDialog.Dialog):
	"""Dialog box that displays a clock and returns the selected time"""
	def body(self, master, arg = None):
		self.label = Tkinter.Label(master, text="Select a time")
		self.label.pack(side=Tkinter.TOP)
		self.clock = tkinterClock.Clock(master)
		self.clock.pack()
		return self.label

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
		self.result = self.clock.selection

# Demo code:
def main():
	root = Tkinter.Tk()
	root.wm_title("Select a time")

	def onclick():
		td = ClockDialog(root)
		print td.result

	button = Tkinter.Button(root, text="Select time", command=onclick)
	button.pack()
	root.update()
	root.mainloop()

if __name__ == "__main__":
	main()		