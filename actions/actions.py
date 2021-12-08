# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.get_slot('city')

        API_key = "30b769c3babdac103e4dfef554b32115"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
        Final_url = base_url + "appid=" + API_key + "&q=" + city + "&units=metric"
        weather_data = requests.get(Final_url).json()

        temperature=weather_data['main']['temp']
        response = "The current temperature at {} is {} degree Celsius.".format(city,temperature)
        
        dispatcher.utter_message(response)

        return [SlotSet('city',city)]



class GreatBot(Action):

    def name(self) -> Text:
        return "action_great_back"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.get_slot('city')

        base_url = "http://localhost:5006"

        data = requests.post(base_url, data ='Hi mood bot, how are you ?').json()

        response = "{} .".format(data.status_code)

        dispatcher.utter_message(response)


        return []