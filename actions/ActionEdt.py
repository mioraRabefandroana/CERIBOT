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
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

class ActionEdt(Action):
    def name(self) -> Text:

        return "action_edt"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("hello")
        msg = ""
        personName = tracker.get_slot('name')
        print("name :", personName)
        if(personName is None):
            personName = "anonyme"
        else:
            msg = "Salut {0} \n".format(personName)

        # message renvoyé à l'utilisateur
        msg = msg + "---mon message revoyé!! ;)"
        dispatcher.utter_message(msg)

        # return [{"edt": "voici le résultat"}]
        return [SlotSet("name", personName)]