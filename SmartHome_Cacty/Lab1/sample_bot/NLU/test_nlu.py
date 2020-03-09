from rasa.nlu.model import Interpreter

utterance = "can you turn off the lights in bedroom one"
model = "./models/nlu/"

# loading the model from one directory or zip file
interpreter = Interpreter.load(model)

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
print(interpretation)

f = open('testresponse.txt','a')
f.write(str(interpretation))
