from rasa.nlu.model import Interpreter

utterance = u"can i book a table in paris for two persons"
model = "./rasa-nlu-tutorial/models/nlu-20200127-163633.tar.gz"

# loading the model from one directory or zip file
interpreter = Interpreter.load(model)

# parsing the utterance
interpretation = interpreter.parse(utterance)

# printing the parsed output
print(interpretation)
