import Tkinter
import tkSimpleDialog

class WarningDialog(tkSimpleDialog.Dialog):
	"""Dialog box that displays a warning message"""
	def body(self, master, arg = None):
		self.warning_message = arg
		self.label = Tkinter.Label(master, text=self.warning_message)
		self.label.pack()

	def buttonbox(self):
		box = Tkinter.Frame(self)

		w = Tkinter.Button(box, text="OK", width=10, command=self.ok, default=Tkinter.ACTIVE)
		w.pack(padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.ok)
		box.pack()

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()
		self.cancel()

# Demo code:
def main():
	root = Tkinter.Tk()
	root.wm_title("Warning")

	def onclick():
		wd = WarningDialog(root, arg='KEK')
		print wd.warning_message

	button = Tkinter.Button(root, text="Warning", command=onclick)
	button.pack()
	root.update()
	root.mainloop()

if __name__ == "__main__":
	main()				