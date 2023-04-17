import re
import requests
import urllib.parse
import openai
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import yt_dlp
from threading import Thread
import os

# Set OpenAI API key
openai.api_key = "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"

class GetSub():
    def __init__(self, video_url, videoname):
        self.video_url = video_url
        self.videoname = videoname
        self.get_raw_sub()
        self.remove_non_speach()

    def get_text(self):
        return self.text

    def get_raw_sub(self):
        thread = Thread(target=yt_dlp.main, args=(["--write-auto-sub", "--skip-download", self.video_url, "-o", self.videoname],))
        thread.start()
        thread.join()
        if os.path.exists(self.videoname + '.en-orig.vtt'):
            self.file_name = self.videoname + '.en-orig.vtt'
        else:
            self.file_name = self.videoname + '.en.vtt'

    def remove_non_speach(self):
        pattern = re.compile(r'^.*(\d{2}:\d{2}:\d{2}\.\d{3}).*$')
        self.text = ''
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
        with open(self.file_name, 'w') as file:
            last_line = ''
            for line in lines:
                if not pattern.match(line) and line != last_line and line != ' \n' and line != '\n':
                    last_line = line
                    line_cleaned = line.rstrip()
                    line_cleaned = line.replace('\n', ' ')
                    file.write(line_cleaned)
                    self.text = self.text + line_cleaned
        return self.text

def get_website_text_selenium(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

    except Exception as e:
        print(f"An error occurred: {e}")
        text = None

    driver.quit()
    return text

def ask_openai(question, text):
    prompt = f"Question: {question}\nText: {text}\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def main():
    question = input("Enter a question: ")
    url = input("Enter a URL: ")

    if "youtube.com" in url:
        videoname = "video_subtitles"
        get_sub_instance = GetSub(url, videoname)
        text = get_sub_instance.get_text()
    else:
        text = get_website_text_selenium(url)
    if text:
        answer = ask_openai(question, text)
        print(answer)
    else:
        print("Failed to fetch text content. Please try another URL.")

if __name__ == "__main__":
    main()
