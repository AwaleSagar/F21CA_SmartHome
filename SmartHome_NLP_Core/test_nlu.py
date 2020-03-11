#%%
from pprint import pprint
from rasa.nlu.model import Interpreter

utterance = u"what was my energy consumption for yesterday"
model = "./models/nlu"

# loading the model from one directory or zip file
interpreter = Interpreter.load(model)

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
pprint(interpretation)

# %%

#hjzdcekjhzbcjehbdzjce
