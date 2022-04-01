import tkinter.filedialog
import tkinter as tk
import cryptography

def openFile(file_name):
    file = open(file_name,'r')
    file_contents = []
    for line in file:
        file_contents.append(line.split(' '))
    file.close()
    return file_contents

class mainPanel(tk.Tk):
    def __init__(self):
        super().__init__()

# ------------------------------- Program Info ------------------------------- #

        self.databaseContents = None
        self.accountInfo = []
        self.title("SecuriSimplex Password Manager")
        self.geometry("800x900")
        self.pendingChanges = False

        #self.label = tk.Label(self, text = "This is the placeholder Main Panel")
        #self.label.pack()

# ------------------------------- Program Info ------------------------------- #

# ------------------------------- Creating Top Bar Buttons ------------------------------- #

        self.EditSaveFrame = tk.Frame(self, height="100", relief="ridge", pady="5")  #Creating frame for open file and save file widgets
        self.EditSaveFrame.pack(fill="x", padx="5") #Fill entire x axis
        self.EditSaveFrame.pack_propagate(0) #Force the width and height

        self.createButton = tk.Button(self.EditSaveFrame, text="Create A File", relief="groove")  # Button for Creating a File
        self.createButton['command'] = self.create_file
        self.createButton.pack(side="left", fill="both", expand=True, padx="0")

        self.openButton = tk.Button(self.EditSaveFrame, text = "Open A File", relief="groove")   #Button for Opening a File
        self.openButton['command'] = self.open_file
        self.openButton.pack(side="left", fill="both", expand=True, padx="0")

        self.saveButton = tk.Button(self.EditSaveFrame, text="Save A File", relief="groove")     #Button for Saving a File
        self.saveButton['command'] = self.save_file
        self.saveButton.pack(side="left", fill="both", expand=True, padx="0")

        self.abortButton = tk.Button(self.EditSaveFrame, text="Abort Changes", relief="groove")     #Button for Aborting Changes to a File
        self.abortButton['command'] = self.reopen_file
        self.abortButton['state'] = "disabled"
        self.abortButton.pack(side="left", fill="both", expand=True, padx="0")

# ------------------------------- Creating Top Bar Buttons ------------------------------- #

# -------------------------------- Creating Add New Entry -------------------------------- #

        self.addEntryButton = tk.Button(self, text="Add New Entry", height = 6, relief="groove")  # Button for Adding New Entry to a File
        self.addEntryButton['command'] = self.add_database_entry
        #self.addEntryButton['state'] = "disabled"
        self.addEntryButton.pack(side="top", fill="x", padx="0")

# -------------------------------- Creating Add New Entry -------------------------------- #

# ------------------------------- Creating Data Buttons ------------------------------- #

        self.dataFrameContainer = tk.Frame(self, bg="gray", relief="ridge")
        self.dataFrameContainer.pack(expand=1, fill="both", padx="5")  # Fill entire x axis
        self.dataFrameContainer.pack_propagate(0)  # Force the width and height

        self.dataFrameCanvas = tk.Canvas(self.dataFrameContainer, bg="gray")
        self.dataFrameScrollbar = tk.Scrollbar(self, orient="vertical", command=self.dataFrameCanvas.yview)

        self.dataFrame = tk.Frame(self.dataFrameCanvas, bg="gray", relief="ridge")  # Creating frame for data entries
        #self.dataFrame.pack(expand=1, fill="both", padx="5", pady="5")  # Fill entire x axis
        #self.dataFrame.pack_propagate(0)  # Force the width and height

        self.dataFrameScrollbar = tk.Scrollbar(self.dataFrameContainer, orient="vertical", command=self.dataFrameCanvas.yview)

        self.dataFrameCanvas.update_idletasks()
        self.dataFrameCanvas.configure(scrollregion=self.dataFrame.bbox("all"), yscrollcommand=self.dataFrameScrollbar.set)

        self.dataFrameCanvas.pack(fill="both", expand=True, side="left", padx="2", pady="2")
        self.dataFrameCanvas.create_window(30, 0, anchor="center", window=self.dataFrame, tags="dataFrame")
        self.dataFrameScrollbar.pack(fill="y", side="right")

# ------------------------------- Creating Data Buttons ------------------------------- #

        self.resizable(False, False)  # Prevents resizing the window, may remove later

    def open_edit_panel(self, num):
        self.editPanel = editPanel(self.databaseContents, num)

    def open_file(self):
        self.filename = tk.filedialog.askopenfilename(initialdir = ".", title="Select the File to Open", filetypes=(("All Files", "*"), ("Database Files", ".xyz"), ))
        #self.keyfilename = tk.filedialog.askopenfilename(initialdir = ".", title="Select Key Used to Decrypt", filetypes = (("All Files", "*"), ("Keys", ".key"), ))
        self.databaseContents = openFile(self.filename)
        self.create_database_panel()

    def reopen_file(self):
        self.databaseContents = openFile(self.filename)
        self.create_database_panel()
        self.abortButton['state'] = "disabled"

    def save_file(self):
        try:
            file = open(self.filename, 'w')
            for line in self.databaseContents:
                file.write(line[0] + " ")
                file.write(line[1] + " ")
                file.write(line[2].rstrip() + "\n")
            #self.create_database_panel()
            self.pendingChanges = False
            self.abortButton['state'] = "disabled"
        except AttributeError:
            print("Must Load File First")

    def create_file(self):
        self.databaseContents = [["", "", ""]]
        self.create_database_panel()

    def add_database_entry(self):
        self.databaseContents.append(["", "", ""])
        self.create_database_panel()

    def create_database_panel(self):
        for element in self.accountInfo:
            element.destroy()
        if self.databaseContents is not None:
            for num in range(0, len(self.databaseContents)):
                newButton = tk.Button(self.dataFrame, bg="white", text=self.databaseContents[num][0], height="5", relief="ridge", command=lambda a=num: self.open_edit_panel(a))
                newButton.pack(fill="x", expand=True)
                self.accountInfo.append(newButton)  # Creating frame for data entries
            #for num in range(0, len(self.accountInfo)):
            #    self.accountInfo[num].pack(fill="x", expand=False, padx="5")  # Fill entire x axis
            #    self.accountInfo[num].pack_propagate(0)  # Force the width and height

        self.dataFrameCanvas.itemconfigure("dataFrame", width=self.winfo_width() - 35, anchor="center")
        self.dataFrameCanvas.update_idletasks()
        self.dataFrameCanvas.config(scrollregion=self.dataFrameCanvas.bbox("all"))


