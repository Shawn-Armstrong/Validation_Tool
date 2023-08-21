import log_capturer as lc

# main.py

def main():
    capturer = lc.LogCapturer()
    print(capturer.urls)
    logs_by_url = capturer.capture_logs()
    print(logs_by_url)

if __name__ == '__main__':
    main()