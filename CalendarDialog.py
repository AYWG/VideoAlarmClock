import Tkinter
import ttkcalendar

import tkSimpleDialog

class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.label = Tkinter.Label(master, text="Select a date")
        self.label.pack(side=Tkinter.TOP)
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()
        return self.label

    def buttonbox(self):
        box = Tkinter.Frame(self)

        w = Tkinter.Button(box, text="Next", width=10, command=self.ok, default=Tkinter.ACTIVE)
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

        self.destroy()
    
    def apply(self):
        self.result = self.calendar.selection

# Demo code:
def main():
    root = Tkinter.Tk()
    root.wm_title("Select a date")

    def onclick():
        cd = CalendarDialog(root)
        print cd.result

    button = Tkinter.Button(root, text="Select date", command=onclick)
    button.pack()
    root.update()

    root.mainloop()


if __name__ == "__main__":
    main()