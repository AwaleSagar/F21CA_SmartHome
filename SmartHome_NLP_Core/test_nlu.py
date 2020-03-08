#%%
from rasa.nlu.model import Interpreter

utterance = u"please turn off bedroom lights"
model = "./models/20200308-221056.tar.gz"

# loading the model from one directory or zip file
interpreter = Interpreter.load(model)

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
print(interpretation)