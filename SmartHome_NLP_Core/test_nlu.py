#%%
from rasa.nlu.model import Interpreter

utterance = u"please turn off bedroom heater"
model = "./models/nlu"

# loading the model from one directory or zip file
interpreter = Interpreter.load(model)

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
print(interpretation)

# %%

#hjzdcekjhzbcjehbdzjce
