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

from typing import Any, Dict, List, Text
from actions.utils.custom_url_request import BASE_URL, send_request
from utils.custom_messages import INTRO_SALLE_DISPONIBLE, NO_CLASSROOM_AVAILABLE
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
import urllib.request
import json

class ActionSalleDisponible(Action):
    def name(self) -> Text:

        return "action_classroom_availability"

    def set_result(self, value):
        self.results = value.get("results")

    # convert results (json format) into a readable message
    def get_result_message(self):
        # no available classroom
        if(not self.results or len(self.results) == 0):
            return NO_CLASSROOM_AVAILABLE
        
        msg = INTRO_SALLE_DISPONIBLE
        for salle in self.results:
            msg += salle["libelle"]+".\n"
            
        return msg

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----action_classroom_availability-----")
        
        url = BASE_URL + "api/salles/disponibilite"
        requestData = {
            "site": "CERI",
            "date": "2021-12-13",
            "duree": "3",
            "debut": "10.30"
        }

        data = send_request(url, requestData)
        self.set_result( data )


        dispatcher.utter_message(self.get_result_message())

        # return [SlotSet("name", personName)]
        return []