from typing import Any, Dict, List, Text
# from actions.utils.custom_url_request import send_request
from utils.api_urls import JOKE_URL
from rasa_sdk import Action, Tracker
import urllib.request
import json
import subprocess

from utils.custom_html import custom_response_message, to_html

class ActionJoke(Action):
    def name(self) -> Text:
        return "action_blague"

    """
    convert results (json format) into a readable message
    """
    def get_result_message(self):
        html = to_html( "<div class='joke'>{0}</div>".format( self.joke )  )
        text = self.speakable_joke(self.joke)
        return custom_response_message(text, html)


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

        dispatcher.utter_message(self.get_result_message())
        return []