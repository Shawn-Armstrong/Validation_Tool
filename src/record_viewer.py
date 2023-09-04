import tkinter as tk
from tkinter import ttk

class RecordApp:
    def __init__(self, master, records):
        self.master = master
        self.master.title("Webpage Validation")
        
        self.records = records
        self.setup_styles()
        self.setup_gui()

    def setup_styles(self):
            style = ttk.Style(self.master)
            style.theme_use("alt")
            style.configure("TNotebook", background="#f0f0f0")
            style.configure("TNotebook.Tab", background="#f0f0f0", padding=[5, 5])
            style.configure("TFrame", background="#f0f0f0")  
            style.configure("TLabel", background="#f0f0f0")  
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
                    foreground=[('selected', 'white')]     # white text when selected
                    )

            style.configure("TLabelframe", background="#f0f0f0")
            style.configure("TLabelframe.Label", background="#f0f0f0")

    def setup_gui(self):
        self.master.title("Webpage Validation")

        # Create the Notebook widget (represents the tabs container)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill='both')
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)

        # Create frames for each tab
        self.main_frame = ttk.Frame(self.notebook)
        self.secondary_frame = ttk.Frame(self.notebook)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.secondary_frame.grid_rowconfigure(0, weight=1)
        self.secondary_frame.grid_columnconfigure(0, weight=1)

        # Add the frames as tabs to the notebook with titles "Main" and "Secondary"
        self.notebook.add(self.main_frame, text='Main')
        self.notebook.add(self.secondary_frame, text='Secondary')

        self.setup_endpoint_section()

        self.setup_production_page_section()
            
    def setup_endpoint_section(self):
        # Create a labeled frame titled 'Endpoints' in the main frame. This acts as a separator or section for endpoints.
        self.endpoint_separator = ttk.LabelFrame(self.main_frame, text="Endpoints", padding=(20, 10))
        self.endpoint_separator.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')

        # Create a frame inside the labeled frame for selecting endpoints.
        self.endpoint_select_frame = ttk.Frame(self.endpoint_separator)
        self.endpoint_select_frame.pack(pady=20, padx=20, fill=tk.Y)

        # Add a vertical scrollbar inside the endpoint selection frame.
        self.endpoint_vsb = ttk.Scrollbar(self.endpoint_select_frame, orient="vertical")
        self.endpoint_vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Listbox to list and select the available endpoints. It uses the vertical scrollbar for scrolling.
        self.endpoint_listbox = tk.Listbox(self.endpoint_select_frame, height=5, width=50, selectmode=tk.SINGLE, yscrollcommand=self.endpoint_vsb.set)
        self.endpoint_listbox.pack(side=tk.LEFT)
        self.endpoint_vsb.config(command=self.endpoint_listbox.yview)

        for _, record in self.records.items():
            self.endpoint_listbox.insert(tk.END, record.endpoint)

        # A placeholder for future functionality where a specific action will be performed when an endpoint is selected.
        # TO DO LATER
        self.endpoint_listbox.bind('<<ListboxSelect>>', self.on_endpoint_selected)


    def setup_production_page_section(self):
        # Create a labeled frame titled 'Production Page' in the main frame. This acts as a separator or section for production page content.
        self.production_page_separator = ttk.LabelFrame(self.main_frame, text="Production Page", padding=(20, 10))
        self.production_page_separator.grid(row=0, column=1, pady=20, padx=20, sticky='nsew')

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create a frame inside the labeled frame for displaying logs.
        self.production_page_frame = ttk.Frame(self.production_page_separator)
        self.production_page_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.production_page_separator.grid_rowconfigure(0, weight=1)
        self.production_page_separator.grid_columnconfigure(0, weight=1)

        # Initialize the treeview with specified columns and configure it to show column headings.
        self.production_console_tree = ttk.Treeview(self.production_page_frame, 
                                        columns=("Type", "Level", "Source", "Message"), 
                                        show="headings", height=10)
        
        # Create vertical and horizontal scrollbars for the treeview.
        vsb = ttk.Scrollbar(self.production_page_frame, orient="vertical", command=self.production_console_tree.yview)
        hsb = ttk.Scrollbar(self.production_page_frame, orient="horizontal", command=self.production_console_tree.xview)

        # Connect the scrollbars to the treeview.
        self.production_console_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Configure treeview to have alternating row colors for better readability.
        self.production_console_tree.tag_configure('evenrow', background='#FFFFFF')  
        self.production_console_tree.tag_configure('oddrow', background='#d3d3d3') 

        # Grid the treeview and scrollbars within the production_page_frame.
        self.production_console_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Ensure the treeview expands properly when the production_page_frame is resized.
        self.production_page_frame.grid_columnconfigure(0, weight=1)
        self.production_page_frame.grid_rowconfigure(0, weight=1)

        # Define the width for each column in the treeview.
        self.production_console_tree.column("Type", width=100)
        self.production_console_tree.column("Level", width=100)
        self.production_console_tree.column("Source", width=100)
        self.production_console_tree.column("Message", width=300)

        # Set the headings for each column in the treeview.
        self.production_console_tree.heading("Type", text="Type")
        self.production_console_tree.heading("Level", text="Level")
        self.production_console_tree.heading("Source", text="Source")
        self.production_console_tree.heading("Message", text="Message")

    def on_endpoint_selected(self, event):
        # First, clear any previous entries in the treeview
        for row in self.production_console_tree.get_children():
            self.production_console_tree.delete(row)
        
        # Get the selected endpoint's name
        selected_index = self.endpoint_listbox.curselection()
        if not selected_index:  # If no item is selected
            return
        selected_endpoint = self.endpoint_listbox.get(selected_index)

        selected_record = None
        for _, record in self.records.items():
            if record.endpoint == selected_endpoint:
                selected_record = record
                break
        

        
        if selected_record:  # Ensure that a matching record was found
            # Insert console_logs into the treeview
            for i, log in enumerate(selected_record.prod_logs['console_logs']):

                row_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.production_console_tree.insert('', 'end', values=('Console', log['level'], log['source'], log['message']), tags=(row_tag,))


def main():
    root = tk.Tk()
    app = RecordApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
