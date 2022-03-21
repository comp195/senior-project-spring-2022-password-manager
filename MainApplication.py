import tkinter.filedialog
import tkinter as tk

def openFile(file_name):
    file = open(file_name,'r')
    file_contents = []
    for line in file:
        file_contents.append(line.split(' '))
    return file_contents

class mainPanel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.databaseContents = None
        self.accountInfo = []
        self.title("SecuriSimplex Password Manager")
        self.geometry("800x700")

        #self.label = tk.Label(self, text = "This is the placeholder Main Panel")
        #self.label.pack()

        self.EditSaveFrame = tk.Frame(self, height="100", relief="ridge", pady="5")  #Creating frame for open file and save file widgets
        self.EditSaveFrame.pack(fill="x", padx="5") #Fill entire x axis
        self.EditSaveFrame.pack_propagate(0) #Force the width and height

        self.button = tk.Button(self.EditSaveFrame, text = "Open A File", relief="groove")   #Button for Opening a File
        self.button['command'] = self.open_file
        self.button.pack(side=tk.LEFT, fill="both", expand=True, padx="0")

        self.button = tk.Button(self.EditSaveFrame, text="Save A File", relief="groove")     #Button for Saving a File
        self.button['command'] = self.save_file
        self.button.pack(side="right", fill="both", expand=True, padx="0")

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

        self.resizable(False, False) # May remove later

    def open_edit_panel(self, num):
        self.editPanel = editPanel(self.databaseContents, num)

    def open_file(self):
        self.filename = tk.filedialog.askopenfilename(initialdir = ".", title="Select the File to Open", filetypes=(("All Files", "*"), ("Database Files", ".xyz"), ))
        self.databaseContents = openFile(self.filename)
        #print(self.databaseContents)
        self.create_database_panel()

    def save_file(self):
        print("not functional yet")

    def create_database_panel(self):
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

        self.accLabel = tk.Label(self, text="Account Name")
        self.accEntry = tk.Entry(self, width=31, bg="gray")
        self.accEntry.insert(0, "**********")

        self.passLabel = tk.Label(self, text="Account Password")
        self.passEntry = tk.Entry(self, width=31, bg="gray")
        self.passEntry.insert(0, "**********")

        self.descLabel.grid(row=0, column=0)
        self.descEntry.grid(row=0, column=1)
        self.accLabel.grid(row=1, column=0)
        self.accEntry.grid(row=1, column=1)
        self.passLabel.grid(row=2, column=0)
        self.passEntry.grid(row=2, column=1)

        self.unhideText = tk.IntVar()
        self.censorCheckbox = tk.Checkbutton(self, text='Unhide Text', variable=self.unhideText, onvalue=1, offvalue=0, command=self.toggle_text)
        self.censorCheckbox.grid(row=3, column=1)

        self.button = tk.Button(self, text="Close Edit Panel")
        self.button['command'] = self.close_edit_panel
        self.button.grid(row=3, column=0, sticky='w')

        self.resizable(False, False)

    def close_edit_panel(self):
        self.destroy()

    def save_details(self):
        print("not implemented yet")

    def toggle_text(self):
        if self.unhideText.get() == 0:
            self.descEntry.delete(0, "end")
            self.descEntry.insert(0, "**********")
            self.accEntry.delete(0, "end")
            self.accEntry.insert(0, "**********")
            self.passEntry.delete(0, "end")
            self.passEntry.insert(0, "**********")
        if self.unhideText.get() == 1:
            self.descEntry.delete(0, "end")
            self.descEntry.insert(0, self.targetDatabaseContent[0])
            self.accEntry.delete(0, "end")
            self.accEntry.insert(0, self.targetDatabaseContent[1])
            self.passEntry.delete(0, "end")
            self.passEntry.insert(0, self.targetDatabaseContent[2].rstrip())


    # Flag user for confirmation for closing application



if __name__ == "__main__":
    app = mainPanel()
    app.update()
    app.mainloop()