import tkinter as tk
from tkinter import ttk
import webbrowser

class Book:
    def __init__(self, title, author, year, publisher, isbn, genre, description):
        self.title = title
        self.author = author
        self.year = year
        self.publisher = publisher
        self.isbn = isbn
        self.genre = genre
        self.description = description

class BookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Books and Websites")
        
        self.books = [
            Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Charles Scribner's Sons", "9780743273565", "Novel", 
                "The story primarily concerns the young and mysterious millionaire Jay Gatsby."),
            Book("Tender is the Night", "F. Scott Fitzgerald", 1934, "Charles Scribner's Sons", "9780684801544", "Novel", 
                "The novel tells the story of Dick Diver, a promising young psychoanalyst and his wife, Nicole."),
            Book("To Kill a Mockingbird", "Harper Lee", 1960, "J. B. Lippincott & Co.", "9780061120084", "Southern Gothic", 
                "The novel is renowned for its warmth and humor."),
            Book("Go Set a Watchman", "Harper Lee", 2015, "HarperCollins", "9780062409850", "Southern Gothic", 
                "Written in the mid-1950s, Go Set a Watchman imparts a fuller, richer understanding and appreciation of the late Harper Lee."),
            Book("1984", "George Orwell", 1949, "Secker & Warburg", "9780451524935", "Dystopian", 
                "The novel is set in Airstrip One, a province of the superstate Oceania."),
            Book("Shadows Over Monroeville", "Harper Lee", 1981, "Fictional Publishing", "9780061111111", "Drama", 
                "A fictional exploration of a town's secrets."),
            Book("The Finch Chronicles", "Harper Lee", 1990, "Fictional Publishing", "9780061111122", "Historical Fiction", 
                "A fictional dive into the history of the Finch family."),
            Book("Alabama Blues", "Harper Lee", 1995, "Fictional Publishing", "9780061111133", "Literary Fiction", 
                "A fictional tale of love, loss, and redemption set against the backdrop of the American South."),
        ]
        self.extract_unique_authors()
        
        self.setup_styles()
        self.setup_gui()

    def setup_styles(self):
        style = ttk.Style(self.master)
        style.theme_use("alt")
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TNotebook.Tab", background="#f0f0f0", padding=[5, 5])
        style.configure("TFrame", background="#f0f0f0")  # set background for all frames to #f0f0f0
        style.configure("TLabel", background="#f0f0f0")  # set background for all labels to #f0f0f0
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", background="#f0f0f0")

        style.theme_use("alt")
        style.configure("Treeview.Heading",
                        background="#a9a9a9",  
                        foreground="#2e2e2e",   
                        font=("Arial", 10, "bold"))

        style.map("Treeview.Heading",
                background=[('active', '#4b98d8')],  # color when hovered (or active)
                )

        style.map("Treeview",
                background=[('selected', '#4b98d8')],  # blue when selected
                foreground=[('selected', 'white')]    # white text when selected
                )

        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", background="#f0f0f0")

        
    def setup_gui(self):
        self.master.title("Books and Websites")

        # Create the Notebook widget (represents the tabs container)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.main_frame = ttk.Frame(self.notebook)
        self.secondary_frame = ttk.Frame(self.notebook)

        # Add the frames as tabs to the notebook with titles "Main" and "Secondary"
        self.notebook.add(self.main_frame, text='Main')
        self.notebook.add(self.secondary_frame, text='Secondary')

        # BOOK SECTION
        self.book_frame = ttk.LabelFrame(self.main_frame, text="Book Stuff", padding=(20, 10))
        self.book_frame.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')

        # Section 1: List of authors within book_frame
        self.author_frame = ttk.Frame(self.book_frame)
        self.author_frame.pack(pady=20, padx=20, fill=tk.Y) 

        self.author_vsb = ttk.Scrollbar(self.author_frame, orient="vertical")
        self.author_vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.author_listbox = tk.Listbox(self.author_frame, height=5, width=50, selectmode=tk.SINGLE, yscrollcommand=self.author_vsb.set)
        self.author_listbox.pack(side=tk.LEFT)
        self.author_vsb.config(command=self.author_listbox.yview)

        for author in self.authors:
            self.author_listbox.insert(tk.END, author)

        self.author_listbox.bind('<<ListboxSelect>>', self.on_author_selected)

        # Section 2: Display details of the books by the selected author in a treeview with scrollbars
        self.details_frame = ttk.Frame(self.book_frame)
        self.details_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.details_tree = ttk.Treeview(self.details_frame, columns=("Title", "Year", "Publisher", "ISBN", "Genre", "Description"), show="headings", height=5)
        vsb = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_tree.yview)
        hsb = ttk.Scrollbar(self.details_frame, orient="horizontal", command=self.details_tree.xview)
        self.details_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.details_tree.tag_configure('evenrow', background='#d3d3d3')  # light gray for even rows
        self.details_tree.tag_configure('oddrow', background='#c0c0c0')   # a slightly darker gray for odd rows

        self.details_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_rowconfigure(0, weight=1)

        self.details_tree.column("Title", width=100)
        self.details_tree.column("Year", width=50)
        self.details_tree.column("Publisher", width=100)
        self.details_tree.column("ISBN", width=100)
        self.details_tree.column("Genre", width=100)
        self.details_tree.column("Description", width=300)

        self.details_tree.heading("Title", text="Title")
        self.details_tree.heading("Year", text="Year")
        self.details_tree.heading("Publisher", text="Publisher")
        self.details_tree.heading("ISBN", text="ISBN")
        self.details_tree.heading("Genre", text="Genre")
        self.details_tree.heading("Description", text="Description")

        # WEBSITE SECTION
        self.website_frame = ttk.LabelFrame(self.main_frame, text="Website Stuff", padding=(20, 10))
        self.website_frame.grid(row=0, column=1, pady=20, padx=20, sticky='nsew')

        self.hyperlink_label = tk.Label(self.website_frame, text="www.google.com", fg="blue", cursor="hand2")
        self.hyperlink_label.grid(row=0, column=0, pady=20)
        self.hyperlink_label.bind("<Button-1>", self.open_webpage)
        self.hyperlink_label.configure(font=('-underline', 1))

        self.website_frame2 = ttk.LabelFrame(self.main_frame, text="Website Stuff2", padding=(20, 10))
        self.website_frame2.grid(row=1, column=1, pady=20, padx=20, sticky='nsew')

        self.hyperlink_label2 = tk.Label(self.website_frame2, text="www.google2.com", fg="blue", cursor="hand2")
        self.hyperlink_label2.grid(row=0, column=0, pady=20)
        self.hyperlink_label2.bind("<Button-1>", self.open_webpage)
        self.hyperlink_label2.configure(font=('-underline', 1))

        # Website Stuff3 in Secondary Tab
        self.website_frame3 = ttk.LabelFrame(self.secondary_frame, text="Website Stuff3", padding=(20, 10))
        self.website_frame3.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')

        self.hyperlink_label3 = tk.Label(self.website_frame3, text="www.google3.com", fg="blue", cursor="hand2")
        self.hyperlink_label3.grid(row=0, column=0, pady=20)
        self.hyperlink_label3.bind("<Button-1>", self.open_webpage)
        self.hyperlink_label3.configure(font=('-underline', 1))

        
    def on_author_selected(self, event):
        # First, clear any previous entries in the treeview
        for row in self.details_tree.get_children():
            self.details_tree.delete(row)

        # Get the selected author's name
        selected_index = self.author_listbox.curselection()
        if not selected_index:  # If no item is selected
            return
        selected_author = self.author_listbox.get(selected_index)

        # Filter books by the selected author (assuming `self.books` is a list of dictionaries containing book details)
        selected_books = [book for book in self.books if book.author == selected_author]

        # Populate the treeview with books of the selected author
        for book in selected_books:
           self.details_tree.insert("", tk.END, values=(book.title, book.year, book.publisher, book.isbn, book.genre, book.description))


    def open_webpage(self, event):
        webbrowser.open_new("http://www.google.com")
    
    def extract_unique_authors(self):
        # Use a set to ensure uniqueness
        authors = {book.author for book in self.books}
        # Convert the set back to a list for consistency
        self.authors = list(authors)

def main():
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
