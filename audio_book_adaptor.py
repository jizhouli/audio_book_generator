#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'justinli.ljt@gmail.com'
import os
import sys
import argparse


SCRIPT_PATH = '/root/audio_book'

parser = argparse.ArgumentParser(description="convert mobi file to audio")
parser.add_argument('--audio', help='the mobi file to make audio', type=argparse.FileType('r'), required=True)

def audio_book(mobi_file):
    _format = mobi_file.split('.')[-1].lower()
    if _format != 'mobi':
        print('only mobi is supported')
        return

    cmd = []
    cmd.append('export SESSION_PATH={}'.format(os.getcwd()))
    cmd.append('cd {}'.format(SCRIPT_PATH))
    cmd.append('source {}/venv/bin/activate'.format(SCRIPT_PATH))
    cmd.append('cd src')
    cmd.append('python main.py {}'.format(mobi_file))
    cmd.append('cd ')
    cmd = '&&'.join(cmd)

    print(cmd)
    os.system(cmd)


if __name__ == '__main__':

    args = parser.parse_args()
    audio_book(args.audio.name)

