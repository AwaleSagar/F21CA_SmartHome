
from rasa.nlu.model import Interpreter
import json


utterance = "can you turn on the light in bedroom two"
model = "./NLU/models/nlu-20200214-113529/nlu"

# loading the model from one directory or zip file
interpreter = Interpreter.load(model)

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
print(interpretation)


f = open('testresponse.json','a')

json.dump(interpretation, f)
# make it append
# f.write(str('/n'))
f.close

with open('testresponse.json', 'r+') as file:
    content = file.read()
    file.seek(0)
    content.replace('\'', '\"')
    file.write(content)