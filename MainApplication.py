import tkinter.filedialog
import tkinter as tk
from cryptography.fernet import Fernet

def openFile(file_name, key_file_name):
    file = open(file_name, 'rb')
    keyFile = open(key_file_name, 'rb')
    key = keyFile.readline()
    decryptor = Fernet(key)
    file_contents = []

    for line in file:
        contents = decryptor.decrypt(line.strip())
        list_of_contents = contents.decode("utf-8").rstrip().split(' ')
        file_contents.append(list_of_contents)
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
        self.protocol("WM_DELETE_WINDOW", self.closing_window)
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
        self.saveButton['state'] = 'disabled'
        self.saveButton.pack(side="left", fill="both", expand=True, padx="0")

        self.abortButton = tk.Button(self.EditSaveFrame, text="Abort Changes", relief="groove")     #Button for Aborting Changes to a File
        self.abortButton['command'] = self.reopen_file
        self.abortButton['state'] = "disabled"
        self.abortButton.pack(side="left", fill="both", expand=True, padx="0")

# ------------------------------- Creating Top Bar Buttons ------------------------------- #

# -------------------------------- Creating Add New Entry -------------------------------- #

        self.addEntryButton = tk.Button(self, text="Add New Entry", height = 6, relief="groove")  # Button for Adding New Entry to a File
        self.addEntryButton['command'] = self.add_database_entry
        self.addEntryButton['state'] = "disabled"
        self.addEntryButton.pack(side="top", fill="x", padx="0")

# -------------------------------- Creating Add New Entry -------------------------------- #

# ------------------------------- Creating Data Buttons ------------------------------- #

        self.dataFrameContainer = tk.Frame(self, bg="gray", relief="ridge")
        self.dataFrameContainer.pack(expand=1, fill="both", padx="5")  # Fill entire x axis
        self.dataFrameContainer.pack_propagate(0)  # Force the width and height

        self.dataFrameCanvas = tk.Canvas(self.dataFrameContainer, bg="gray")
        self.dataFrameScrollbar = tk.Scrollbar(self, orient="vertical", command=self.dataFrameCanvas.yview)

        self.dataFrame = tk.Frame(self.dataFrameCanvas, bg="gray", relief="ridge")  # Creating frame for data entries

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
        self.keyfilename = tk.filedialog.askopenfilename(initialdir = ".", title="Select Key Used to Decrypt", filetypes = (("All Files", "*"), ("Keys", ".key"), ))
        if self.filename is not None and self.filename != "" and self.keyfilename is not None and self.keyfilename != "":
            self.databaseContents = openFile(self.filename, self.keyfilename)
            self.create_database_panel()
            self.addEntryButton['state'] = 'active'
            self.saveButton['state'] = 'active'
            self.title("SecuriSimplex Password Manager - " + self.filename.split("/")[len(self.filename.split("/")) - 1])

    def reopen_file(self):
        try:
            self.databaseContents = openFile(self.filename, self.keyfilename)
            self.create_database_panel()
            self.abortButton['state'] = "disabled"
        except (AttributeError, FileNotFoundError, TypeError) as error:
            self.databaseContents = [["", "", ""]]
            self.create_database_panel()

    def save_file(self):
        try:
            file = open(self.filename, 'wb')
        except (AttributeError, FileNotFoundError, TypeError) as error:
            self.filename = tk.filedialog.asksaveasfilename(initialdir = ".", title="Select the File to Open", filetypes=(("Database Files", ".xyz"), ))
            if self.filename == "":
                self.filename = "default"
        file = open(self.filename, 'wb')
        key = Fernet.generate_key()
        encryptor = Fernet(key)
        keyFile = open(self.filename + ".key", "wb")
        keyFile.write(key)
        keyFile.close()

        length_of_database_contents = len(self.databaseContents)
        num = 0
        while num < length_of_database_contents:
            if self.databaseContents[num][0] != "" and self.databaseContents[num][1] != "" and self.databaseContents[num][2] != "":
                stuff_to_write = encryptor.encrypt((self.databaseContents[num][0] + " " + self.databaseContents[num][1] + " " + self.databaseContents[num][2].rstrip() + "\n").encode())
                file.write(stuff_to_write + b'\n')
            #stuff_to_write = encryptor.encrypt((self.databaseContents[num][0] + " " + self.databaseContents[num][1] + " " + self.databaseContents[num][2].rstrip() + "\n").encode())
            #file.write(stuff_to_write + b'\n')
            num += 1
        file.close()
        self.create_database_panel()
        self.pendingChanges = False
        self.abortButton['state'] = "disabled"
        self.title("SecuriSimplex Password Manager - " + self.filename.split("/")[len(self.filename.split("/")) - 1])

        """
        except (AttributeError, FileNotFoundError, TypeError) as error:
            self.filename = tk.filedialog.asksaveasfilename(initialdir = ".", title="Select the File to Open", filetypes=(("Database Files", ".xyz"), ))
            if self.filename == "":
                self.filename = "default"
            file = open(self.filename, 'wb')

            key = Fernet.generate_key()
            encryptor = Fernet(key)
            keyFile = open(self.filename + ".key", "wb")
            keyFile.write(key)
            keyFile.close()

            length_of_database_contents = len(self.databaseContents)
            #print(self.databaseContents)
            #print(length_of_database_contents)
            num = 0
            while num < length_of_database_contents:
                if self.databaseContents[num][0] != "" and self.databaseContents[num][1] != "" and self.databaseContents[num][2] != "":
                    stuff_to_write = encryptor.encrypt((self.databaseContents[num][0] + " " + self.databaseContents[num][1] + " " + self.databaseContents[num][2].rstrip() + "\n").encode())
                    file.write(stuff_to_write + b'\n')
                num += 1
            file.close()
            self.create_database_panel()
            self.pendingChanges = False
            self.abortButton['state'] = "disabled"
            self.title("SecuriSimplex Password Manager - " + self.filename.split("/")[len(self.filename.split("/")) - 1])
    """
    def closing_window(self):
        if self.pendingChanges == False:
            self.destroy()
        else:
            self.confirmationPanel = confirmationPanel()

    def create_file(self):
        self.databaseContents = [["", "", ""]]
        self.create_database_panel()
        self.addEntryButton['state'] = 'active'
        self.saveButton['state'] = 'active'
        self.filename = ""

    def add_database_entry(self):
        self.databaseContents.append(["", "", ""])
        self.create_database_panel()

    def create_database_panel(self):
        for element in self.accountInfo:
            element.destroy()
        if self.databaseContents is not None:
            for num in range(0, len(self.databaseContents)):
                newButton = tk.Button(self.dataFrame, bg="white", text=self.databaseContents[num][0], height="5", relief="ridge", command=lambda a=num: self.open_edit_panel(a))
                newButton.pack(side = "top", fill="x", expand=True)
                self.accountInfo.append(newButton)  # Creating frame for data entries
        self.dataFrameCanvas.itemconfigure("dataFrame", width=self.winfo_width() - 35, anchor="n")
        self.dataFrameCanvas.update_idletasks()
        self.dataFrameCanvas.config(scrollregion=self.dataFrameCanvas.bbox("all"))

