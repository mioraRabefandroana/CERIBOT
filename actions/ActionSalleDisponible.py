from typing import Any, Dict, List, Text
from actions.utils.custom_url_request import send_request
from utils.api_urls import CLASSROOM_AVAILAIBILITY_URL
from utils.custom_messages import INTRO_SALLE_DISPONIBLE, NO_CLASSROOM_AVAILABLE
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
import re

class ActionSalleDisponible(Action):
    def name(self) -> Text:

        return "action_classroom_availability"

    """
    save resutls
    """
    def set_result(self, value):
        self.results = value.get("results")

    """
    convert results (json format) into a readable message
    """
    def get_result_message(self):
        # no available classroom
        if(not self.results or len(self.results) == 0):
            return NO_CLASSROOM_AVAILABLE
        
        msg = INTRO_SALLE_DISPONIBLE
        for salle in self.results:
            libelle = salle["libelle"]
            msg += self.speakable_salle_libelle(libelle) + ",\n"
            
        return msg


    """
    format salle libelle into a better speakable text for NAO/Pepper
    """
    def speakable_salle_libelle(self, libelle):
        libelle = re.sub(r'^s',"salle ", libelle)
        libelle = re.sub(r'=',".",libelle)
        libelle = re.sub(r' 0'," ",libelle)
        return libelle


    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----action_classroom_availability-----")
        
        url = CLASSROOM_AVAILAIBILITY_URL
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