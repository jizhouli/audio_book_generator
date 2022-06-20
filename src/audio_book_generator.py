
import os
import sys
import time
import shutil
import mobi
from lxml import etree

from tencent_sdk import TencentSDK
from config import Config

import logging
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

class AudioBookGenerator(object):

    def __init__(self):
        self.cloud = TencentSDK(Config.SECRET_ID, Config.SECRET_KEY)

        self.html_content = ''
        self.text = ''
        self.audio_url = ''

    def load_file(self, file_name):
        logging.info('begin to parse file')
        start_t = time.time()
        tmp_dir, tmp_html = mobi.extract(file_name)
        end_t = time.time()
        logging.info('extract {} to {}. cost {}ms'.format(file_name, tmp_html, int((end_t-start_t)*1000)))

        with open(tmp_html, 'r') as fp:
            lines = fp.readlines()
        self.html_content = ''.join(lines)
        logging.info('load file total {} chars'.format(len(self.html_content)))

        shutil.rmtree(tmp_dir)
        logging.info('clean temp dir {}'.format(tmp_dir))
    
    def pre_process(self, content):
        content = content.replace('<mbp:pagebreak/>', '')
        return content

    def parse_html(self):
        logging.info('parse html')
        # pre process
        self.html_content = self.pre_process(self.html_content)
        
        # parse dom
        dom = etree.fromstring(self.html_content)
        plist = dom.xpath('//p/text()')
        audio_texts = []

        idx_start = 1010
        for p in plist[idx_start:idx_start+10]:
            #logging.info('{}'.format(p))
            audio_texts.append(p)
        
        self.text = ''.join(audio_texts)
        logging.info('content length {}'.format(len(self.text)))

    def synthesis(self):
        self.audio_url = self.cloud.long_text_synthesis(self.text)

    def process(self, file_name):
        self.load_file(file_name)
        self.parse_html()
        self.synthesis()

    def get_audio_url(self):
        logging.info('get_audio_url: {}'.format(self.audio_url))
        return self.audio_url


def main():
    file_name = sys.argv[1]
    generator = AudioBookGenerator()
    generator.process(file_name)
    print(generator.get_audio_url())

if __name__ == '__main__':
    main()
