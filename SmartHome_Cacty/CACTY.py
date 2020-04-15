#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 17:57:21 2020

@author: clarence
"""
#This is a test commit

## nhvnhgnbv  n,b,nbnb
from tkinter import *
import random
import time
import os 
import string
from pygame import mixer  # Load the popular external library
from gtts import gTTS
from nltk import tokenize
import speech_recognition as sr
#from rasa.nlu.model import Interpreter

import os
import subprocess

from subprocess import PIPE, run
import signal
#from playsound import playsound


#----------------OPEN NGROK-------------------------
p = subprocess.Popen(['gnome-terminal', '--disable-factory', '-e', 'bash -c \"./ngrok http 5130; sleep 1000000\" '], preexec_fn=os.setpgrp)

time.sleep(7)

#-----------------------GET NGROK URL----------------

command = ["curl","—silent","—show-error","http://127.0.0.1:4040/api/tunnels","|","sed","-nE","""'s/.*public_url":"https:..([^"]*).*/\1/p'"""]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
str1=result.stdout

import json
diu=json.loads(str1)

ngrok_url=diu['tunnels'][0]['public_url']

#-----------------------CALL BOT---------------------------------------------------------

actual_path=os.path.abspath(os.getcwd())
os.chdir(actual_path+'/Lab1/sample_bot')
p2 = subprocess.Popen(['gnome-terminal', '--disable-factory', '-e', 'bash -c \"bash condactivateAlana.sh; sleep 1000000\" '], preexec_fn=os.setpgrp)

time.sleep(10)
os.chdir(actual_path)

#---------------------------------------------------------------------------------

import numpy as np

from PIL import Image, ImageTk
WIDTH = 500
HEIGHT = 300
size=300
#----------------------------------------------------------------------
def resizefile(file,size):
    image = Image.open(file)
    image = image.resize((size,size))
    photo = ImageTk.PhotoImage(image)
    return photo
#-----------------------------------------------------------------------
    
import requests
answer =""

New_bots = {"EcoBot_Fact":ngrok_url}
print(New_bots)
bot_list_= [New_bots]
prio_bot_list_=list(bot_list_)
#bot_list_=["clarification_bot","ontology_bot","aiml_bot","coherence_bot","evi","weather_bot","fact_bot","news_bot_v2","wiki_bot_mongo","profanity_bot","reddit_bot"]
#prio_bot_list_= list(bot_list_).remove('coherence_bot')



#-----------------------------------------------------------------------

class MainWindow():

    #----------------

    def __init__(self, main):

        # canvas for image
        self.canvas = Canvas(main, width=WIDTH, height=HEIGHT)
        self.canvas.grid(row=0, column=0, columnspan = 2,sticky = W+E+N+S )

        # images
        self.my_images = []
        self.my_images.append(resizefile("./test.png",size))
        self.my_images.append(resizefile("./test1.png",size))
        self.my_images.append(resizefile("./test2.png",size))
        self.my_images.append(resizefile("./test3.png",size))
        self.my_images.append(resizefile("./test4.png",size))
        self.my_images.append(resizefile("./test5.png",size))
        self.my_image_number = 0
        
        #mood
        self.happy = self.my_images.copy()[0:3]
        #print(len(self.happy))
        self.sad = [self.my_images.copy()[i] for i in [0,3]]
        #print(len(self.sad))
        self.angry = self.my_images.copy()[4:6]
        #print(len(self.angry))
        
        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(WIDTH/2, HEIGHT/2, image = self.my_images[self.my_image_number])

        #text input
        self.variable1=StringVar() # Value saved here
        self.e1 = Entry(main, textvariable = self.variable1)
        self.e1.grid(row=1,column=0, columnspan = 2,sticky = W+E+N+S )

        #text output
        self.t1 = Text(main,width=40, height=10)
        self.t1.grid(row=3,column=0, columnspan = 2,sticky = W+E+N+S )
        
        # button to change image
        self.button = Button(main, text="Write", command=self.getText)
        self.button.grid(row=2, column=0, sticky = W+E+N+S )
        
        
        # button to Speak
        self.button = Button(main, text="Speak", command=self.getSpeech)
        self.button.grid(row=2, column=1, sticky = W+E+N+S )

    #----------------
    def getText(self):
        text=self.variable1.get()
        self.askAlana(text)
        
    def getSpeech(self):
        text = self.SpeechtoText()
        #time.sleep(1)
        self.askAlana(text)
        
        
    def askAlana(self,text):

        #text=self.variable1.get()
        data = {'user_id': 'test-user', 'question': text, 'session_id': 'someonearoundthecornerSSSS', 'projectId': 'CA2020', 'overrides': {'BOT_LIST': bot_list_ , 'PRIORITY_BOTS': [prio_bot_list_]}}
        #data = {'user_id': 'test-user', 'question': text, 'session_id': 'someonearoundthecorner', 'projectId': 'CA2020', 'overrides': {'BOT_LIST': bot_list_ , 'PRIORITY_BOTS': [prio_bot_list_, 'coherence_bot']}}
        
        r= requests.post(url='http://52.56.181.83:5000', json=data)
        #r= requests.post(url='http://52.23.135.246:5000', json=data)
        answer=r.json()['result']

        self.t1.configure(state='normal')
        self.t1.delete('1.0', END)
        self.t1.insert(END,answer)
        self.t1.configure(state='disabled')
        
        sentence_list=tokenize.sent_tokenize(answer)
        
        for i in range (0,len(sentence_list)):            

            
            wordlist=[word.strip(string.punctuation) for word in sentence_list[i].split()]
            numerofword=len(wordlist)
            #print(numerofword)
            
            try:
                output_speech=gTTS(text = sentence_list[i], lang="en", slow = False)
                output_speech.save("speech.mp3")
                
                mixer.init()
                mixer.music.load("speech.mp3")
                mixer.music.play()
    
                
                mood_ = "happy"
                for j in range (0,round(numerofword*2.2)):
                    root.update()
                    self.onButton(mood_)
                    time.sleep(0.2)
                    
            except AssertionError:
                pass
            
            self.my_image_number = -1
            self.onButton(mood_)
            
            time.sleep(0.5)

        
    def onButton(self,mood = None):

        if mood is None:
            mood="happy"
        # next image
        
        if mood == "happy":
            self.moodlist = self.happy
        if mood == "sad":
            self.moodlist = self.sad
        if mood == "angry":
            self.moodlist = self.angry
            
        self.my_image_number += 1
        
        # return to first image
        if self.my_image_number == len(self.moodlist) or self.my_image_number > len(self.moodlist) :
            self.my_image_number = 0

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.moodlist[self.my_image_number])

    def SpeechtoText(self):

        r3 = sr.Recognizer()
        
        with sr.Microphone(device_index=0) as source:
        #with sr.Microphone(device_index=0) as source:
            #print('[search edureka : search youtube]')
            print('Want to speak to Alana?')
            try:
                
                r3.adjust_for_ambient_noise(source,duration = 1)
                #r3.energy_threshold = 50
                #r3.dynamic_energy_threshold = False
                print("Speak")
                audio = r3.listen(source, timeout= 5)
                
            except sr.UnknownValueError:
                print('error')
            except sr.RequestError as e:
                print('failed'.format(e))
                
        #print(r3.recognize_google(audio))
        output3=r3.recognize_google(audio, language = 'en-GB', show_all = True)
        output4 = output3['alternative'][0]['transcript']
        
        #print(output3)
        print(output4)
        
        return output4
    

#----------------------------------------------------------------------



root = Tk()


root.title("Welcome to Alana app")

MainWindow(root)
root.mainloop()

#-----------------KILL TERMINAL----------------------
os.killpg(p.pid, signal.SIGINT)
os.killpg(p2.pid, signal.SIGINT)
