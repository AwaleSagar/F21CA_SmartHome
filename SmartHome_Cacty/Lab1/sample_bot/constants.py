import os
import pandas as pd


#MODEL_ADDR = "./NLU/models/nlu-20200216-142039/nlu"
#MODEL_ADDR = "./NLU/models/Old_NLU/nlu-20200214-113529/nlu"

#MODEL_ADDR = "./NLU/models/20200323-181158/nlu"

#MODEL_ADDR = "./NLU/models/20200331-192950/nlu"

#-------------------------------------------------
#MODEL_ADDR = "./NLU/models/20200331-192950_2/nlu"
#MODEL_ADDR = "./NLU/models/20200323-181158/nlu"
MODEL_ADDR = "../../../SmartHome_NLP_Core/models/nlu-20200413-224443/nlu"
#-------------------------------------------------


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#MONGODB_URL = "mongodb://0.tcp.ngrok.io:10277"
#MONGODB_URL = "mongodb://127.0.0.1:18239/?compressors=disabled&gssapiServiceName=mongodb"
#MONGODB_URL= "mongodb://0.tcp.ngrok.io:16626/?compressors=disabled&gssapiServiceName=mongodb"
#MONGODB_URL= "mongodb://0.tcp.ngrok.io:16206/?compressors=disabled&gssapiServiceName=mongodb"
MONGODB_URL= "mongodb://f21ca:watt6789@18.219.152.221:27017/shome"



#MONGODB_URL= "mongodb://b64736ba.ngrok.io/"
## WAGI API PARAMS
API_KEY = "dc7cf06b49047ee83091c9c350abcf80db6fbd43"
API_URL = f"https://api.waqi.info/feed/edinburgh/?token={API_KEY}"

## DATASETs PARAMS
DATASETS_FOLDER = os.path.join(os.getcwd(),"/home/osboxes/Documents/F21CA_SmartHome/SmartHome_Interface/Data_Files")

AIR_QUALITY_DATASET_FILE_NAME = "air_quality/edi_air_quality.csv"
CONSUMPTION_DATASET_FILE_NAME = "energy_consumption/energy_consumption.pkl"
TIMESTAMPS_DATASET_FILE_NAME = "energy_consumption/timestamps.csv"

AIR_QUALITY_DATASET = pd.read_csv(os.path.join(DATASETS_FOLDER, AIR_QUALITY_DATASET_FILE_NAME))
CONSUMPTION_DATASET = pd.read_pickle(os.path.join(DATASETS_FOLDER, CONSUMPTION_DATASET_FILE_NAME))
TIMESTAMPS_DATASET = pd.read_csv(os.path.join(DATASETS_FOLDER, TIMESTAMPS_DATASET_FILE_NAME))

THRESHOLD = 0.5

LOCATION_TO_ZONE = {"living" : "A", # living room
                    "washroom" : "B", # washroom
                    "pantry" : "C", 
                    "kitchen" : "D", 
                    "entrance" : "E", # entrance hall
                    "garage" : "F", 
                    "hallway" : "G", 
                    "bedroom one" : "H", # kids room
                    "bathroom one" : "I", # bathroom
                    "bedroom two" : "J",  # single bedroom
                    "bathroom two" : "K", # bathroom
                    "bedroom three" : "L", # double bedroom
                    "laundry" : "M", 
                    "office" : "N",
                    "exterior" : "O"} # also include gate, pool and lights

ZONE_TO_LOCATION = {"A" : "living room", # living room
                    "B" : "washroom", # washroom
                    "C" : "pantry", 
                    "D" : "kitchen", 
                    "E" : "entrance hall", # entrance hall
                    "F" : "garage", 
                    "G" : "hallway", 
                    "H" : "kids room", # kids room
                    "I" : "bathroom", # bathroom
                    "J" : "single bedroom",  # single bedroom
                    "K" : "bathroom", # bathroom
                    "L" : "double bedroom", # double bedroom
                    "M" : "laundry room", 
                    "N" : "office",
                    "O" : "exterior"}

LOCATION_TO_NAME = {"living" : "living room", # living room
                    "washroom" : "washroom", # washroom
                    "pantry" : "pantry", 
                    "kitchen" : "kitchen", 
                    "entrance" : "entrance hall", # entrance hall
                    "garage" : "garage", 
                    "hallway" : "hallway", 
                    "bedroom one" : "kids room", # kids room
                    "bathroom one" : "bathroom", # bathroom
                    "bedroom two" : "single bedroom",  # single bedroom
                    "bathroom two" : "bathroom", # bathroom
                    "bedroom three" : "double bedroom", # double bedroom
                    "laundry" : "laundry room", 
                    "office" : "office",
                    "exterior" : "exterior"} # also include gate, pool and lights

