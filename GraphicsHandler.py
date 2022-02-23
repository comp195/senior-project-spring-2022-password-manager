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
        self.title("Main panel")
        self.geometry("700x700")

        self.label = tk.Label(self, text = "This is the placeholder Main Panel")
        self.label.pack()

        self.button = tk.Button(self, text="Open Edit Panel", relief="groove")   #Open Edit Panel (Placeholder)
        self.button['command'] = self.open_edit_panel
        self.button.pack()

        self.EditSaveFrame = tk.Frame(self, height="100", relief="ridge", pady="5")  #Creating frame for open file and save file widgets
        self.EditSaveFrame.pack(fill="x", padx="5") #Fill entire x axis
        self.EditSaveFrame.pack_propagate(0) #Force the width and height

        self.button = tk.Button(self.EditSaveFrame, text = "Open A File", relief="groove")   #Button for Opening a File
        self.button['command'] = self.open_file
        self.button.pack(side=tk.LEFT, fill="both", expand=True, padx="0")

        self.button = tk.Button(self.EditSaveFrame, text="Save A File", relief="groove")     #Button for Saving a File
        self.button['command'] = self.save_file
        self.button.pack(side=tk.RIGHT, fill="both", expand=True, padx="0")

        self.dataFrame = tk.Frame(self, bg="gray", height="500", relief="ridge", pady="5")  # Creating frame for data entries
        self.dataFrame.pack(fill="x", padx="5")  # Fill entire x axis
        self.dataFrame.pack_propagate(0)  # Force the width and height


    def open_edit_panel(self):
        self.editPanel = editPanel()

    def open_file(self):
        self.filename = tk.filedialog.askopenfilename(initialdir = ".", title="Select the File to Open", filetypes=(("All Files", "*"), ("Database Files", ".xyz"), ))
        self.databaseContents = openFile(self.filename)
        print(self.databaseContents)
        self.create_database_panel()

    def save_file(self):
        print("not functional yet")

    def create_database_panel(self):
        if self.databaseContents is not None:
            for num in range(0, len(self.databaseContents)):
                self.accountInfo.append(tk.Button(self.dataFrame, bg="white", text=self.databaseContents[num][0], height="5", relief="ridge", pady="5"))  # Creating frame for data entries
            for num in range(0, len(self.accountInfo)):
                self.accountInfo[num].pack(fill="x", expand=False, padx="5")  # Fill entire x axis
                self.accountInfo[num].pack_propagate(0)  # Force the width and height


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