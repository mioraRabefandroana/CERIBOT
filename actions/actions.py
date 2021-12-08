# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, cast
import wikipedia 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "requete_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #search = "Who is Obama ?" 
        #searc = tracker.get_slot("requete") 
        try:

            current_state = tracker.current_state()
            latest_message = current_state["latest_message"]["text"]
            

            data = wikipedia.summary(latest_message, sentences=1)
            #print("ojjjjjjjjjjjjjjjjjjjj",search,data)
            dispatcher.utter_message(data)
        except wikipedia.exceptions.PageError:
            data = "No answer has been found.\nPlease tray again!"
            dispatcher.utter_message(data)
        return []

