import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

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
    
        # Allow the main window to expand in all directions
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.setup_notebook_tabs()
        self.setup_endpoint_section()
        self.setup_production_page_section()
        
    def setup_notebook_tabs(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.main_frame = ttk.Frame(self.notebook)
        self.main_frame.grid_rowconfigure(0, weight=0)  
        self.main_frame.grid_columnconfigure(0, weight=0)  
        self.notebook.add(self.main_frame, text='Main')

        self.secondary_frame = ttk.Frame(self.notebook)
        self.secondary_frame.grid_rowconfigure(0, weight=0) 
        self.secondary_frame.grid_columnconfigure(0, weight=0)  
        self.notebook.add(self.secondary_frame, text='Secondary')
            
    def setup_endpoint_section(self):
        """
        Sets up the 'Endpoint' section, consisting of a frame which contains a listbox and scrollbar. 
        """

        # Create frame to contain the endpoint contents
        self.endpoint_label = ttk.LabelFrame(self.main_frame, text="Endpoints", padding=(10, 10), width=300, height=700)
        self.endpoint_label.grid(row=0, column=0, rowspan=2, pady=10, padx=10, sticky='nsew')

        # Configure the frame grid to allow its children  consume entire frame
        self.endpoint_label.grid_rowconfigure(0, weight=1)  
        self.endpoint_label.grid_columnconfigure(0, weight=1) 
        
        # Prevent the frame itself from resizing
        self.endpoint_label.grid_propagate(flag=False)

        # Create a vertical scrollbar inside the frame
        self.endpoint_select_vsb = ttk.Scrollbar(self.endpoint_label, orient="vertical")
        self.endpoint_select_vsb.grid(row=0, column=1, sticky='ns')

        # Create a listbox inside the frame to display the endpoints
        self.endpoint_listbox = tk.Listbox(self.endpoint_label, selectmode=tk.SINGLE, yscrollcommand=self.endpoint_select_vsb.set)
        self.endpoint_listbox.grid(row=0, column=0, sticky='nsew')

        # Configure the vertical scrollbar to the listbox
        self.endpoint_select_vsb.config(command=self.endpoint_listbox.yview)

        # Populate the listbox with endpoint records.
        for _, record in self.records.items():
            self.endpoint_listbox.insert(tk.END, record.endpoint)

        self.endpoint_listbox.bind('<<ListboxSelect>>', self.on_endpoint_selected)

    def setup_production_page_section(self):

        self.production_page_label = ttk.LabelFrame(self.main_frame, text="Production Page", padding=(10, 10), width=1000, height=330)
        self.production_page_label.grid(row=0, column=1, pady=10, padx=10, sticky='n')
        
        # Allow children frames to expand horizontally
        self.production_page_label.grid_columnconfigure(0, weight=1)

        # Prevent the frame itself from resizing
        self.production_page_label.grid_propagate(flag=False)

        # Initialize the treeview with specified columns and configure it to show column headings.
        self.production_console_tree = ttk.Treeview(self.production_page_label, 
                                        columns=("Type", "Level", "Source", "Message"), 
                                        show="headings", height=4)
        
        # Create vertical and horizontal scrollbars for the treeview.
        vsb = ttk.Scrollbar(self.production_page_label, orient="vertical", command=self.production_console_tree.yview)
        hsb = ttk.Scrollbar(self.production_page_label, orient="horizontal", command=self.production_console_tree.xview)

        # Connect the scrollbars to the treeview.
        self.production_console_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Configure treeview to have alternating row colors for better readability.
        self.production_console_tree.tag_configure('evenrow', background='#FFFFFF')  
        self.production_console_tree.tag_configure('oddrow', background='#d3d3d3') 

        # Grid the treeview and scrollbars within the production_page_label.
        self.production_console_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Define the width for each column in the treeview.
        self.production_console_tree.column("Type", width=60)
        self.production_console_tree.column("Level", width=50)
        self.production_console_tree.column("Source", width=100)
        self.production_console_tree.column("Message", width=2000)

        # Set the headings for each column in the treeview.
        self.production_console_tree.heading("Type", text=" Type", anchor="w")
        self.production_console_tree.heading("Level", text=" Level", anchor="w")
        self.production_console_tree.heading("Source", text=" Source", anchor="w")
        self.production_console_tree.heading("Message", text=" Message", anchor="w")

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
