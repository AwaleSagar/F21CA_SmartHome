#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 20:25:06 2020

@author: clarence
"""
from rasa.nlu.model import Interpreter

utterance = "can i book a table in paris for two persons"
model = "./nlu-20200127-163633/nlu"

# loading the model from one directory or zip file
interpreter = Interpreter.load(model)

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
print(interpretation)

print("-----------------------------")
print(interpretation['intent']['name'])