class editPanel(tk.Toplevel):
    def __init__(self, databaseContent, num):
        super().__init__()

        self.title("Edit panel")
        self.geometry("300x90")

        self.targetDatabaseContent = databaseContent[num]  # Each edit panel only stores the info necessary for its own use

        self.descLabel = tk.Label(self, text="Description")
        self.descEntry = tk.Entry(self, width=31, bg="gray")
        self.descEntry.insert(0, "**********")
        self.descEntry['state'] = 'disabled'

        self.accLabel = tk.Label(self, text="Account Name")
        self.accEntry = tk.Entry(self, width=31, bg="gray")
        self.accEntry.insert(0, "**********")
        self.accEntry['state'] = 'disabled'

        self.passLabel = tk.Label(self, text="Account Password")
        self.passEntry = tk.Entry(self, width=31, bg="gray")
        self.passEntry.insert(0, "**********")
        self.passEntry['state'] = 'disabled'

        self.descLabel.grid(row=0, column=0)
        self.descEntry.grid(row=0, column=1)
        self.accLabel.grid(row=1, column=0)
        self.accEntry.grid(row=1, column=1)
        self.passLabel.grid(row=2, column=0)
        self.passEntry.grid(row=2, column=1)

        self.unhideText = tk.IntVar()
        self.censorCheckbox = tk.Checkbutton(self, text='Unhide Text', variable=self.unhideText, onvalue=1, offvalue=0, command=self.toggle_text)
        self.censorCheckbox.grid(row=3, column=1)

        self.button = tk.Button(self, text="Close")
        self.button['command'] = lambda a=num: self.close_edit_panel(a)
        self.button.grid(row=3, column=0, sticky='w')

        self.resizable(False, False)

    def close_edit_panel(self, num):
        parentName = self.winfo_parent()
        parentWindow = self.nametowidget(parentName)

        if self.unhideText.get() == 1:
            if parentWindow.databaseContents[num][0] != self.descEntry.get() or parentWindow.databaseContents[num][1] != self.accEntry.get() or parentWindow.databaseContents[num][2].rstrip() != self.passEntry.get():
                parentWindow.pendingChanges = True
            parentWindow.databaseContents[num][0] = self.descEntry.get()
            parentWindow.databaseContents[num][1] = self.accEntry.get()
            parentWindow.databaseContents[num][2] = self.passEntry.get()
            parentWindow.create_database_panel()

        elif self.unhideText == 0:
            self.unhideText.set(1)
            self.toggle_text()
            if parentWindow.databaseContents[num][0] != self.descEntry.get() or parentWindow.databaseContents[num][1] != self.accEntry.get() or parentWindow.databaseContents[num][2].rstrip() != self.passEntry.get():
                parentWindow.pendingChanges = True
            parentWindow.databaseContents[num][0] = self.descEntry.get()
            parentWindow.databaseContents[num][1] = self.accEntry.get()
            parentWindow.databaseContents[num][2] = self.passEntry.get()
            parentWindow.create_database_panel()

        if parentWindow.pendingChanges == True:
            parentWindow.abortButton['state'] = "active"
        self.destroy()

    def toggle_text(self):
        if self.unhideText.get() == 0:
            self.descEntry.delete(0, "end")
            self.descEntry.insert(0, "**********")
            self.descEntry['state'] = 'disabled'

            self.accEntry.delete(0, "end")
            self.accEntry.insert(0, "**********")
            self.accEntry['state'] = 'disabled'

            self.passEntry.delete(0, "end")
            self.passEntry.insert(0, "**********")
            self.passEntry['state'] = 'disabled'

        if self.unhideText.get() == 1:
            self.descEntry['state'] = 'normal'
            self.descEntry.delete(0, "end")
            self.descEntry.insert(0, self.targetDatabaseContent[0])

            self.accEntry['state'] = 'normal'
            self.accEntry.delete(0, "end")
            self.accEntry.insert(0, self.targetDatabaseContent[1])

            self.passEntry['state'] = 'normal'
            self.passEntry.delete(0, "end")
            self.passEntry.insert(0, self.targetDatabaseContent[2].rstrip())


    # Note: Eventually flag user for confirmation for closing application



if __name__ == "__main__":
    app = mainPanel()
    app.update()
    app.mainloop()