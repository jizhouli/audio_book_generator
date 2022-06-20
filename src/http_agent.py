# -*- coding: utf-8 -*-

import os
import requests


class HttpAgent(object):

    def __init__(self):
        self.DOWNLOAD_RETRY = 3

    def download(self, file_url, local_file):
        dir = os.path.dirname(os.path.abspath(local_file))
        if not os.path.isdir(dir):
            msg = 'http download fail: directory not exist "{}"'.format(dir)
            print(msg)
            return False, msg

        for _ in range(self.DOWNLOAD_RETRY):
            try:
                proxies = {'http':None, 'https':None}
                myfile = requests.get(file_url, allow_redirects=True, proxies=proxies)
                open(local_file, 'wb').write(myfile.content)
                break
            except Exception as e:
                print('http download fail, retry: {} -> {}, msg={}'.format(file_url, local_file, str(e)))
                continue

        if not os.path.isfile(local_file):
            msg = 'http download fail: {} -> {}, msg=retry but no file'.format(file_url, local_file)
            print(msg)
            return False, msg
        
        print('http download succ: {} -> {}'.format(file_url, local_file))
        return True, ''
