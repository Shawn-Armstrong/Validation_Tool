import tkinter as tk
from tkinter import ttk
import json

class RecordViewer(tk.Tk):
    def __init__(self, records):
        super().__init__()

        self.records = records
        self.title("Log Viewer")

        self.create_widgets()

    def create_widgets(self):
        # Field 1: Scrollable list of endpoints
        self.endpoint_listbox = tk.Listbox(self, height=20, width=50)
        self.endpoint_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.endpoint_listbox.bind('<<ListboxSelect>>', self.on_endpoint_select)

        for endpoint in self.records.keys():
            self.endpoint_listbox.insert(tk.END, endpoint)

        # Scrollbar for endpoints listbox
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.endpoint_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.endpoint_listbox.config(yscrollcommand=scrollbar.set)

        # # Field 2: Test Logs
        # test_frame = ttk.LabelFrame(self, text="Test", height=400, width=400)
        # test_frame.grid(row=0, column=2, padx=10, pady=10)
        # self.test_text = tk.Text(test_frame, wrap=tk.WORD, height=20, width=50)
        # self.test_text.pack(padx=10, pady=10)

       # Field 3: Production Logs
        production_frame = ttk.LabelFrame(self, text="Production", height=400, width=400)
        production_frame.grid(row=0, column=3, padx=10, pady=10)

        # Create the Text widget
        self.production_text = tk.Text(production_frame, wrap=tk.NONE, height=20, width=50)  # Note: wrap is set to tk.NONE

        # Create Scrollbars
        self.production_text_scroll_y = tk.Scrollbar(production_frame, orient='vertical', command=self.production_text.yview)
        self.production_text_scroll_x = tk.Scrollbar(production_frame, orient='horizontal', command=self.production_text.xview)

        # Configure the Text widget to use the Scrollbars
        self.production_text.config(yscrollcommand=self.production_text_scroll_y.set, xscrollcommand=self.production_text_scroll_x.set)

        # Pack the Text widget and Scrollbars into the frame
        self.production_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Using grid instead of pack for better placement
        self.production_text_scroll_y.grid(row=0, column=1, sticky="ns")
        self.production_text_scroll_x.grid(row=1, column=0, sticky="ew")

        # Adjusting the grid weights so that Text widget expands as the frame resizes
        production_frame.grid_rowconfigure(0, weight=1)
        production_frame.grid_columnconfigure(0, weight=1)


    def on_endpoint_select(self, event):
        selected_indices = self.endpoint_listbox.curselection()
        if not selected_indices:  # Check if the tuple is empty
            return  # Exit the function if there's no selection

        selected_index = selected_indices[0]
        endpoint = self.endpoint_listbox.get(selected_index)
        record_data = self.records[endpoint]

        # Clear the previous logs
        self.production_text.delete(1.0, tk.END)

        # Check if there's any data to display
        if "production_page_log" in record_data and "network_logs" in record_data["production_page_log"]:
            # Convert all log entries (which are dictionaries) to a string and join them
            log_entries = '\n'.join(json.dumps(log, indent=4) for log in record_data["production_page_log"]["network_logs"])
            self.production_text.insert(tk.END, log_entries)
        else:
            self.production_text.insert(tk.END, "No data")