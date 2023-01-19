#!/usr/bin/env python
from threading import Thread
import requests
import os
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
        #thread = Thread(target=yt_dlp.main, args=(["--write-auto-sub", "--convert-subs=vtt", "--skip-download", self.video_url, "-o", self.videoname],))
        thread = Thread(target=yt_dlp.main, args=(["--write-auto-sub", "--sub-langs=en.*", "--skip-download", self.video_url, "-o", self.videoname],))
        thread.start()
        thread.join()
        if os.path.exists(self.videoname + '.en-en.vtt'):
            self.file_name = self.videoname + '.en-en.vtt'
        else:
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

class AskGPT():
    def __init__(self):
        return 0
    def ask(self, question, data):
        r = requests.post('https://api.genesistranslation.com/v1/gtp3',
                json={"user_key": "<your key>",
                    "query": question
                    })

        data = r.json()
        print(data['result'])
if __name__ == '__main__':
    g = GetSub()
    g.sub_only()

#financial
"""
1. Give me a breif summary of the video
2. provide me as many bullet points as you can about the video
3. Does the speaker(s) make any forecasts
"""
#scientific
"""
1. Give me a beif summary
2. Does this contradict any main stream scientific thought?
3. Give me as many bullet points as you can about the video?
"""
