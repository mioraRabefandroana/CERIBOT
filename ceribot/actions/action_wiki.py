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
from utils.custom_html import custom_response_message, to_html

class ActionWiki(Action):
    def name(self) -> Text:
        return "action_wiki"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        terme_cle = tracker.get_slot("demande_wiki") 
        try:
            current_state = tracker.current_state()
            latest_message = current_state["latest_message"]["text"]
            wikipedia.set_lang("fr")
            data = wikipedia.summary(terme_cle, sentences=2)
        except wikipedia.exceptions.PageError:
            data = "Aucune correspondace n'a été trouvé. Veillez réessayer!"

        html = to_html( "<div class='joke'>{0}</div>".format( data ))
        dispatcher.utter_message(custom_response_message(data, html))

        return []

