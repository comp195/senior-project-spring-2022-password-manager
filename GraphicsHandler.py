import tkinter as tk

class mainPanel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main panel")
        self.geometry("700x700")

        self.label = tk.Label(self, text = "This is the placeholder Main Panel")
        self.label.pack()

        self.button = tk.Button(self, text = "Open Edit Panel")
        self.button['command'] = self.open_edit_panel
        self.button.pack()

    def open_edit_panel(self):
        self.editPanel = editPanel()

class editPanel(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Edit panel")
        self.geometry("300x300")

        self.button = tk.Button(self, text="Close Edit Panel")
        self.button['command'] = self.close_edit_panel
        self.button.pack()

    def close_edit_panel(self):
        self.destroy()

if __name__ == "__main__":
    app = mainPanel()
    app.mainloop()