# class Record:
#     def __init__(self, endpoint):
#         self.endpoint = endpoint
#         self.test_page_log = None
#         self.production_page_log = None

    # def assign_log(self, url, log):
    #     if 'https://www.wellsfargo.com' in url:
    #         self.production_page_log = log
    #     else:
    #         self.test_page_log = log

class Record:
    def __init__(self, endpoint, test_logs, prod_logs):
        self.endpoint = endpoint
        self.test_logs = test_logs
        self.prod_logs = prod_logs
    
