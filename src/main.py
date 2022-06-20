# -*- coding: utf-8 -*-
import os
import sys
from audio_book_generator import AudioBookGenerator
from http_agent import HttpAgent

import logging
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

def main():
    file_name = sys.argv[1]
    logging.info('upload file: {}'.format(file_name))

    # gen audio
    generator = AudioBookGenerator()
    generator.process(file_name)
    audio_url = generator.get_audio_url()
    logging.info('get audo url: {}'.format(audio_url))
    
    # download audio
    session_path = os.environ.get('SESSION_PATH', './')
    audio_name = os.path.join(session_path, 'result.mp3')
    agent = HttpAgent()
    agent.download(audio_url, audio_name)
    logging.info('download audio to: {}'.format(audio_name))

if __name__ == '__main__':
    main()