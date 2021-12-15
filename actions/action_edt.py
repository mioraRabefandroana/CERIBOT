# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionEDT(Action):
    def name(sefl) -> Text:
        return "requete_edt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            niveau = tracker.get_slot('niveau')
            formation = tracker.get_slot('formation')
            
            text = text='Vous avez demander votre emploie du temps pour la formation '+ niveau + ' ' +formation
            dispatcher.utter_message(text)
            return []

