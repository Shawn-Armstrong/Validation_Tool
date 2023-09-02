import tkinter as tk
from tkinter import ttk
import webbrowser

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

books = [
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

def on_author_selected(event):
    selected_index = author_listbox.curselection()
    if selected_index:
        selected_author = authors[selected_index[0]]
        
        # Clear existing items in the treeview
        for row in details_tree.get_children():
            details_tree.delete(row)
        
        # Filter the books based on the selected author
        books_by_selected_author = [book for book in books if book.author == selected_author]
        
        # Insert details of the books by the selected author into the treeview with alternating colors
        for idx, book in enumerate(books_by_selected_author):
            tags = ("evenrow", "oddrow")
            tag = tags[idx % 2]
            details_tree.insert("", "end", values=(book.title, book.year, 
                                                   book.publisher, book.isbn, book.genre, 
                                                   book.description), tags=tag)


'''
    SETUP style configuration
'''
root = tk.Tk()
root.title("Books and Websites")

style = ttk.Style(root)
style = ttk.Style(root)
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
# style.configure("TLabelframe.Label", background="#d9d9d9")

# Create the Notebook widget (represents the tabs container)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
main_frame = ttk.Frame(notebook)
secondary_frame = ttk.Frame(notebook)

# Add the frames as tabs to the notebook with titles "Main" and "Secondary"
notebook.add(main_frame, text='Main')
notebook.add(secondary_frame, text='Secondary')



'''
    BOOK SECTION
'''
# Book Stuff Separator
book_frame = ttk.LabelFrame(main_frame, text="Book Stuff", padding=(20, 10))
book_frame.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')


# Section 1: List of authors within book_frame

# Create a frame for the author_listbox and its scrollbar
author_frame = ttk.Frame(book_frame)
author_frame.pack(pady=20, padx=20, fill=tk.Y)  # Change fill to tk.Y

# Add vertical scrollbar for the author listbox
author_vsb = ttk.Scrollbar(author_frame, orient="vertical")
author_vsb.pack(side=tk.RIGHT, fill=tk.Y)

author_listbox = tk.Listbox(author_frame, height=5, width=50, selectmode=tk.SINGLE, yscrollcommand=author_vsb.set)
author_listbox.pack(side=tk.LEFT)  # Remove fill and expand arguments

# Link the scrollbar to the listbox
author_vsb.config(command=author_listbox.yview)

authors = list(set([book.author for book in books]))
authors.sort()  # Sort the authors alphabetically

# Populate listbox with authors
for author in authors:
    author_listbox.insert(tk.END, author)

author_listbox.bind('<<ListboxSelect>>', on_author_selected)

# Section 2: Display details of the books by the selected author in a treeview with scrollbars
details_frame = ttk.Frame(book_frame)
details_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Treeview, scrollbar setup and other details here...
details_tree = ttk.Treeview(details_frame, columns=("Title", "Year", "Publisher", "ISBN", "Genre", "Description"), show="headings", height=5)
vsb = ttk.Scrollbar(details_frame, orient="vertical", command=details_tree.yview)
hsb = ttk.Scrollbar(details_frame, orient="horizontal", command=details_tree.xview)
details_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Define row colors
details_tree.tag_configure('evenrow', background='#d3d3d3')  # light gray for even rows
details_tree.tag_configure('oddrow', background='#c0c0c0')   # a slightly darker gray for odd rows

details_tree.grid(row=0, column=0, sticky='nsew')
vsb.grid(row=0, column=1, sticky='ns')
hsb.grid(row=1, column=0, sticky='ew')

details_frame.grid_columnconfigure(0, weight=1)
details_frame.grid_rowconfigure(0, weight=1)

details_tree.column("Title", width=100)
details_tree.column("Year", width=50)
details_tree.column("Publisher", width=100)
details_tree.column("ISBN", width=100)
details_tree.column("Genre", width=100)
details_tree.column("Description", width=300)

details_tree.heading("Title", text="Title")
details_tree.heading("Year", text="Year")
details_tree.heading("Publisher", text="Publisher")
details_tree.heading("ISBN", text="ISBN")
details_tree.heading("Genre", text="Genre")
details_tree.heading("Description", text="Description")




'''
WEBSITE SECTION
'''

def open_webpage(event):
    webbrowser.open_new("http://www.google.com")

# Website Stuff in Main Tab
website_frame = ttk.LabelFrame(main_frame, text="Website Stuff", padding=(20, 10))
website_frame.grid(row=0, column=1, pady=20, padx=20, sticky='nsew')

hyperlink_label = tk.Label(website_frame, text="www.google.com", fg="blue", cursor="hand2")
hyperlink_label.grid(row=0, column=0, pady=20)
hyperlink_label.bind("<Button-1>", open_webpage)
hyperlink_label.configure(font=('-underline', 1))

website_frame2 = ttk.LabelFrame(main_frame, text="Website Stuff2", padding=(20, 10))
website_frame2.grid(row=1, column=1, pady=20, padx=20, sticky='nsew')

hyperlink_label2 = tk.Label(website_frame2, text="www.google2.com", fg="blue", cursor="hand2")
hyperlink_label2.grid(row=0, column=0, pady=20)
hyperlink_label2.bind("<Button-1>", open_webpage)
hyperlink_label2.configure(font=('-underline', 1))

# Website Stuff3 in Secondary Tab
website_frame3 = ttk.LabelFrame(secondary_frame, text="Website Stuff3", padding=(20, 10))
website_frame3.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')

hyperlink_label3 = tk.Label(website_frame3, text="www.google3.com", fg="blue", cursor="hand2")
hyperlink_label3.grid(row=0, column=0, pady=20)
hyperlink_label3.bind("<Button-1>", open_webpage)
hyperlink_label3.configure(font=('-underline', 1))


root.mainloop()
