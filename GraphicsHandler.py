import tkinter.filedialog
import tkinter as tk

class mainPanel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main panel")
        self.geometry("700x700")

        self.label = tk.Label(self, text = "This is the placeholder Main Panel")
        self.label.pack()

        self.button = tk.Button(self, text="Open Edit Panel")
        self.button['command'] = self.open_edit_panel
        self.button.pack()

        self.button = tk.Button(self, text = "Open A File")
        self.button['command'] = self.open_file
        self.button.pack(side=tk.TOP, pady="10")

        self.button = tk.Button(self, text="Save A File")
        self.button['command'] = self.save_file
        self.button.pack(side=tk.TOP)


    def open_edit_panel(self):
        self.editPanel = editPanel()

    def open_file(self):
        self.filename = tk.filedialog.askopenfilename(initialdir = "", title="Select the File to Open", filetypes=(("Database Files", ".xyz"), ("All Files", "*")))

    def save_file(self):
        print("not functional yet")


class editPanel(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Edit panel")
        self.geometry("300x90")

        descLabel = tk.Label(self, text="Description")
        descEntry = tk.Entry(self, width=31, bg="gray")

        accLabel = tk.Label(self, text="Account Name")
        accEntry = tk.Entry(self, width=31, bg="gray")

        passLabel = tk.Label(self, text="Account Password")
        passEntry = tk.Entry(self, width=31, bg="gray")

        descLabel.grid(row=0, column=0)
        descEntry.grid(row=0, column=1)
        accLabel.grid(row=1, column=0)
        accEntry.grid(row=1, column=1)
        passLabel.grid(row=2, column=0)
        passEntry.grid(row=2, column=1)

        self.button = tk.Button(self, text="Close Edit Panel")
        self.button['command'] = self.close_edit_panel
        self.button.grid(row=3, column=1, sticky='w')

        self.resizable(False, False)

    def close_edit_panel(self):
        self.destroy()

if __name__ == "__main__":
    app = mainPanel()
    app.mainloop()