ENTITY_TO_DATABASE_NAME = {
                "light" : "Light",
                "heater" : "Heater"
            }

HEATING_CHANGE_RATE = 0.2

ACTION_TO_DB_VALUE_MAPPING = {
        "turn on": lambda x: "true",
        "turn off": lambda x: "false",
        "increase": lambda x: x*(1+HEATING_CHANGE_RATE),
        "decrease": lambda x: x*(1-HEATING_CHANGE_RATE)
    }

ENERGY_CONSUMPTION_ADDRESSES = {
    "hour":146,
    "day":147,
    "week":148,
    "month":149
        }

##########################
##      AIR QUALITY     ##
##########################

LEVELS = [
    "GOOD", "MODERATE", "UNHEALTHY FOR SENSITIVE PEOPLE", "UNHEALTHY", "DANGEROUS", "HAZARDOUS"
]


CARBON_MONOXIDE_DESC = { #source: https://support.firstalert.com/servlet/rtaImage?eid=ka33l000000dHVl&feoid=00N1N00000Pyq9h&refid=0EM3l000002FIWI
    0.1: {
        "desc":"it is equivalent to living outside in a rural area",
        "level":0
        },
    5: {
        "desc":"it is equivalent to indoor level or of outside levels in cities",
        "level":0
        },
    15: {
        "desc":"it is equivalent to being within feet of a gas stove/furnace in an unvented kitchen",
        "level":0
        },
    20: {
        "desc":"it is equivalent to concentration in flue gases and can cause minor long-term/cardiovascular effects. Warning",
        "level":1
        },
    35: {
        "desc":"it is the maximum allowable outdoor level according to EPA. Warning.",
        "level":2
        },
    50: {
        "desc":"it is the maximum safe level for long-term exposure, up to 8 hours. Dangerous.",
        "level":2
        },
    75: {
        "desc":"it is equivalent to levels of a heavy smoker. Dangerous.",
        "level":3
        },
    150: {
        "desc":"it is the sign of a polluted city center. Do not practice exercise outside for too long.",
        "level":3
        },
    400: {
        "desc":"can cause hallucinations, dementia, serious headaches with 1 to 2 hours of exposure",
        "level":4
        },
    800: {
        "desc":"Can generate seizures, severe headaches and vomiting under an hour",
        "level":4
        },
    1500: {
        "desc":"Headaches, dizziness and nausea in under 20 minutes",
        "level":5
        },
    6400: {
        "desc":"Unconsciousness after two to three breaths leading to death within 15 minutes",
        "level":5
        }
}

NITROGEN_DIOXIDE_DESC = { #source: https://i.pinimg.com/originals/85/c1/48/85c148689f4feacbea35d77bd6ef0646.png
    50: {
        "desc":"air quality is satisfactory, with little to no risk posed by air pollution",
        "level":0
        },
    100: {
        "desc":"air quality is acceptable. However, people exceptionally sensitive to air pollution may experience moderate health problems.",
        "level":1
        },
    150: {
        "desc":"air quality is unhealthy for sensitive groups like elders or young children and babies.",
        "level":2
        },
    200: {
        "desc":"air quality is unhealthy to anyone. Serious health effects may occur in sensitive groups.",
        "level":3
        },
    300: {
        "desc":"air quality is very unhealthy, the entire population is affected.",
        "level":4
        },
    500: {
        "desc":"air quality is hazardous: everyone will experience serious health effects",
        "level":5
        }
}

OZONE_DESC = { #source: https://www.mwcog.org/assets/1/6/Air_Quality_Index_web.png
    50: {
        "desc":"air quality is considered good",
        "level":0
        },
    100: {
        "desc":"air quality may pose a moderate health risk for sensitive population",
        "level":1
        },
    150: {
        "desc":"air quality is unhealthy for sensitive groups like elders or young children and babies. They should limit time spent outside",
        "level":2
        },
    200: {
        "desc":"everyone may experience health effects and should limit outdoor activity.",
        "level":3
        },
    300: {
        "desc":"everyone may experience serious health effects and should avoid outdoor activities.",
        "level":4
        },
    500: {
        "desc":"air quality is hazardous: everyone will experience serious health effects",
        "level":5
        }
}
