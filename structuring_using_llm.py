import os

from groq import Groq

client = Groq(
    api_key='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',
)
message ="""
FROM? MARITIME SURVEILLANCE UNIT ALRAA
TO % NAVAL OPERPTIONS CommAND
PRIORITY ¢ IMMEDIBTE

OTH Q6A2302 oct a4

UNIDENTIFIED Suamarine OFTEGED oF THE Const OF KERALA
COORDINGTES 5 (0° 00/N ) TIS'E,

SUBMARINE MOVING FT ROOKNOIS, HERDING AT A 45 - DEGREE
ANCE

CURRENT DEPTH 2 KO METRES
INITIAY DETELON AT 2200 UTC ON (E&I 24 OCT 2024

NO COMMUNICATION WAS RECEIVEO FROM VEMEL
POSIBLE THREAT DUE To Hidit-SeEED MOVEMENT IN RESTRIGED
WTERS ,

RESUESTING INMEDIATIE DEPLOYMENT oF SURVEIMANUE AND
INTERCEPTOR UNITS TO ASSESS AND NEVTRAUSE POTENTIAV
THREAT






"""
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": """Your role is a text-structuring model nothing else structure the below text into (NO comments and no additional text)
           ''' {
                datetime:(always convert it to yyyy-mm-dd format) ,
                coords: [[lat1, lon1],[latn,lonn]] ,
                description:( descriptive summary of the whole message),
                speed : (unknown if not mentioned ),
                directions: (unknown if not mentioned),
                depth :(unknown if not mentioned ) 
                
                
            }'''
            format"""
            +f"""
            Context:
      {message}
            """,
        }
    ],
    model="llama3-70b-8192",
)

print(chat_completion.choices[0].message.content)