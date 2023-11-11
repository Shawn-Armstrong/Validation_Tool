import tkinter as tk
from tkinter import ttk

class BookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Books and Websites")
        self.setup_gui()

    def setup_gui(self):
        # Allow the main window to expand in all directions, but make sure the notebook stays centered
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.main_frame = ttk.Frame(self.notebook)
        self.main_frame.grid_rowconfigure(0, weight=0)  
        self.main_frame.grid_columnconfigure(0, weight=0)  
        self.notebook.add(self.main_frame, text='Main')

        self.secondary_frame = ttk.Frame(self.notebook)
        self.secondary_frame.grid_rowconfigure(0, weight=0)  # Keep this as 0
        self.secondary_frame.grid_columnconfigure(0, weight=0)  # Keep this as 0
        self.notebook.add(self.secondary_frame, text='Secondary')

        self.book_frame = ttk.LabelFrame(self.main_frame, text="Book Stuff", padding=(20, 10), width=500, height=300)
        self.book_frame.grid(row=0, column=0, pady=20, padx=20)
        self.book_frame.grid_propagate(flag=False)

        self.details_frame = ttk.Frame(self.book_frame, width=400, height=200)
        self.details_frame.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')
        self.details_frame.grid_propagate(flag=False)

        self.details_tree = ttk.Treeview(self.details_frame, columns=("Title", "Year", "Publisher", "ISBN", "Genre", "Description"), show="headings", height=2)
        self.vsb = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_tree.yview)
        self.hsb = ttk.Scrollbar(self.details_frame, orient="horizontal", command=self.details_tree.xview)
        self.details_tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.details_tree.tag_configure('evenrow', background='#FFFFFF')
        self.details_tree.tag_configure('oddrow', background='#d3d3d3')
        
        self.details_tree.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb.grid(row=1, column=0, sticky='ew')

        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_rowconfigure(0, weight=1)

        self.details_tree.column("Title", width=100)
        self.details_tree.column("Year", width=50)
        self.details_tree.column("Publisher", width=100)
        self.details_tree.column("ISBN", width=100)
        self.details_tree.column("Genre", width=100)
        self.details_tree.column("Description", width=200)  # Adjusted width

        self.details_tree.heading("Title", text="Title")
        self.details_tree.heading("Year", text="Year")
        self.details_tree.heading("Publisher", text="Publisher")
        self.details_tree.heading("ISBN", text="ISBN")
        self.details_tree.heading("Genre", text="Genre")
        self.details_tree.heading("Description", text="Description")

        dummy_values = ("Dummy Title", "2023", "Dummy Publisher", "1234567890", "Dummy Genre", "This is a dummy description." * 10)
        self.details_tree.insert("", "end", values=dummy_values)


def main():
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
