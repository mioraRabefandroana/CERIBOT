# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

###################################
# Lien explicatif :https://forum.rasa.com/t/deploy-actions-server-with-multiple-custom-actions-file/28100
######################################
'''
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
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

# Custom action to get timetable from CERI EDT API

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


class ActionSALLES(Action):
    def name(sefl) -> Text:
        return "requete_salle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text='Vous avez demander des renseignements sur une salle!')
            return []

class ActionPROF(Action):
    def name(sefl) -> Text:
        return "requete_prof"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text='Vous avez demander demander des renseignements sur un professeur!')
            return []
'''