class confirmationPanel(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Confirmation Panel")
        self.geometry("300x110")

        self.textLabel = tk.Label(self, text="You have unsaved changes. Are you sure you would like to close?", wraplength=250)
        self.textLabel.pack(side="top")

        self.yesButton = tk.Button(self, bg="white", text="Yes", width=10, relief="ridge", command=lambda a=0: self.nametowidget(self.winfo_parent()).destroy())
        self.noButton = tk.Button(self, bg="white", text="No", width=10, relief="ridge", command=lambda a=0: self.destroy())
        self.yesButton.pack(side="left", padx="20")
        self.noButton.pack(side="right", padx="20")

        self.resizable(False, False)

class editPanel(tk.Toplevel):
    def __init__(self, databaseContent, num):
        super().__init__()

        self.title("Edit panel")
        self.geometry("300x110")

        self.targetDatabaseContent = databaseContent[num]  # Each edit panel only stores the info necessary for its own use

        self.descLabel = tk.Label(self, text="Description")
        self.descEntry = tk.Entry(self, width=25, bg="gray")
        self.descEntry.insert(0, "**********")
        self.descEntry['state'] = 'disabled'

        self.accLabel = tk.Label(self, text="Account Name")
        self.accEntry = tk.Entry(self, width=25, bg="gray")
        self.accEntry.insert(0, "**********")
        self.accEntry['state'] = 'disabled'

        self.passLabel = tk.Label(self, text="Account Password")
        self.passEntry = tk.Entry(self, width=25, bg="gray")
        self.passEntry.insert(0, "**********")
        self.passEntry['state'] = 'disabled'

        self.copyButton1 = tk.Button(self, bg="white", text="Copy", relief="ridge", command=lambda a=0: self.copy_to_clipboard(a))
        self.copyButton2 = tk.Button(self, bg="white", text="Copy", relief="ridge", command=lambda a=1: self.copy_to_clipboard(a))
        self.copyButton3 = tk.Button(self, bg="white", text="Copy", relief="ridge", command=lambda a=2: self.copy_to_clipboard(a))

        self.descLabel.grid(row=0, column=0)
        self.descEntry.grid(row=0, column=1)
        self.copyButton1.grid(row=0, column=2)
        self.accLabel.grid(row=1, column=0)
        self.accEntry.grid(row=1, column=1)
        self.copyButton2.grid(row=1, column=2)
        self.passLabel.grid(row=2, column=0)
        self.passEntry.grid(row=2, column=1)
        self.copyButton3.grid(row=2, column=2)

        self.unhideText = tk.IntVar()
        self.censorCheckbox = tk.Checkbutton(self, text='Unhide Text', variable=self.unhideText, onvalue=1, offvalue=0, command=self.toggle_text)
        self.censorCheckbox.grid(row=3, column=1, sticky='n')

        self.button = tk.Button(self, text="Close", relief='ridge')
        self.button['command'] = lambda a=num: self.close_edit_panel(a)
        self.button.grid(row=3, column=0, sticky='n')

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

    def copy_to_clipboard(self, num):
        if num==0:
            self.clipboard_clear()
            self.clipboard_append(self.targetDatabaseContent[0])
        if num==1:
            self.clipboard_clear()
            self.clipboard_append(self.targetDatabaseContent[1])
        if num==2:
            self.clipboard_clear()
            self.clipboard_append(self.targetDatabaseContent[2])

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
    ##app.protocol("WM_DELETE_WINDOW", app.iconify())
    app.mainloop()