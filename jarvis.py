from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import os
import webbrowser
import random
import chromedriver_binary
import re
import wikipedia
from time import strftime
from bs4 import BeautifulSoup as soup
import urllib.request  as urllib2
import newspaper
from newspaper import  article




import smtplib
def talkToMe(audio):
    print(audio)
    tts = gTTS(text=audio,lang='en')
    tts.save("audio.mp3")
    os.system("mpg123 audio.mp3")
#listen for our command
def myCommand():
    global command
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("i'm ready for your command boss")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio).lower()
        print('you said' + text + '/n')
#loop back
    except sr.UnknownValueError:
        talkToMe("cant hear you boss")
        text = myCommand()
    return text
#if conditionssss
def assistant(text):
    errors = [
        "I don\'t know what you mean!",
        "Excuse me?",
        "Can you repeat it please?",
    ]


    if 'who made you' in text:
        talkToMe("it's you my boss")
    elif 'what\'s your name' in text:
        talkToMe("my name is devi")
    elif 'love you dear' in text:
        talkToMe("love you too boss")
    elif 'hello' in text:
        day_time = int(strftime('%H'))
        if day_time < 12:
            talkToMe('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            talkToMe('Hello Sir. Good afternoon')
        else:
            talkToMe('Hello Sir. Good evening')
    elif 'open google'in text:
        reg_ex = re.search('open google (.*)', text)
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        webbrowser.open(url)
        print('Done!')
    elif 'open google and search' in text:
        reg_ex = re.search('open google and search (.*)', text)
        search_for = text.split("search", 1)[1]
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        talkToMe('Okay!')
        driver = webdriver.Chrome()  # depends which web browser you are using
        driver.get('https://www.google.com')
        search = driver.find_element_by_name('q')  # finds search
        search.send_keys(str(search_for))  # sends search keys
        search.send_keys(Keys.RETURN)  # hits enter
    elif 'tell me about' in text:
        reg_ex = re.search('tell me about (.*)', text)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                ny = ny.content[:500]
                # ny = ny.encode('utf-8')
                print(ny)
                talkToMe(ny)
        except Exception as e:
            print(e)
            talkToMe(e)

    elif 'news for today' in text:
        try:
            news_url = "https://news.google.com/news/rss"
            with urllib2.urlopen(news_url) as response:
                xml_page = response.read()
            response.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")

            for news in news_list[:15]:
                print(news.title.text)
                talkToMe(news.title.text)
        except Exception as e:
            print(e)
    elif 'date and time ' in text:
        import datetime
        now = datetime.datetime.now()
        talkToMe('Current time is %d hours %d minutes' % (now.hour, now.minute))
    else:
        error = random.choice(errors)
        talkToMe(error)

talkToMe('hy boss im Devi,  your personal voice assistant and im ready for your command boss')
while 1:

    assistant(myCommand())




