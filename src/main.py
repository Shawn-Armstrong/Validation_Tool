import log_capturer as lc
import record_manager as rm
import record_viewer as rv

# main.py

def main():
    capturer = lc.LogCapturer()
    logs_by_url = capturer.capture_logs()
    manager = rm.RecordManager(logs_by_url)
    viewer = rv.RecordViewer(manager.records)
    app = rv.RecordViewer(viewer)
    app.mainloop()


if __name__ == '__main__':
    main()