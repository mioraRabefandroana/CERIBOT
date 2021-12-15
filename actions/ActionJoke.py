from typing import Any, Dict, List, Text
from actions.utils.custom_url_request import send_request
from utils.api_urls import JOKE_URL
from rasa_sdk import Action, Tracker
import urllib.request
import json

class ActionJoke(Action):
    def name(self) -> Text:
        return "action_joke"

    """
    convert results (json format) into a readable message
    """
    def get_result_message(self):
        return self.speakable_joke(self.joke)


    """
    format joke into a better speakable text for NAO/Pepper
    """
    def speakable_joke(self, joke):
        return joke


    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----action_joke-----")
        
        url = JOKE_URL
        self.joke = json.loads( urllib.request.urlopen(url).read() ).get("results")

        print(self.joke)
        dispatcher.utter_message(self.get_result_message())
        return []