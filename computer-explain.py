#!/usr/bin/env python
from threading import Thread
import yt_dlp
import re

class GetSub():
    def __init__(self):
        self.video_url = input("Enter video-url: ")
        self.videoname = input("Enter name for video: ")

    def sub_only(self):
        self.getsub()
        self.remove_non_speach()

    def getsub(self):
        thread = Thread(target=yt_dlp.main, args=(["--write-auto-sub", "--convert-subs=vtt", "--skip-download", self.video_url, "-o", self.videoname],))
        thread.start()
        thread.join()
        self.file_name = self.videoname + '.en.vtt'

    def remove_non_speach(self):
        pattern = re.compile(r'^.*(\d{2}:\d{2}:\d{2}\.\d{3}).*$')
        with open(self.file_name, 'r') as file:
            print(f'opening file for reading {self.file_name}')
            lines = file.readlines()
        with open(self.file_name, 'w') as file:
            last_line = ''
            for line in lines:
                if not pattern.match(line) and line != last_line and line != ' \n' and line != '\n':
                    #print(f'line: {repr(line)}\nvsus: {repr(last_line)}')
                    last_line = line
                    line_cleaned = line.rstrip()
                    line_cleaned = line.replace('\n', ' ')
                    file.write(line_cleaned)

if __name__ == '__main__':
    g = GetSub()
    g.sub_only()
