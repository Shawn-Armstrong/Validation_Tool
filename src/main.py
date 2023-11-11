import log_capturer as lc
import record_manager as rm
import record_viewer as rv
import tkinter as tk

# main.py

def main():
    capturer = lc.LogCapturer()
    logs_by_url = capturer.capture_logs()

    manager = rm.RecordManager(logs_by_url)

    root = tk.Tk()
    app = rv.RecordApp(root, manager.records)
    root.mainloop()



if __name__ == '__main__':
    main()