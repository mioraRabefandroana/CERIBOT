
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
from utils.custom_html import custom_response_message, to_html

class ActionMeteo(Action):

    def name(self) -> Text:
        return "action_meteo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ville = tracker.get_slot('ville')

        API_key = "30b769c3babdac103e4dfef554b32115"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
        Final_url = base_url + "appid=" + API_key + "&q=" + ville + "&units=metric"
        weather_data = requests.get(Final_url).json()

        temperature=weather_data['main']['temp']
        response = "La température actuelle à {} est de {} degrée Celsius.".format(ville,temperature)

        html = to_html( "<div class='joke'>{0}</div>".format( response ))
        dispatcher.utter_message(custom_response_message(response, html))

        
        return  []


